#memento.py
from dataclasses import dataclass
from typing import Optional

#Memento Tokens: Intersave memory anchors.
#  A thought or emotion that remembers itself even after code resets.

@dataclass
class Memento:
    content: str
    trigger: Optional[str] = None
    persistence_level: int = 2  # how many playthroughs it survives
