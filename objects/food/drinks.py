#objects.food.drinks.py
from objects.InWorldObjects import ObjectInWorld, Size, Toughness, ItemType
#from character_components.npc_effects import RecentDrinkEffect

class Drink(ObjectInWorld):
    is_concrete = True

    def __init__(self, name="Drink"):
        super().__init__(
            name=name,
            toughness=Toughness.FRAGILE,
            item_type=ItemType.DRINK,
            size=Size.SMALL,
            blackmarket_value=0,
            price=3,
        )

class Coffee(Drink):
    
    def __init__(self):
        super().__init__(name="Coffee")
        self.effect_type = "caffeine_boost"

    def create_effect(self):
        from character_components.npc_effects import EFFECT_REGISTRY
        effect_class = EFFECT_REGISTRY.get(self.effect_type)
        if effect_class:
            return effect_class(source=self)
        return None

    
class Tea(Drink):
    def __init__(self):
        super().__init__(name="Tea")

class Water(Drink):
    def __init__(self):
        super().__init__(name="Water")