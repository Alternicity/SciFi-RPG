#anchors.eat_anchor.py
from 

class EatAnchor(Anchor):#but, Anchor is not defined here
    def resolve_target_location(self):
        npc = self.owner
        return npc.mind.memory.semantic.best_food_location()