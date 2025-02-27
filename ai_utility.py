#ai_utility.py → If using Utility AI, scoring logic goes here.

def score_action(self, action_type, context):
    """Assigns a score to an action based on context."""
    if action_type == "expand_territory":
        return 10 if context["rival_presence"] > 5 else 3
    elif action_type == "recruit":
        return 8 if context["faction_strength"] < 50 else 2
    return 1