#LunaMath
import math
import LunaMath

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
print(froot.pair())     # (~7.071, ~0.707)
print(froot.product())  # Should return 5
