#character_components.npc_effects.py
from debug_utils import debug_print
from character_thought import Thought

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
        debug_print(
            npc,
            f"[EFFECT] RecentMealEffect started: {npc.name} effort -2, concentration -1",
            category="effect"
        )

    def on_tick(self, npc):

        npc.effort = min(20, npc.effort + 1)

        debug_print(
            npc,
            f"[EFFORT] +1 digestion recovery → {npc.effort}",
            category="effect"
        )
        debug_print(
            npc,
            f"[DIGESTION] concentration steady → {npc.concentration}",#maybe call this something else, the ALLCAPS bit
            category="effect"
        )
        
    def on_end(self, npc):
        npc.effort = min(20, npc.effort + 4)
        npc.concentration = min(20, npc.concentration + 2)
        
        npc.mind.memory.add_episodic(
            subject=npc,
            verb="finished_meal",
            object_=npc.location.name,
            importance=1
        )
        npc.mind.add_thought(#should this use a mind function rather than append?
            Thought(
                subject=npc.location,
                content="Time to leave",
                tags=["leave_location"],
                urgency=5
            )
        )
        debug_print(
            npc,
            "[EFFECT] RecentMealEffect ended",
            category="effect"
        )

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

class MorningSettlingEffect(TimedEffect):
    def __init__(self):
        super().__init__("morning_settling", duration=1)

    def on_start(self, npc):
        debug_print(
            npc,
            "[LIBERTY] Morning settling — staying home this tick.",
            category="liberty"
        )

    def on_tick(self, npc):
        # No stat changes — purely behavioral gate
        pass

    def on_end(self, npc):
        debug_print(
            npc,
            "[LIBERTY] Morning settling complete.",
            category="liberty"
        )