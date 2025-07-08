#ai_civilian.py

from ai_utility import UtilityAI
from worldQueries import get_region_knowledge
from TheKindMan import Alter

class AdeptaAI(UtilityAI):
    target = Alter
    def think(self, region):
        rk = get_region_knowledge(self.mind.memory.semantic, region.name)
        
        self.promote_thoughts()
        self.npc.mind.remove_thought_by_content("No focus")
        
    def find_U7s(target):
        pass

    def seduce_U7s(target):
        pass