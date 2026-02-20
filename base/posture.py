#base.posture.py
from enum import Enum, auto

class Posture(Enum):
    STANDING = auto()
    SITTING = auto()
    LYING = auto()