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
    
    # NEW: what this anchor considers helpful (e.g. ["weapon", "ranged"])
    desired_tags: List[str] = field(default_factory=list)
    # NEW: what this anchor wants to avoid (e.g. ["security", "police"])
    disfavored_tags: List[str] = field(default_factory=list)

    tag_weights: Dict[str, float] = field(default_factory=dict)

    source: Union[object, None] = None
    active: bool = True
    time_created: float = field(default_factory=time.time)

    

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