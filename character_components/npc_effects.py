#character_components.npc_effects.py

class TimedEffect:
    def __init__(self, name, duration):
        self.name = name
        self.remaining = duration

    def on_start(self, npc): pass
    def on_tick(self, npc): pass
    def on_end(self, npc): pass

class RecentMealEffect(TimedEffect):
    def __init__(self):
        super().__init__("recent_meal", duration=2)

    def on_start(self, npc):
        npc.effort = max(1, npc.effort - 2)
        npc.concentration = max(1, npc.concentration - 1)

    def on_tick(self, npc):
        pass  # digestion happens implicitly

    def on_end(self, npc):
        npc.effort = min(20, npc.effort + 4)
        npc.concentration = min(20, npc.concentration + 2)
