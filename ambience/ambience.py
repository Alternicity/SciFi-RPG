#ambience.py 
from dataclasses import dataclass, field
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters import Character
    from objects.InWorldObjects import ObjectInWorld

@dataclass
class Ambience:
    vibes: dict[str, float] = field(default_factory=dict)

    def absorb(self, character: "Character") -> dict:
        return {
            vibe: power * (character.psy / 20) * character.get_ambience_filter(vibe)
            for vibe, power in self.vibes.items()
        }

    def blend(self, other: "Ambience"):
        for k, v in other.vibes.items():
            self.vibes[k] = self.vibes.get(k, 0) + v

    @staticmethod
    def from_objects(objects: list["ObjectInWorld"]) -> "Ambience":
        total = defaultdict(float)
        for obj in objects:
            if hasattr(obj, "modulated_ambience"):
                modulated = obj.modulated_ambience()
                for k, v in modulated.items():
                    total[k] += v
        return Ambience(dict(total))

    
""" Example Usage in a Location Class
In your Location or Sublocation, add:

def update_ambience(self):
    self.ambience = Ambience.from_objects(self.objects_present) """

""" Call this during:
Location setup
Whenever objects are added/removed
Tick start
 """

""" This allows:
Passive narrative emergence
Psy-based sensitivity
Symbolic design of locations """