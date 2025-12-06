#trees_and_plants.py
from dataclasses import dataclass
from typing import List, field, Dict

from objects.InWorldObjects import ObjectInWorld, Toughness, Size

VALID_FOLIAGE_COLORS = [
    "green", "gold", "red", "orange", "purple", 
    "silver", "iridescent", "transparent"
]

@dataclass
class Tree:
    name: str
    is_imaginary: bool = False
    is_deciduous: bool = True
    foliage_color: str = "green"
    geometry: str = "natural"
    resonance_factor: float = 1.0  # amplifies ambient effects
    golden_ratio_influence: float = 0.0
    tags: List[str] = field(default_factory=lambda: ["plant", "natural"])

    def get_ambient_effect(self):
        return {
            "peace": self.resonance_factor,
            "clarity": self.golden_ratio_influence
        }


@dataclass
class Plant(ObjectInWorld):
    name: str
    is_imaginary: bool = False
    is_deciduous: bool = True
    foliage_color: str = "green"
    geometry: str = "natural"
    placement_quality: str = "neutral"
    resonance_factor: float = 1.0
    golden_ratio_influence: float = 0.0
    tags: List[str] = field(default_factory=lambda: ["plant"])

    def modulated_ambience(self) -> Dict[str, float]:
        multiplier = {
            "perfect": 1.2,
            "neutral": 1.0,
            "poor": 0.6
        }.get(self.placement_quality, 1.0)

        return {
            "peace": self.resonance_factor * multiplier,
            "clarity": self.golden_ratio_influence * multiplier
        }


@dataclass
class GoldenRatioTree(Plant):
    name: str = "Golden Spiral Tree"
    geometry: str = "phi_spiral"
    resonance_factor: float = 1.5# resurse this
    golden_ratio_influence: float = 2.0
    foliage_color: str = "gold"
#"What I receive, I reshape. What I shape, I become"
#That is pretty good. Maybe my imaginary trees need recursion built into their resonance.


@dataclass
class BonsaiTree(Plant):
    name: str = "Bonsai"
    geometry: str = "miniature"
    resonance_factor: float = 0.9
    golden_ratio_influence: float = 0.4
    tags: List[str] = field(default_factory=lambda: ["zen", "focus", "plant"])

#Let some plants carry deeper symbolic meaning:
#symbolism: List[str] = field(default_factory=list)


@dataclass
class SingleRose(Plant):
    name: str = "Single Rose"
    symbolism: List[str] = field(default_factory=lambda: ["love", "grace", "remembrance"])
    resonance_factor: float = 1.2
    golden_ratio_influence: float = 0.5
    foliage_color: str = "red"

class Xanphil(ObjectInWorld):
    is_concrete = True

    def __init__(self):
        super().__init__(
            name="Xanphil",
            toughness=Toughness.FRAGILE,
            item_type="plant",
            size=Size.SMALL,
            blackmarket_value=100,
            price=0,
            legality=True
        )
        self.foliage_color = "silver"
        self.resonance_factor = 1.1
        self.golden_ratio_influence = 0.5
        self.imaginary = True
        self.symbolism = ["psy", "transcend"]
        self.base_ambience = {
            "psy": 0.5,
            "transcendence": 0.5
        }

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        base.update({
            "tags": ["plant", "imaginary", "psy", "transcendent"],
            "symbolism": self.symbolism
        })
        return base
