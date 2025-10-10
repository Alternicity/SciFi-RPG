#anchor_utils.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, List, Union, Dict, TYPE_CHECKING, Optional, Any

import time
from memory_entry import MemoryEntry
from debug_utils import debug_print
from create_game_state import get_game_state

if TYPE_CHECKING:
    from character_thought import Thought
    from character import Character

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

    def __post_init__(self):
        """Stamp simulation time (tick/day) on creation if possible."""
        try:
            state = get_game_state()
            self.tick_created = getattr(state, "tick", None)
            self.day_created = getattr(state, "day", None)
        except Exception as e:
            self.tick_created = None
            self.day_created = None
            debug_print(
                self.owner,
                f"[ANCHOR INIT] Warning: Could not access game state for {self.name}: {e}",
                category="anchor"
            )

        # Optional debug trace of creation context
        if self.owner:
            debug_print(
                self.owner,
                f"[ANCHOR CREATED] {self.name} (type={self.type}) "
                f"tick={self.tick_created}, day={self.day_created}",
                category="anchor"
            )

    def compute_salience_for(self, percept_data, npc) -> float:
        tags = percept_data.get("tags", [])
        score = 1.0

        if not any(tag in tags for tag in self.desired_tags):
            score += 0.5  # Penalize irrelevant
        if any(tag in tags for tag in self.disfavored_tags):
            score += 0.5  # Penalize unwanted traits

        for tag in tags:
            score += self.tag_weights.get(tag, 0)

        return round(score * self.weight, 2)

    def is_percept_useful(self, percept_data: dict) -> bool:
        tags = percept_data.get("tags", [])
        return any(tag in tags for tag in self.desired_tags)


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
            "ranged_weapon": 0.7,
            "shop": 0.3,
            "security": -0.4,
            "police": -0.6,
            "alert_employee": -0.5,
        })
        super().__init__(**kwargs)



    def compute_salience_for(self, percept_data, npc) -> float:
        score = super().compute_salience_for(percept_data, npc)

        # Penalize already-armed NPCs
        if npc.inventory.has_ranged_weapon():
            score -= 0.4
        elif npc.inventory.has_melee_weapon():
            score -= 0.2
        else:
            if "ranged_weapon" in percept_data.get("tags", []):
                score += 0.3
            elif "melee_weapon" in percept_data.get("tags", []):
                score += 0.1

        return score
        #return round(score * self.weight, 2)

def create_anchor_from_motivation(npc, motivation) -> Anchor:
    from anchor_utils import RobberyAnchor, ObtainWeaponAnchor

    tags = motivation.tags

    if motivation.type == "rob":
        return RobberyAnchor(
            name="rob",
            type="motivation",
            weight=motivation.urgency,
            priority=motivation.urgency,
            tags = tags,
            owner=npc,
            source=motivation
        )

    if motivation.type == "obtain_ranged_weapon":
        return ObtainWeaponAnchor(
            name="obtain_ranged_weapon",
            type="motivation",
            weight=motivation.urgency,
            priority=motivation.urgency,
            tags = tags,
            owner=npc,
            source=motivation
        )

    return Anchor(
        name=motivation.type,
        type="motivation",
        weight=motivation.urgency,
        priority=motivation.urgency,
        tags = tags,
        owner = npc,
        source=motivation
    )


#line 134, utility function, ie not in a class definition
def create_anchor_from_thought(npc, thought: "Thought", name: str = None) -> "Anchor":#Thought is stilll marked as not defined
    from character_thought import Thought #Thought not accessed 
    """
    Converts a Thought into a Motivation Anchor, carrying over tags and urgency.
    """
    anchor_name = name or f"{thought.subject}_{int(thought.timestamp)}"
    anchor = Anchor(
        name=anchor_name,
        type="motivation",
        weight=thought.urgency or 1.0,
        priority=thought.weight or 1.0,
        tags=thought.tags,
        #add a reference to npc here?
        desired_tags=thought.tags,  # Could filter/refine later
        disfavored_tags=[],
        tag_weights={tag: 1.0 for tag in thought.tags},
        owner=npc,
        source=thought
    )
    
    urgency_delta = min(int(anchor.weight or 1), 3)
    npc.motivation_manager.update_motivations(motivation_type=anchor.name, urgency=urgency_delta)

    #the following might be up for deletion. I am not sure if creating an episodic memory every time a 
    #anchor is created is necessary. npcs can already accesss their anchor via self.current_anchor or similiar 
    memory_entry = MemoryEntry(
        subject=npc.name,
        object_="anchor",
        verb="generated",
        details=f"Anchor {anchor.name} from thought '{thought.content}'",
        tags=["anchor", "thought"],
        target=anchor,
        importance=thought.urgency,
        type="anchor_creation",
        initial_memory_type="episodic",
        function_reference=None,
        implementation_path=None,
        associated_function=None
    )
    npc.mind.memory.add_episodic(memory_entry)

    return anchor

class ObtainWeaponAnchor(Anchor):
    def compute_salience_for(self, percept_data, npc) -> float:
        origin = percept_data.get("origin", None)

        # Don't consider self or owned items as salient
        if origin is npc:
            return 0
        #possibly check self.inventory here, I'm not sure origin is reliable for this

        score = 1.5  # Base score
        print(f"[SALIENCE] First ObtainWeaponAnchor Score: {score:.2f} for {percept_data.get('name', percept_data.get('type'))} | Anchor: {self.name}")

        tags = percept_data.get("tags", [])
        if "weapon" in tags:
            score += 0.3  # more relevant. HIGHER salience is more salience, ie more useful to the npc
        if "ranged" in tags:
            score += 0.6  # even better
        if getattr(origin, "location", None) == npc.location:
            score += 0.3  # boost for being right here
        if "has_security" in percept_data and percept_data["has_security"]:
            score -= 1.0  #location is less attractive

        print(f"[SALIENCE] Second ObtainWeaponAnchor Score: {score:.2f} for {percept_data.get('name', percept_data.get('type'))} | Anchor: {self.name}")

        return round(score * self.weight, 2)
    
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