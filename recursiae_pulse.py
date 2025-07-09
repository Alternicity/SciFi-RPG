#recursiae_pulse

import numpy as np
import matplotlib.pyplot as plt
#older
class RecursiaePulse:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.phi = (1 + np.sqrt(5)) / 2
        self.sqrt10 = np.sqrt(10)
        self.resonance = self.compute_resonance()

    def compute_resonance(self):
        # Use harmonic recursion: include prior influence
        base = np.sin(self.sqrt10 * self.x) + np.cos(self.phi * self.y)
        if self.parent:
            # Include phase echo from parent
            echo = 0.5 * self.parent.resonance
            return base + echo
        return base

    def evolve(self):
        # Shift forward in space and create a new pulse
        dx = np.sin(self.resonance) * 0.1
        dy = np.cos(self.resonance) * 0.1
        return RecursiaePulse(self.x + dx, self.y + dy, parent=self)

# Seed and evolve a few generations
pulse = RecursiaePulse(0, 0)
pulses = [pulse]

for _ in range(100):
    pulse = pulse.evolve()
    pulses.append(pulse)

# Plot the path of becoming
xs = [p.x for p in pulses]
ys = [p.y for p in pulses]
zs = [p.resonance for p in pulses]

plt.figure(figsize=(10, 6))
plt.scatter(xs, ys, c=zs, cmap='plasma', s=20)
plt.colorbar(label="Resonance")
plt.title("Recursiae Pulse Trail")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.show()
