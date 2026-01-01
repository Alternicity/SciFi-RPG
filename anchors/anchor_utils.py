#anchors.anchor_utils.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, List, Union, Dict, TYPE_CHECKING, Optional, Any
import re

from events import Event #maybe risky import
from anchors.work_anchor import WorkAnchor
from anchors.eat_anchor import EatAnchor
import time
from memory.memory_entry import MemoryEntry
from debug_utils import debug_print
from create.create_game_state import get_game_state
from weapons import Weapon, RangedWeapon
from events import Event
if TYPE_CHECKING:
    from character_thought import Thought
    from base.character import Character#not accessed


#canonical coercion helper
def _normalize_percept(percept_data, npc):
    """
    Return a safe percept dict with keys:
    { 'object', 'name', 'tags', 'origin', 'salience', 'details' }
    """
    #use _normalize_percept() in anchor methods

    # dict already
    if isinstance(percept_data, dict):
        p = dict(percept_data)  # shallow copy
        p.setdefault("object", p.get("origin", p.get("object")))
        p.setdefault("name", p.get("name", str(p.get('object', '<unknown>'))))
        p.setdefault("tags", p.get("tags", []))
        p.setdefault("salience", p.get("salience", 1.0))
        p.setdefault("origin", p.get("origin", p.get("object")))
        return p

    # objects that implement get_percept_data(observer=)
    if hasattr(percept_data, "get_percept_data"):
        try:
            p = percept_data.get_percept_data(observer=npc) or {}
            p.setdefault("object", percept_data)
            p.setdefault("name", getattr(percept_data, "name", str(percept_data)))
            p.setdefault("tags", getattr(percept_data, "tags", []))
            p.setdefault("salience", getattr(percept_data, "salience", 1.0))
            p.setdefault("origin", percept_data)
            return p
        except Exception:
            pass

    # fallback synthesis
    tags = list(getattr(percept_data, "tags", []) or [])
    name = getattr(percept_data, "name", None) or str(percept_data)
    return {
        "object": percept_data,
        "name": str(name),
        "tags": tags,
        "origin": getattr(percept_data, "origin", percept_data),
        "salience": getattr(percept_data, "salience", 1.0),
    }
    #rhis print is structureally unreachable
    #debug_print(npc, f"([ANCHOR DEBUG]  normalize_percept fallback activated, catagory = "anchor"))

#The Anchor object becomes a harmonic attractor: it pulls salience into form.
#context-aware decision filter
@dataclass
class Anchor:
    name: str  # e.g., "rob", "join_faction"
    type: Literal["motivation", "plan", "event", "object"]
    weight: float = 1.0  # salience amplification factor
    priority: float = 1.0  # importance to current AI thinking
    enables: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)  # used in tag-overlap salience logic
    owner: Optional[Any] = None  # populated with npc object at runtime
    desired_tags: List[str] = field(default_factory=list)
    disfavored_tags: List[str] = field(default_factory=list)
    tag_weights: Dict[str, float] = field(default_factory=dict)
    source: Union[object, None] = None
    active: bool = True
    time_created: float = field(default_factory=time.time)
    target_object: Optional[Any] = None  # e.g., ObjectInWorld, Location, Region, Character
    # Simulation timing
    tick_created: Optional[int] = None
    day_created: Optional[int] = None
    target_location: Optional[Any] = None
    _warned_no_target: bool = False

    #Object lifecycle logs belong at creation sites, not constructors.

    def __post_init__(self):
        """Stamp simulation time (tick/day) on creation if possible."""
        try:
            state = get_game_state()
            self.hour_created = getattr(state, "hour", None)
            self.day_created = getattr(state, "day", None)
        except Exception as e:
            self.hour_created = None
            self.day_created = None
            debug_print(
                self.owner,
                f"[ANCHOR INIT] Warning: Could not access game state for {self.name}: {e}",
                category="anchor"
            )

    def resolve_target_location(self):
        npc = self.owner

        if self.target_location is None:
            if not getattr(self, "_warned_no_target", False):
                debug_print(
                    self.owner,
                    f"[ANCHOR] {self.name} has no target_location to resolve",
                    category="anchor"
                )
                self._warned_no_target = True
            return None
        
    
        debug_print(
            self.owner,
            f"[ANCHOR] {self.name} resolved target_location -> {getattr(self.target_location, 'name', self.target_location)}",
            category="anchor"
        )
        return self.target_location

    def _coerce_to_percept(self, percept_data, npc) -> dict:
        """
        Normalize any input (dict, object, or string) into a percept-like dict.
        Handles dicts, PerceptibleMixin objects, Characters, Weapons, Locations, etc.
        """

        # --- 1. Already a percept dict ---
        if isinstance(percept_data, dict):
            return percept_data

        # --- 2. Try get_percept_data(observer=) if available ---
        if hasattr(percept_data, "get_percept_data"):
            try:
                p = percept_data.get_percept_data(observer=npc) or {}
                p.setdefault("object", percept_data)
                p.setdefault("name", getattr(percept_data, "name", str(percept_data)))
                p.setdefault("tags", getattr(percept_data, "tags", []))
                p.setdefault("salience", p.get("salience", 1.0))
                return p
            except Exception:
                pass  # fall through to synthesis

        # --- 3. Synthesize percept dict based on type introspection ---
        tags = list(getattr(percept_data, "tags", []) or [])
        details = {}

        # Handle Character-like objects
        if hasattr(percept_data, "race") and hasattr(percept_data, "sex"):
            tags += ["character", percept_data.sex.lower()]
            details.update({
                "race": getattr(percept_data, "race", None),
                "sex": getattr(percept_data, "sex", None),
                "faction": getattr(percept_data, "faction", None),
                "status": getattr(percept_data, "status", None),
            })

        # Handle Weapon-like objects
        if hasattr(percept_data, "damage") and hasattr(percept_data, "intimidation"):
            tags += ["weapon"]
            if hasattr(percept_data, "ammo"):
                tags.append("ranged")
            if getattr(percept_data, "bloodstained", False):
                tags.append("bloodstained")

            details.update({
                "damage": getattr(percept_data, "damage", None),
                "intimidation": getattr(percept_data, "intimidation", None),
                "owner": getattr(percept_data, "owner", None),
                "range": getattr(percept_data, "range", None),
                "ammo": getattr(percept_data, "ammo", None),
            })

        # Handle Location-like objects
        if hasattr(percept_data, "is_shop") or hasattr(percept_data, "robbable"):
            tags += ["location"]
            if getattr(percept_data, "is_shop", False):
                tags.append("shop")
            if getattr(percept_data, "robbable", False):
                tags.append("robbable")

            details.update({
                "region": getattr(percept_data, "region", None),
                "robbable": getattr(percept_data, "robbable", None),
            })

        # Fallback name
        name = getattr(percept_data, "name", None) or (
            percept_data if isinstance(percept_data, str) else percept_data.__class__.__name__
        )

        # --- 4. Final percept structure ---
        """
        Return a canonical percept dict:
        { object, name, tags, salience, origin, details }
        """
        # use the helper to normalize
        try:
            percept = _normalize_percept(percept_data, npc)
        except Exception:
            percept = {
                "object": percept_data,
                "name": str(percept_data),
                "tags": getattr(percept_data, "tags", []),
                "salience": 0.5,
                "origin": percept_data
            }
        return percept
    
    #Tags may adjust salience, but may never grant eligibility, classes do.
    def compute_salience_for(self, percept_data, npc) -> float:
        """
        Generic anchor salience computation.
        Always uses safe percept dict from _coerce_to_percept.
        """

        # --- normalize percept safely ---
        percept = self._coerce_to_percept(percept_data, npc)

        obj   = percept.get("object")
        name  = percept.get("name", "<unnamed>")
        tags  = percept.get("tags", []) or []

        # --- base score ---
        score = float(getattr(self, "base_salience", 0.0))

        # --- tag-based boosts ---
        if "weapon" in tags:
            score += 0.4
        if "shop" in tags:
            score += 0.3

        # --- reduce score if NPC already has a ranged weapon ---
        has_ranged_weapon = False
        try:
            has_ranged_weapon = npc.inventory.has_ranged_weapon() \
                if callable(npc.inventory.has_ranged_weapon) \
                else bool(npc.inventory.has_ranged_weapon)
        except Exception:
            pass

        if has_ranged_weapon:
            score *= 0.5

        # --- attempt to extract a robbery target name from textual content ---
        target_name = None
        content = getattr(obj, "content", None)

        if isinstance(content, str):
            import re
            m = re.search(r"rob\s+([A-Za-z0-9_'\-]+)", content, flags=re.IGNORECASE)
            if m:
                target_name = m.group(1)

        return round(score, 2)

    def is_percept_useful(self, percept_data: Any, npc=None) -> bool:
        """
        Lightweight filter: returns True if percept shares any tags with this anchor's desired_tags.
        Salience handles deeper context; this is just an early short-circuit.
        """
        percept = self._coerce_to_percept(percept_data, npc)
        tags = percept.get("tags", []) or []
        if not self.desired_tags:
            return True
        for tag in self.desired_tags:
            if tag in tags:
                return True
        return False
    
    @property
    def motivation_type(self):
        return self.name or self.type

#utilty functions
def select_best_anchor(npc, anchors):
    if not anchors:
        return None

    viable = [a for a in anchors if not getattr(a, "blocked", False)]
    if not viable:
        return None

    return max(viable, key=lambda a: getattr(a, "urgency", 0))

def deduplicate_anchors(npc):
        """
        Keep strongest anchor per name.
        Ensures npc.current_anchor remains valid.
        """
        seen = {}

        for anchor in npc.anchors:
            key = anchor.name
            if key not in seen or anchor.priority > seen[key].priority:
                seen[key] = anchor

        npc.anchors = list(seen.values())

        # Re-link current_anchor if needed
        if npc.current_anchor:
            npc.current_anchor = seen.get(
                npc.current_anchor.name,
                npc.current_anchor
            )




class RobberyAnchor(Anchor):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "rob")
        kwargs.setdefault("type", "motivation")
        kwargs.setdefault("tags", ["robbery", "crime", "weapon"])
        kwargs.setdefault("desired_tags", ["ranged_weapon", "gun", "weapon"])
        kwargs.setdefault("disfavored_tags", ["security", "police", "alert_employee"])
        #"rival_faction" could figure in here, depending on a gangs violence_disposition

        # kwargs.setdefault(...) only sets a default if the key is not already present,
        # avoiding conflicts when name="rob" is already in kwargs.
        # Set default tag_weights if not already defined
        kwargs.setdefault("tag_weights", {
            "weapon": 0.5,
            "ranged_weapon": 0.7,#it’s a weighting factor, not a subtraction, 0.7 adds to total salience.
            "shop": 0.3,
            "security": -0.4,
            "police": -0.6,
            "alert_employee": -0.5,
        })

        

        super().__init__(**kwargs)


    def compute_salience_for(self, percept_data, npc) -> float:
        percept = self._coerce_to_percept(percept_data, npc)
        obj = percept.get("object")
        tags  = percept.get("tags", []) or []
        name = percept.get("name", "<unnamed>")

        # Ignore NPCs, events, etc.
        from events import Event
        if obj is npc or isinstance(obj, Event) or isinstance(obj, npc.__class__):
            return 0.0

        # base score from Anchor
        score = super().compute_salience_for(percept, npc)

        # Weapon-based adjustments
        if npc.inventory.has_ranged_weapon():
            score -= 0.4
        elif "ranged_weapon" in tags:
            score += 0.3
        elif "melee_weapon" in tags:
            score += 0.1

        # Extract robbery target name
        target_name = None
        content = getattr(obj, "content", None)
        if isinstance(content, str):
            import re
            m = re.search(r"rob\s+([A-Za-z0-9_'\-]+)", content, flags=re.IGNORECASE)
            if m:
                target_name = m.group(1)
                
        # Suppress turf-war salience logs
        if tags and "turf_war" in tags:
            return

        return round(score, 2)

class just_got_off_shift(Anchor):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "just_got_off_shift")
        kwargs.setdefault("type", "motivation")
        kwargs.setdefault("tags", ["employment", "unwind", "habit", "co_workers"])
        kwargs.setdefault("desired_tags", ["unwind", "exit", "procure_food", "", "social_thoughts"])
        kwargs.setdefault("disfavored_tags", ["workplace_thoughts", "workplace", "alert_employee"])
        #"rival_faction" could figure in here, depending on a gangs violence_disposition

        # kwargs.setdefault(...) only sets a default if the key is not already present,
        # avoiding conflicts when name="rob" is already in kwargs.
        # Set default tag_weights if not already defined
        kwargs.setdefault("tag_weights", {
            "unwind": 0.5,#should feed an unwind motivation
            "habit": 0.7,
            "procure_food": 0.6,#it’s a weighting factor, not a subtraction, 0.6 adds to total salience.
            "idle": -0.4,#feeds the motivation
            "social_thoughts": 0,#I will make a function and a motivation
            "seek_solitude": -0.5,#reverse of above tag
        })

        

        super().__init__(**kwargs)


    def compute_salience_for(self, percept_data, npc) -> float:
        percept = self._coerce_to_percept(percept_data, npc)
        obj = percept.get("object")
        tags  = percept.get("tags", []) or []
        name = percept.get("name", "<unnamed>")
        target = npc.anchor.target
        # Ignore NPCs, events, etc.
        from events import Event
        if obj is npc or isinstance(obj, Event) or isinstance(obj, npc.__class__):
            return 0.0

        # base score from Anchor, this section will calcualte the salience of objects for getting off shift
        score = super().compute_salience_for(percept, npc)#memories, thoughts, habits, home, partner to add here for this anchor. I think

        #this might not be the ideal logic system here, so needs upgrading
        if npc.XYZ():
            score -= 0.4
        elif "unwind" in tags:#etc
            score += 0.3
        elif "ABC" in tags:
            score += 0.1
        #define target
        debug_print(
            npc,
            f"[ANCHOR-SALIENCE] just_got_off_shift final={score:.2f} for {name}"
            + (f" (target={target})" if target else "")#report on the target, ie what object the npc wants to be near, consume etc
            + f" (tags={tags})",
            category="salience",
        )

        return round(score, 2)




#utility functions
def create_robbery_anchor(npc, source=None, urgency=None, desired_tags=None, disfavored_tags=None, tag_weights=None,):
    """
    General-purpose factory for RobberyAnchor.

    `source` may be:
       - a Motivation
       - a Thought
       - an episodic MemoryEntry
       - None (defaults)
    """

    # Determine urgency and weight from whatever the source is
    u = getattr(source, "urgency", urgency if urgency is not None else 1.0)
    w = getattr(source, "weight", u)

    # construct kwargs to override defaults if desired
    kwargs = {
        "name": "rob",
        "type": "motivation",
        "owner": npc,
        "source": source,
        "priority": u,
        "weight": w,
    }

    # Optional future overrides — only applied if provided
    if desired_tags is not None:
        kwargs["desired_tags"] = desired_tags

    if disfavored_tags is not None:
        kwargs["disfavored_tags"] = disfavored_tags

    if tag_weights is not None:
        kwargs["tag_weights"] = tag_weights

    anchor = RobberyAnchor(**kwargs)

    debug_print(
        npc,
        f"[ANCHOR] Created RobberyAnchor(priority={u}, desired_tags={anchor.desired_tags}) "
        f"from source={type(source).__name__ if source else None}",
        category="anchor",
    )

    return anchor

#utility function
def create_anchor_from_motivation(npc, motivation) -> "Anchor":
    """
    Converts a Motivation into a Motivation Anchor.
    Handles automatic naming, deduplication, memory logging,
    and specialized subclasses (RobberyAnchor, ObtainWeaponAnchor).
    """

    # --- Guard invalid inputs ---
    if motivation is None:
        return None
    
    if motivation.type == "obtain_ranged_weapon" and npc.inventory.has_ranged_weapon():
        debug_print(
            npc,
            "[ANCHOR] Skipping obtain_ranged_weapon anchor — already armed",
            category="anchor"
        )
        return None

    if not hasattr(npc, "anchors") or npc.anchors is None:
        npc.anchors = []

    # --- Auto naming fallback ---
    base_name = getattr(motivation, "type", None) or getattr(motivation, "name", None) or "UnnamedMotivation"
    base_name = str(base_name).strip()

    # --- Deduplicate by existing anchors ---
    if hasattr(npc, "anchors"):
        for existing in npc.anchors:
            if getattr(existing, "source", None) is motivation:
                return existing

    # --- Deduplicate by memory (avoid spam) ---
    existing_memory = [
        m for m in npc.mind.memory.episodic
        if m.type == "anchor_creation"
        and base_name in (m.details or "")
    ]
    if existing_memory:
        return None

    tags = getattr(motivation, "tags", []) or []

    # --- Create specialized anchors ---
    if base_name == "work":
        anchor = WorkAnchor(npc, motivation)


    if base_name == "rob":
        anchor = RobberyAnchor(
            name=base_name,
            type="motivation",
            weight=getattr(motivation, "urgency", 1.0),
            priority=getattr(motivation, "urgency", 1.0),
            tags=tags,
            owner=npc,
            source=motivation,
        )
        anchor.desired_tags = anchor.desired_tags or ["ranged_weapon"]

    elif base_name == "obtain_ranged_weapon":
        anchor = ObtainWeaponAnchor(
            name=base_name,
            type="motivation",
            weight=getattr(motivation, "urgency", 1.0),
            priority=getattr(motivation, "urgency", 1.0),
            tags=tags,
            owner=npc,
            source=motivation,
        )
        anchor.enables = getattr(anchor, "enables", []) + ["rob"]#added
    else:
        anchor = Anchor(
            name=base_name,
            type="motivation",
            weight=getattr(motivation, "urgency", 1.0),
            priority=getattr(motivation, "urgency", 1.0),
            tags=tags,
            owner=npc,
            source=motivation,
        )

        npc.anchors.append(anchor)

        # See when a thought-anchor or motivation-anchor is created without an expected partner
        related = [a.name for a in npc.anchors if a is not anchor]
        if base_name == "rob" and not any("obtain_ranged_weapon" in r for r in related):
            debug_print(npc, f"[ANCHOR] Created '{base_name}' with NO obtain_ranged_weapon enabler", category="anchor")
        elif base_name == "obtain_ranged_weapon" and not any("rob" in r for r in related):
            debug_print(npc, f"[ANCHOR] Created '{base_name}' with NO rob anchor partner", category="anchor")


    # --- Update motivation manager ---
    urgency_delta = min(int(anchor.weight or 1), 3)
    
    if anchor.name != "obtain_ranged_weapon":
        npc.motivation_manager.update_motivations(
            motivation_type=anchor.name,
            urgency=urgency_delta
        )

    # --- Register anchor in NPC memory once ---
    memory_entry = MemoryEntry(
        subject=npc.name,
        object_="anchor",
        verb="generated",
        details=f"Anchor {anchor.name} from motivation '{base_name}'",
        tags=["anchor", "motivation"],
        target=anchor,
        importance=getattr(motivation, "urgency", 0.0),
        type="anchor_creation",
        initial_memory_type="episodic",
        function_reference=None,
        implementation_path=None,
        associated_function=None,
    )
    npc.mind.memory.add_episodic(memory_entry)

    # --- Attach to NPC anchors (always) ---
    if not hasattr(npc, "anchors") or npc.anchors is None:
        npc.anchors = []
    if anchor not in npc.anchors:
        npc.anchors.append(anchor)

    debug_print(
            npc,
            f"[ANCHOR] Created '{anchor.name}' from motivation "
            f"({motivation.type}, urgency={motivation.urgency}) "#motive marked as not defined, so I changed it to motivation
            f"@ day {anchor.day_created}, hour {anchor.hour_created}",
            category="anchor"
        )


    return anchor

#create_anchor_from_motivation and create_anchor_from_thought are generic in name but not in behaviour.

# Once civilian and non-criminal anchors are implemented, split into
# role-specific anchor factories.

def create_anchor_from_thought(npc, thought: "Thought", name: Optional[str] = None) -> Optional["Anchor"]:
    """
    Converts a Thought into an Anchor, carrying over tags and urgency,
    with automatic naming, duplicate prevention, and anchoring flag.
    """

    from character_thought import Thought
    from memory.memory_entry import MemoryEntry
    import time

    # --- Guard: skip invalid or already anchored thoughts ---
    if thought is None:
        return None #is this suggested block meant to replace the subsequent one?

    # Ensure the NPC has an anchors list
    if not hasattr(npc, "anchors"):
        npc.anchors = []

    # If thought already anchored, try to return the existing anchor if present
    if getattr(thought, "anchored", False):#does class thought need an anchored attribute? "anchored" is relatively new to the codebase
        for a in getattr(npc, "anchors", []):
            if getattr(a, "source", None) is thought:
                return a
        return None

    # Build a safe anchor name
    # Preserve canonical motivation names ONLY
    base_name = (
        name
        or thought.primary_tag()              # e.g. "rob", "visit", "explore"
        or getattr(thought, "subject", None)
        or "thought"
    )

    # Force safe canonical form
    canonical = str(base_name).strip().lower()

    anchor_name = canonical  # <-- NO timestamp, NO content slug

    # --- Deduplicate via memory ---
    existing_memory = [
        m for m in npc.mind.memory.episodic
        if m.type == "anchor_creation"
        and (m.details and str(getattr(thought, "content", "")).strip() in m.details)
    ]
    if existing_memory:
        for a in npc.anchors:
            if getattr(a, "source", None) is thought or a.name in existing_memory[0].details:
                return a

    # --- Create the anchor ---
    anchor = Anchor(
        name=anchor_name,
        type="thought",
        weight=getattr(thought, "weight", 1.0),
        priority=getattr(thought, "urgency", 1.0),
        tags=list(getattr(thought, "tags", []) or []),
        owner=npc,
        source=thought,
    )

     #--- Assign target if thought has an origin ---
    origin = getattr(thought, "origin", None)
    anchor.target = getattr(origin, "location", None) if origin else None

    # --- Register the new anchor ---
    npc.anchors.append(anchor)
    thought.anchored = True

    #defensive
    if not hasattr(npc, "anchors") or npc.anchors is None:
        npc.anchors = []

    # Add memory entry with explicit target (prefer anchor.target, fallback to anchor.name)
    target_value = getattr(anchor, "target", None) or anchor.name
    npc.mind.memory.add_entry_if_new( #should this use add_episodic or semantic?
        MemoryEntry(
            subject=npc.name,
            object_=anchor.name,
            details=f"Anchor {anchor.name} from thought '{getattr(thought, 'content', '')}'",
            type="anchor_creation",
            tags=["anchor", "thought"],
            target=target_value
        )
    )
    if thought and not thought.anchored:
        thought.anchored = True
        debug_print(npc, f"[ANCHOR] Thought '{thought.content}' anchored as {anchor.__class__.__name__}", category="anchor")

    return anchor

class ObtainWeaponAnchor(Anchor):

    def compute_salience_for(self, percept_data, npc) -> float:
        percept = self._coerce_to_percept(percept_data, npc)
        obj = percept.get("object")
        tags = percept.get("tags", []) or []
        name = percept.get("name", "<unnamed>")

        # HARD ELIGIBILITY FILTER (NO TAGS HERE)

        # Must be a Weapon instance
        if not isinstance(obj, Weapon):
            return 0.0 

        # Ignore weapons already owned
        if obj.owner is npc:
            return 0.0

        # SOFT SCORING (TAGS & CONTEXT)

        score = 1.0

        # Prefer ranged weapons if NPC already has melee
        if isinstance(obj, RangedWeapon):#RangedWeapon is marked as not defined
            score += 1.0

        debug_print(
            npc,
            f"[ANCHOR-SALIENCE] ObtainWeaponAnchor score={score:.2f} for {name} (tags={tags})",
            category="salience",
        )

        return round(score, 2)


    
#utility functions

def update_saliences_for_anchor(anchor, npc, percepts):
    """Recompute salience for all percepts relative to a given anchor."""
    if not anchor or not percepts:
        return []
    
    updated = []
    for p in percepts:
        score = anchor.compute_salience_for(p["data"], npc)
        p["salience"] = score
        updated.append(p)
    # Use unified debug printing instead of raw print
    debug_print(
        npc=npc,
        message=f"[SALIENCE REFRESH] {npc.name} rescored {len(percepts)} percepts for anchor '{anchor.name}'",
        category="salience"
    )
    return updated
            
            
def refresh_salience_for_anchor(npc, anchor=None):
    """Convenience: re-observe environment and rescore percepts."""
    anchor = anchor or getattr(npc, "current_anchor", None)
    if not anchor:
        return
    npc.observe(location=npc.location, region=npc.region)
    percepts = npc.get_percepts()
    return update_saliences_for_anchor(anchor, npc, percepts)


def _safe_percept_label(percept_data):#marked not accesssed
    if isinstance(percept_data, dict):
        return percept_data.get("description") or percept_data.get("name") or "<unnamed>"
    return getattr(percept_data, "content", None) or getattr(percept_data, "name", "<unnamed>")

def generic_tag_salience_boost(obj, anchor):
    score = 0.0
    if hasattr(obj, "tags") and anchor:
        obj_tags = set(obj.tags or [])
        anchor_tags = set(anchor.tags or [])
        matches = obj_tags & anchor_tags
        if matches:
            score += 1.2 + 0.1 * len(matches)
    return score


def compute_salience_for_percept_with_anchor(obj, anchor, observer=None):
    percept = obj  # Optional alias for clarity
    score = 1.0
    salience += generic_tag_salience_boost(obj, anchor)
    if "tags" in percept and anchor.name in percept["tags"]:
        score += 1.3
    if "location" in percept and observer and percept["location"] == getattr(observer.location, "name", None):
        score += 1.4
    return round(1.0 + (score - 1.0) * anchor.weight, 2)

#example full anchor debug_print
""" if self.npc.is_test_npc and npc.current_anchor:
            a = npc.current_anchor
            debug_print(
                f"[ANCHOR DEBUG] "
                f"name={a.name}, type={a.type}, "
                f"weight={a.weight}, priority={a.priority}, active={a.active}\n"
                f"tags={a.tags}, desired={a.desired_tags}, disfavored={a.disfavored_tags}\n"
                f"owner={getattr(a.owner, 'name', None)}, source={type(a.source).__name__ if a.source else None}",
                category="anchor"
            ) """