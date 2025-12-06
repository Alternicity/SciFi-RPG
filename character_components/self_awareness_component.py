
from base.self_awareness_levels import SelfAwarenessLevel

class SelfAwarenessComponent:
    def __init__(self, owner):
        self.owner = owner
        self.score = 0
        self.level = SelfAwarenessLevel.ANIMAL

    def calculate(self):
        o = self.owner
        score = 0

        # Safely access memory capacity
        # Could be int, list, or object depending on your system
        if hasattr(o, "mind") and hasattr(o.mind, "memory"):
            score += (len(o.mind.memory.capacity) * 0.5)

        if hasattr(o, "psy"):
            score += o.psy * 0.75

        if hasattr(o, "has_autonomous_goals") and o.has_autonomous_goals():
            score += 2
        if hasattr(o, "detects_pattern_glitches") and o.detects_pattern_glitches():
            score += 1.5
        if hasattr(o, "reflects_on_failures") and o.reflects_on_failures():
            score += 1

        self.score = round(score, 2)
        self._update_level()

    def _update_level(self):
        s = self.score

        if s < 2:
            self.level = SelfAwarenessLevel.ANIMAL
        elif s < 4:
            self.level = SelfAwarenessLevel.BASIC
        elif s < 6:
            self.level = SelfAwarenessLevel.PERSONAL
        elif s < 8:
            self.level = SelfAwarenessLevel.REFLECTIVE
        elif s < 10:
            self.level = SelfAwarenessLevel.META
        else:
            self.level = SelfAwarenessLevel.TRANSCENDENT
