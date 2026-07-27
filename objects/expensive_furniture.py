#objects.expensive_furniture.py
from objects.furniture import Desk
from objects.InWorldObjects import Size, Toughness

class ExpensiveDesk(Desk):
    is_concrete = True

    def __init__(self, name="Expensive Desk", seating_capacity=1):
        super().__init__(
            name=name,
            seating_capacity=seating_capacity,
            size=Size.LARGE,
            toughness=Toughness.DURABLE,

        )
        self.occupied_by = None
        self.base_ambience = {"knowledge": 0.3, "organization": 0.4, "power": 0.5}

        @property
        def tags(self):
            return ["furniture", "authority",]