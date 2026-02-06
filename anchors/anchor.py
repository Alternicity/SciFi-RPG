#anchors.anchor.py

from dataclasses import dataclass, field
from typing import Literal, List, Union, Dict, TYPE_CHECKING, Optional, Any
import re
import time
from debug_utils import debug_print
from create.create_game_state import get_game_state

#Do not import anchor_utils or NPC logic

""" Never read NPC state at class scope.
Always read it inside a method that receives npc. """

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

    #Add anchor “confidence decay” to stop flip-flopping
    
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