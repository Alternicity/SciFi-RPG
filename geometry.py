#geometry.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class GeometryInfluence:
    name: str
    points: int
    effect_on_thoughts: Dict[str, float]

    def apply_to_character(self, npc):
        for thought in npc.mind.thoughts:
            for tag, amp in self.effect_on_thoughts.items():
                if tag in thought.tags:
                    thought.urgency *= amp

# Dodecagon zone: amplifies abstract pattern thought
#dodecagon = GeometryInfluence("dodecagon", 12, {"geometry": 1.4, "meta": 1.2})
# Triangle: encourages completion, resolution
#triangle = GeometryInfluence("triangle", 3, {"goal": 1.5, "math": 1.2})
