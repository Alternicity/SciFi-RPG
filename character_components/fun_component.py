#character_components.fun_component.py

class FunComponent:
    """
    Placeholder for TC3+ fun mechanics.
    """

    def __init__(self, npc):
        self.npc = npc
        self.fun = getattr(npc, "fun", 1)
        self.prefs = getattr(npc, "fun_prefs", {}) or {}

    def wants_fun(self):
        return self.fun < 8

    def resolve_fun_target(self):
        """
        Future:
        - locations
        - people
        - objects
        """
        return None

""" future fun mechanics:

✔ location adds fun
✔ social presence modifies fun
✔ objects contribute
✔ time spent matters
✔ boredom decay exists

But none of that belongs in UtilityAI. """