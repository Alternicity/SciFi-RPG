#character_components.npc_effects.py
from debug_utils import debug_print
from character_thought import Thought
from base.posture import Posture
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
        """ if npc.location and "coffee" in getattr(npc.location, "tags", []):
            if not npc.mind.has_thought_with_tag("coffee"):
                thought = Thought(
                    subject="drink",
                    content="A coffee would be nice.",
                    urgency=3,
                    tags=["drink", "coffee", "cafe"]
                )

            npc.mind.add_thought(thought) """
        

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
        
        npc.mind.memory.remember_thing(
            subject=npc.name,
            verb="finished_meal",
            object_=npc.location.name,
            importance=1,
            owner=npc
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

class SleepEffect(TimedEffect):
    
    def __init__(self, duration=3):
        super().__init__("sleeping", duration=duration)

    def on_start(self, npc):
        npc.posture = Posture.LYING
        # Immediate rest bonus
        npc.effort = min(20, npc.effort + 4)
        npc.concentration = min(20, getattr(npc, "concentration", 10) + 2)
        debug_print(
            npc,
            f"[EFFECT] SleepEffect started: {npc.name} lies down, effort +4",
            category="effect"
        )

    def on_tick(self, npc):
        # Gradual recovery each tick
        if self.remaining <= 0:
            return  # already ended, guard against double-tick
        npc.effort = min(20, npc.effort + 2)
        npc.hunger = min(20, npc.hunger + 0.3)  # slow hunger creep overnight
        debug_print(
            npc,
            f"[SLEEP] recovering → effort={npc.effort:.1f}",
            category="effect"
        )


    def on_end(self, npc):
        npc.location_purpose_fulfilled = True
        npc.posture = Posture.STANDING

        # Final recovery burst
        npc.effort = min(20, npc.effort + 3)
        npc.concentration = min(20, getattr(npc, "concentration", 10) + 3)

        # Suppress sleep motivation now that it's satisfied
        npc.motivation_manager.set_urgency("sleep", 0)

        #npc.motivation_manager.suppress("sleep", reason="just_slept", duration=6)

        result = npc.motivation_manager.suppress("sleep", reason="just_slept", duration=6)
        debug_print(npc, f"[SLEEP] Suppressed sleep: {result is not None}", category="sleep")
        # Also briefly suppress have_fun so NPC doesn't immediately run off
        npc.motivation_manager.suppress("have_fun", reason="just_woke", duration=2)

        # Clear bed occupancy
        bed = getattr(npc, "current_bed", None)
        if bed and hasattr(bed, "vacate"):
            bed.vacate()

        npc.mind.memory.remember_thing(
            subject=npc.name,
            verb="woke_up",
            object_=npc.location.name,
            importance=1,
            owner=npc
        )

        debug_print(
            npc,
            f"[EFFECT] SleepEffect ended: {npc.name}, effort={npc.effort:.1f}",
            category="effect"
        )
        motives = [(m.type, m.urgency, m.suppressed) for m in npc.motivation_manager.motivations]
        debug_print(npc, f"[MOTIVES POST-SLEEP] {motives}", category="motive")