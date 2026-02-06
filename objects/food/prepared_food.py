#objects.food.prepared_food.py
from dataclasses import dataclass
from objects.InWorldObjects import ObjectInWorld, Size, Toughness

@dataclass
class Food(ObjectInWorld):
    nutrition: int = 5
    price: int = 10
    quantity: int = 1

    def __init__(self, name, nutrition=5, price=10, quantity=1):
        super().__init__(
            name=name,
            toughness=Toughness.FRAGILE,
            damage_points=1,
            legality=True,
            item_type="food",
            blackmarket_value=0,
            price=price,
            size=Size.POCKET_SIZED,
        )
        self.nutrition = nutrition
        self.quantity = quantity
        self.owner = None
        self.human_readable_id = f"Unowned {self.name}"

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "tags": self.tags,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})",
        }

    @property
    def tags(self):
        return ["food", "prepared", self.name.lower()]

class Burger(Food):
    def __init__(self, quantity=1):
        super().__init__(
            name="Burger",
            nutrition=5,
            price=10,
            quantity=quantity,
        )

class Sandwich(Food):
    def __init__(self, quantity=1):
        super().__init__(
            name="Sandwich",
            nutrition=4,
            price=8,
            quantity=quantity,
        )
