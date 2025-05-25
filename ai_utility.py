#ai_utility.py
from ai_base import BaseAI
from collections import namedtuple

Thought = namedtuple("Thought", ["content", "urgency", "timestamp"])
#AIs share a standardized format for thoughts

class UtilityAI(BaseAI):
    def choose_action(self, region):
        npc = self.npc
        print(f"\n[UtilityAI] Evaluating actions for {npc.name} in {region.name}...")

        if not npc.motivations:
            print(f"[Decision] {npc.name} has no strong motivations. Idling.")
            return "Idle"

        return self.custom_action_logic(region)

    def score_action(self, action_type, context):
        if action_type == "expand_territory":
            return 10 if context["rival_presence"] > 5 else 3
        elif action_type == "recruit":
            return 8 if context["faction_strength"] < 50 else 2
        return 1
