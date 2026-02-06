#aether.py

from typing import List, Optional, Union, field
from dataclasses import dataclass

from base.character import Character
from dream import Dream

@dataclass
class AethericEntity:
    name: str
    archetype: str
    instantiation_threshold: float = 0.7  # must be dreamt of often or by high-psy dreamers
    manifesting: bool = False

    linked_entities: List["AethericEntity"]
    linked_dreams: List[Dream] = field(default_factory=list)
    cognizant_characters: List["Character"] = field(default_factory=list)

#Luna dreams it enough → It crosses the aether → It becomes real

