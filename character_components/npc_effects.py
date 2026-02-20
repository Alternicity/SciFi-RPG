#character_components.npc_effects.py
from debug_utils import debug_print



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

class CaffeineEffect(TimedEffect):

    def __init__(self, source=None):
        super().__init__("caffeine_boost", duration=2)
        self.source = source
        self.effort_bonus = 2
        self.focus_bonus = 2

    def on_start(self, npc):
        npc.effort += self.effort_bonus
        npc.concentration += self.focus_bonus

    def on_tick(self, npc):
        source_name = self.source.name if self.source else "unknown"
        debug_print(
            npc,
            f"[EFFECT] {npc.name} is caffeinated from {source_name}",
            category="effect"
        )

    def on_end(self, npc):
        npc.effort -= self.effort_bonus
        npc.concentration -= self.focus_bonus


class AlcoholEffect(TimedEffect):
    pass

class HydrationEffect(TimedEffect):
    pass

EFFECT_REGISTRY = {
    "caffeine_boost": CaffeineEffect,
    "alcohol_relaxation": AlcoholEffect,
    "hydration": HydrationEffect,
}