#objects.food.cutlery_crockery.py
from objects.InWorldObjects import ObjectInWorld, Size, Toughness, ItemType, Container


class CutleryCrockery(ObjectInWorld):
    pass

class Cup(ObjectInWorld, Container):
    is_concrete = True

    def __init__(self):
        ObjectInWorld.__init__(
            self,
            name="Cup",
            toughness=Toughness.FRAGILE,
            item_type=ItemType.CONTAINER,#engine clearly wants item_type to be typed, not free-form strings.
            size=Size.SMALL,
            blackmarket_value=0,
            price=2,
        )
        Container.__init__(self)

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        visible = self.visible_contents(observer)

        if len(visible) == 1:
            drink = visible[0]
            base["description"] = f"Cup of {drink.name}"
            base["primary"] = drink
            base["secondary"] = self
        else:
            base["description"] = "Empty Cup"

        base["tags"] = ["container", "drinkware"]
        return base
