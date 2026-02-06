#ai_goap.py
from ai_base import BaseAI

class GOAPAI(BaseAI):
    def plan(self): pass
    def act(self): pass

class StrategicAI(GOAPAI):
    def decide(self):
        if self.motivation_to_plan > 0.8:
            self.plan()
        else:
            self.utility_ai.decide()