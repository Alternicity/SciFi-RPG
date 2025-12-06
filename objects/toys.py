#toys.py
from objects.InWorldObjects import ObjectInWorld
from typing import List

class Marble(ObjectInWorld):
    def __init__(self, color: str):
        self.color = color

    def __repr__(self):
        return f"Marble(color={self.color})"


class Brick(ObjectInWorld):
    def __init__(self, color: str):
        self.color = color
        self.connected_to: List['Brick'] = []

    def connect(self, other_brick: 'Brick'):
        if other_brick not in self.connected_to:
            self.connected_to.append(other_brick)
            other_brick.connected_to.append(self)

    def __repr__(self):
        return f"Brick(color={self.color}, connections={len(self.connected_to)})"