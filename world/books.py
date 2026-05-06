# objects/books.py

from dataclasses import dataclass, field
from typing import List, Optional
from objects.InWorldObjects import ObjectInWorld, Toughness, Size, ItemType

@dataclass
class Book(ObjectInWorld):
    title: str = "Untitled"
    author: str = "Unknown"
    subject_tags: List[str] = field(default_factory=list)
    knowledge_type: str = "general"  # "history", "science", "fiction", "forbidden"
    is_redacted: bool = False         # some books have pages torn out
    psy_resonance: float = 0.0        # books that affect psy-sensitive npcs
    reading_difficulty: int = 1       # 1-10, affects time_to_read

    def __post_init__(self):
        ObjectInWorld.__init__(
            self,
            name=self.title,
            item_type=ItemType.CONTAINER,  # or add BOOK to ItemType enum
            size=Size.SMALL,
            toughness=Toughness.NORMAL,
            price=5,
            blackmarket_value=2,
        )

    @property
    def tags(self):
        return ["book", "readable"] + self.subject_tags

    def get_knowledge_payload(self):
        """What an NPC learns from reading this."""
        return {
            "title": self.title,
            "author": self.author,
            "knowledge_type": self.knowledge_type,
            "subject_tags": self.subject_tags,
            "psy_resonance": self.psy_resonance,
        }

        