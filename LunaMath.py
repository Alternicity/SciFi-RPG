#LunaMath
import math


class FractalRoot:
    def __init__(self, x):
        self.original = x
        self.root10 = math.sqrt(10)
        self.upper = math.sqrt(x * 10)
        self.lower = self.upper / self.root10

    def pair(self):
        return (self.upper, self.lower)

    def product(self):
        return self.upper * self.lower

# Example
froot = FractalRoot(5)
from visual_effects import loading_bar, GREEN, color_text
print(f"[FUTURE] {color_text('Hi from Luna!', GREEN)}")

print(froot.pair())     # (~7.071, ~0.707)
print(froot.product())  # Should return 5



# Toggle field visualization on/off
RUN_TEMP_FIELD = False

if RUN_TEMP_FIELD:
    import numpy as np
    import matplotlib.pyplot as plt



# Define a scalar field function: e.g., temperature over 2D space
def temperature_field(x, y):
    return np.sin(x) * np.cos(y)

    # Create a grid of points
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)

    # Evaluate the scalar field over the grid
    Z = temperature_field(X, Y)

    # Plot the scalar field
    plt.contourf(X, Y, Z, levels=50, cmap='plasma')
    plt.colorbar(label='Temperature')
    plt.title("2D Scalar Field: Temperature")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
