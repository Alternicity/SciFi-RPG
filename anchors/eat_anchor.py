#anchors.eat_anchor.py
from anchors.anchor import Anchor
from memory.memory_builders.memory_utils import best_food_location

class EatAnchor(Anchor):
    #No __init__
    #If an anchor must do extra setup, do it after super().__init__() and keep the signature identical.

    def resolve_target_location(self):
        npc = self.owner
        return best_food_location(npc)