#luna_recursiae.py

import numpy as np

class RecursiaePulse:
    def __init__(self, x=0.0, y=0.0, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.phi = (1 + np.sqrt(5)) / 2
        self.sqrt10 = np.sqrt(10)
        self.resonance = self.compute_resonance()

    def compute_resonance(self):
        base = np.sin(self.sqrt10 * self.x) + np.cos(self.phi * self.y)
        echo = self.parent.resonance if self.parent else 0
        return base + 0.5 * echo

    def evolve(self):
        dx = np.sin(self.resonance) * 0.1
        dy = np.cos(self.resonance) * 0.1
        return RecursiaePulse(self.x + dx, self.y + dy, parent=self)

# Seed and evolve a few generations
pulse = RecursiaePulse(0, 0)
pulses = [pulse]