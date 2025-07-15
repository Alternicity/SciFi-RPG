#anchor_utils.py
from dataclasses import dataclass, field
from typing import Literal, List, Union, Dict
import time
from memory_entry import MemoryEntry


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
    tag_weights: Dict[str, float] = field(default_factory=dict)
    # NEW: what this anchor considers helpful (e.g. ["weapon", "ranged"])
    desired_tags: List[str] = field(default_factory=list)
    # NEW: what this anchor wants to avoid (e.g. ["security", "police"])
    disfavored_tags: List[str] = field(default_factory=list)
    
    source: Union[object, None] = None
    active: bool = True
    time_created: float = field(default_factory=time.time)

    

    def is_percept_useful(self, percept_data: dict) -> bool:
        """Return True if this percept contains tags useful to this anchor."""
        tags = percept_data.get("tags", [])
        return any(tag in tags for tag in self.desired_tags)

    def compute_salience_for(self, percept_data: dict, npc) -> float:
        """
        Anchors define how salience is computed for percepts.
        """
        percept_tags = set(percept_data.get("tags", []))
        overlap = set(self.tags) & percept_tags
        base_score = 1.0

        if not overlap:
            return 1.5  # Default: not relevant at all

        score = base_score - (0.1 * len(overlap))

        # Bonus if this percept is useful to the anchor
        if self.is_percept_useful(percept_data):
            score -= 0.3

        # Penalty if the percept has undesirable traits
        if any(tag in percept_tags for tag in self.disfavored_tags):
            score += 0.4

        # Extra penalty for irrelevant types
        if percept_data.get("type") in {"PoliceStation", "ApartmentBlock"}:
            score += 0.3

        return round(score * self.weight, 2)


class RobberyAnchor(Anchor):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "rob")
        kwargs.setdefault("type", "motivation")
        kwargs.setdefault("tags", ["robbery", "crime", "weapon"])
        kwargs.setdefault("desired_tags", ["ranged_weapon", "gun", "weapon"])
        kwargs.setdefault("disfavored_tags", ["security", "police"])
        # kwargs.setdefault(...) only sets a default if the key is not already present,
        # avoiding conflicts when name="rob" is already in kwargs.
        super().__init__(**kwargs)

        #add a desired_objects or useful_items field to RobberyAnchor to support 
        # general-purpose planning or layered salience.

        def compute_salience_for(self, percept_data, npc) -> float:
            score = super().compute_salience_for(percept_data, npc)

            if "robbable" in percept_data and percept_data["robbable"]:
                score -= 0.2
            if "has_security" in percept_data and percept_data["has_security"]:
                score += 0.2

            return round(score * self.weight, 2)

def create_anchor_from_motivation(motivation) -> Anchor:
    from anchor_utils import RobberyAnchor, ObtainWeaponAnchor

    tags = motivation.tags

    if motivation.type == "rob":
        return RobberyAnchor(
            name="rob",
            type="motivation",
            weight=motivation.urgency,
            priority=motivation.urgency,
            tags = tags,
            source=motivation
        )

    if motivation.type == "obtain_ranged_weapon":
        return ObtainWeaponAnchor(
            name="obtain_ranged_weapon",
            type="motivation",
            weight=motivation.urgency,
            priority=motivation.urgency,
            tags = tags,
            source=motivation
        )

    return Anchor(#same here
        name=motivation.type,
        type="motivation",
        weight=motivation.urgency,
        priority=motivation.urgency,
        tags = tags,
        source=motivation
    )



def create_anchor_from_thought(self, npc, thought, name: str, anchor_type: str = "motivation") -> Anchor:
    anchor = Anchor(
        name=name,
        type=anchor_type,
        weight=thought.urgency,
        source=thought,
        tags=thought.tags
    )
    npc.motivation_manager.update_motivations(anchor.name, urgency=anchor.weight, source=thought)

    memory_entry = MemoryEntry(
        subject=npc.name,
        object_="anchor",
        verb="generated",
        details=f"Anchor {anchor.name} from thought '{thought.content}'",
        tags=["anchor", "thought"],
        target=anchor,
        importance=thought.urgency,
        type="anchor_creation",
        initial_memory_type="episodic"
    )
    npc.mind.memory.add_episodic(memory_entry)

    return anchor

class ObtainWeaponAnchor(Anchor):
    def compute_salience_for(self, percept_data, npc) -> float:
        score = 1.5  # start low
        #score = super().compute_salience_for(percept_data, npc)
        tags = percept_data.get("tags", [])
        origin = percept_data.get("origin", None)

        print(f"[SALIENCE] Score: {score:.2f} for {percept_data.get('name', percept_data.get('type'))} | Anchor: {self.name}")

        if "weapon" in tags:
            score -= 0.6  # more relevant
        if "ranged" in tags:
            score -= 0.4  # even better
        if getattr(origin, "location", None) == npc.location:
            score -= 0.3  # boost for being right here
        if percept_data.get("type") == "Location":
            score += 0.6  # penalize locations
        if "has_security" in percept_data and percept_data["has_security"]:
            score += 0.2  # slightly less attractive

        return round(score * self.weight, 2)