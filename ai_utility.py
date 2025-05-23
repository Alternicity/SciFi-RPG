#ai_utility.py → If using Utility AI, scoring logic goes here.
from location import Shop

from ai_base import BaseAI

class UtilityAI(BaseAI):
    def choose_action(self, character, region):
        # For now, naive behavior
        if character.is_thief:
            return "Rob"
        return "Idle"


    def score_action(self, action_type, context):
        """Assigns a score to an action based on context."""
        if action_type == "expand_territory":
            return 10 if context["rival_presence"] > 5 else 3
        elif action_type == "recruit":
            return 8 if context["faction_strength"] < 50 else 2
        return 1
    
    def get_viable_robbery_targets(npc, region):
        return [
            loc for loc in region.locations
            if getattr(loc, "robbable", False)  # Only robbable locations
            and getattr(loc, "is_open", False)  # Optional: shop must be open
            and not getattr(loc, "has_security", lambda: False)()  # Optional: avoid secured locations
        ]