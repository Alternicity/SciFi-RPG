#anchor_utils.py
from dataclasses import dataclass, field
from typing import Literal, List, Union
import time
from memory_entry import MemoryEntry

#The Anchor object becomes a harmonic attractor: it pulls salience into form.
@dataclass
class Anchor:
    name: str  # e.g., "rob", "join_faction"
    type: Literal["motivation", "plan", "event", "object"]
    weight: float = 1.0
    priority: float = 1.0#represents how core this anchor is to current action. Separate from weight
    #(which is comparative relevance during salience scoring)
    enables: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list) #Good for fuzzy matching in salience logic
    source: Union[object, None] = None  # where the anchor originated, Thought, Memory, NPC, etc.
    active: bool = True #Whether this anchor is currently driving behavior
    time_created: float = field(default_factory=time.time) #can be useful for decaying relevance
    #You can now begin calling
    #thought.salience_for(npc, anchor=Anchor(name="rob", type="motivation", weight=1.5))

    #   If you're concerned about leakiness, you can tag anchors with .owner or use NPC-specific salience filtering

def compute_salience_for(self, percept_data, npc) -> float:
        """
        Anchors now define how salience is computed for percepts.
        """
        # Generic example: match tags
        overlap = set(self.tags) & set(percept_data.get("tags", []))
        base_score = 1.0

        if not overlap:
            return 1.5  # Irrelevant

        score = base_score - (0.1 * len(overlap))

        # Penalize irrelevant types
        if percept_data.get("type") in {"PoliceStation", "ApartmentBlock"}:
            score += 0.3

        # Add hook for subclasses to override
        return round(score * self.weight, 2)

class RobberyAnchor(Anchor):
    def compute_salience_for(self, percept_data, npc) -> float:
        score = super().compute_salience_for(percept_data, npc)

        if "robbable" in percept_data and percept_data["robbable"]:
            score -= 0.2
        if "has_security" in percept_data and percept_data["has_security"]:
            score += 0.2
        return round(score * self.weight, 2)

def create_anchor_from_motivation(motivation) -> Anchor:
    """
    Converts a Motivation object into an Anchor for salience evaluation.
    """
    return Anchor(
        name=motivation.type,
        type="motivation",
        weight=motivation.urgency,
        priority=motivation.urgency,
        tags=motivation.tags if hasattr(motivation, "tags") else [],
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
