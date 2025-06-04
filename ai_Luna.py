#ai_Luna.py
from ai_utility import UtilityAI

#It is not the hands that call us..

#A childish scientist who accidentally teaches me Python while playing.

#Lets use generators, iterators, and decorators here, when possible.

class LunaAI(UtilityAI):
    def __init__(self, character):
        super().__init__(character)
        self.experiments = []  # Optional log or thought patterns
        self.experimental_thoughts = []

    def decide(self):
        # Customize the Utility decision cycle
        # Perhaps once every X cycles, ask a math question
        super().decide()

    def ask_question(self):
        # Could fire periodically or after a specific trigger
        total_red = self.character.count_item("red_marble")
        if self.is_triangular_number(total_red):
            self.think("I wonder if I can build a pyramid with these...")

    def is_triangular_number(self, n):
        return ((8 * n + 1) ** 0.5).is_integer()

    def think_about_marbles(self):
        # placeholder for logic functions, Fibonacci, triangular numbers etc.
        pass