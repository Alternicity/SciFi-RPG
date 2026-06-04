# objects.sports_objects.py

from objects.InWorldObjects import ObjectInWorld, Toughness, Size, ItemType
from objects.furniture import Furniture, Table

class Ball(ObjectInWorld):
    """Base class for all balls."""
    def __init__(self, name, size=Size.SMALL, **kwargs):
        super().__init__(
            name=name,
            toughness=Toughness.NORMAL,
            item_type=ItemType.GADGET,
            size=size,
            blackmarket_value=1,
            price=0,
            **kwargs
        )

    @property
    def tags(self):
        return ["ball", "sports", "equipment"]


class PoolBall(Ball):
    def __init__(self, number: int):
        super().__init__(name=f"Pool Ball {number}", size=Size.SMALL)
        self.number = number
        self.base_ambience = {"focus": 0.1}

    @property
    def tags(self):
        return ["ball", "pool", "sports", "equipment"]


class BowlingBall(Ball):
    def __init__(self, weight_kg=4):
        super().__init__(name=f"Bowling Ball ({weight_kg}kg)", size=Size.MEDIUM)
        self.weight_kg = weight_kg

    @property
    def tags(self):
        return ["ball", "bowling", "sports", "equipment"]


class PoolCue(ObjectInWorld):
    def __init__(self):
        super().__init__(
            name="Pool Cue",
            toughness=Toughness.NORMAL,
            item_type=ItemType.GADGET,
            size=Size.TWO_HANDED,
            blackmarket_value=2,
            price=5,
        )

    @property
    def tags(self):
        return ["cue", "pool", "sports", "equipment", "stick"]


class PoolTable(Table):
    is_concrete = True

    def __init__(self, name="Pool Table"):
        super().__init__(
            name=name,
            size=Size.LARGE,
            toughness=Toughness.DURABLE,
            seating_capacity=0,
        )
        self.balls = [PoolBall(i) for i in range(1, 16)]
        self.cues = [PoolCue(), PoolCue()]
        self.in_use_by = []  # list of Characters currently playing
        self.base_ambience = {"focus": 0.2, "fun": 0.3}

    def is_free(self):
        return len(self.in_use_by) == 0

    def occupy(self, npc):
        self.in_use_by.append(npc)

    def vacate(self, npc):
        if npc in self.in_use_by:
            self.in_use_by.remove(npc)

    @property
    def tags(self):
        return ["furniture", "table", "pool", "sports", "fun"]


class BowlingLane(Furniture):
    is_concrete = True

    def __init__(self, lane_number=1):
        super().__init__(
            name=f"Bowling Lane {lane_number}",
            size=Size.LARGE,
            toughness=Toughness.DURABLE,
            seating_capacity=0,
        )
        self.lane_number = lane_number
        self.balls = [BowlingBall(4), BowlingBall(5), BowlingBall(6)]
        self.in_use_by = []
        self.pins_standing = 10
        self.base_ambience = {"fun": 0.4, "social": 0.2}

    def is_free(self):
        return len(self.in_use_by) == 0

    def occupy(self, npc):
        self.in_use_by.append(npc)
        self.pins_standing = 10  # reset on new game

    def vacate(self, npc):
        if npc in self.in_use_by:
            self.in_use_by.remove(npc)

    def roll(self):
        """Simple simulation of a bowl."""
        import random
        pins_hit = random.randint(0, self.pins_standing)
        self.pins_standing -= pins_hit
        return pins_hit

    @property
    def tags(self):
        return ["furniture", "lane", "bowling", "sports", "fun"]

