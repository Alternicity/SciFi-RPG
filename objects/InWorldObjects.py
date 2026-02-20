#objects.InWorldObjects.py
from dataclasses import field
import uuid
from enum import Enum
from perception.perceptibility import PerceptibleMixin
from typing import Dict

# Enums for toughness and size
class Toughness(Enum):
    FRAGILE = "fragile"
    NORMAL = "normal"
    DURABLE = "durable"


class Size(Enum):
    POCKET_SIZED = "pocket_sized"
    ONE_HANDED = "one-handed"
    TWO_HANDED = "two_handed"
    HEAVY = "heavy"
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class ItemType(Enum): 
    WEAPON = "Weapon"
    GADGET = "Gadget"
    ARMOR = "Armor"
    MEDKIT = "Medkit"
    FURNITURE = "Furniture"
    CONTAINER = "Container"
    FOOD = "Food"
    DRINK = "Drink"
    PLANT ="Plant"


# NOTE: The `item_type` attribute is only defined in concrete classes 
# that directly instantiate objects (e.g., Pistol, Knife). 
# Abstract classes like Weapon and RangedWeapon do not include `item_type`, 
# as they are not used to create objects directly. 
# This ensures clarity and avoids redundancy while adhering to OOP principles.

valid_items = [
    "CashWad", "Wallet", "HardDrive", "Medkit", 
    "FoodCrate", "Laptop", "MechanicalToolkit", "ElectricalToolkit", 
    "PowerGenerator", "WaterPurifier", "SmartPhone", "CommoditiesBox"
] 

# Base class for all objects in the world
class ObjectInWorld(PerceptibleMixin):#Ultimate base class
    is_concrete = False  # Abstract base

    placement_quality: str = "neutral"  # options: "perfect", "neutral", "poor"

    def __init__(self, name, toughness, item_type, size, blackmarket_value,
                 price=0, damage_points=None, legality=True, quantity=1, **kwargs):
        super().__init__()

        if not isinstance(toughness, Toughness):
            raise TypeError(f"{name} initialized with invalid toughness: {toughness}")

        if not isinstance(size, Size):
            raise TypeError(f"{name} initialized with invalid size: {size}")

        if not isinstance(item_type, ItemType):
            raise TypeError(f"{name} initialized with invalid item_type: {item_type}")


        self.name = name
        self.base_ambience = {}
        self.toughness = toughness
        self.item_type = item_type
        self.size = size
        self.blackmarket_value = blackmarket_value
        self.price = price
        self.damage_points = damage_points
        self.legality = legality
        self.owner = None
        self.quantity = quantity
        self.bloodstained = None  # Can be a character reference or ID string
        self.is_stolen =False

    @property
    def tags(self):
        return []
    
    def has_tag(self, tag: str) -> bool:
        return tag in self.tags
    
    def has_tags(self, required_tags: list[str]) -> bool:
        return all(tag in self.tags for tag in required_tags)

    def clone(self):
        """Return a new item with identical data but preserved class type."""
        new_item = type(self).__new__(type(self))
        new_item.__dict__.update(self.__dict__.copy())
        return new_item

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "item_type": self.item_type,
            "description": f"{self.name}",
            "region": getattr(getattr(self, "region", None), "name", None),
            "location": getattr(getattr(self, "location", None), "name", None),
            "sublocation": getattr(getattr(self, "sublocation", None), "name", None),
            "origin": self,
            "salience": self.compute_salience(observer),  # Using anchor-based salience now
            "tags": getattr(self, "tags", []),
            "urgency": getattr(self, "urgency", 1),
            "weight": self.percept_weight(observer),
            "source": None,
            "suggested_actions": self.get_suggested_actions(observer),
            "security": getattr(self, "security_level", 0),
            "has_security": self.has_security(),
            "bloodstained": self.bloodstained,
            "owner": self.owner,
            "price": self.price,
            "quantity": self.quantity,
            "toughness": self.toughness.value if isinstance(self.toughness, Enum) else str(self.toughness),
            "size": self.size.value if isinstance(self.size, Enum) else str(self.size),
            "details": f"{self.name} ({self.item_type.value})"
        }


    def modulated_ambience(self) -> Dict[str, float]:
        modifier = {"perfect": 1.2, "neutral": 1.0, "poor": 0.7}.get(self.placement_quality, 1.0)
        return {k: v * modifier for k, v in self.base_ambience.items()}
    
#It's probably cleaner and safer if all items that go in inventory have quantity by default (even if quantity=1 for weapons).



class Item:
    def __init__(self, name, price, size, quantity=1, category=None, description=""):
        self.name = name
        self.price = price
        self.quantity = quantity  # Support for stackable items
        self.category = category
        self.description = description
        self.size = size
    def __repr__(self):
        return f"{self.name} (${self.price}) x{self.quantity}"


class CashWad(ObjectInWorld): #REMOVE ALL VALUE
    is_concrete = True
    def __init__(self, amount):
        super().__init__(
            name="Cash Wad",
            toughness="Fragile",
            item_type="currency",
            damage_points=3,
            legality=True,
            price=amount,  # standardized on 'price'
            blackmarket_value=amount,
            size="Pocket Sized"
        )
        self.amount = amount  # optional but helpful

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"

        }

    def get_value(self):
        """Return the value of the CashWad.
        A CashWad in an in game object that is a quantity of money"""
        return self.value

    def add_to_wallet(self, wallet):
        """Add the value of the CashWad to the wallet."""
        wallet.add_cash(self.price)
        print(f"Added {self.price} cash from CashWad to wallet.")
        self.price = 0  # mark as spent

class Wallet:
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, cash=0, bankCardCash=0):
        self.cash = cash  # Cash for normal purchases (or black market)
        self.bankCardCash = bankCardCash  # Cash available via bank card

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }

    @property
    def balance(self):
        return self.cash + self.bankCardCash

    @balance.setter
    def balance(self, value):
        # Optional: split evenly, or just dump it all into cash
        self.cash = value

    def get_values(self):
        return self.cash, self.bankCardCash

    def add_cash(self, amount):
        """Add cash to the wallet."""
        self.cash += amount

    def add_bankCardCash(self, amount):
        """Add money to the bank card balance."""
        self.bankCardCash += amount

    def spend_cash(self, amount):
        """Spend cash, return True if successful, False if not enough."""
        if self.cash >= amount:
            self.cash -= amount
            return True
        return False

    def spend_bank(self, amount):
        if self.bankCardCash >= amount:
            self.bankCardCash -= amount
            return True
        return False

    """ def spend_bankCardCash(self, price):
        Spend bank card cash, return True if successful, False if not enough.
        if self.bankCardCash >= price:
            self.bankCardCash -= price
            return True
        return False """
        #marked for deletion.characters spend money, not wallets

class HardDrive(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, sensitivity):
        super().__init__(
            name="Hard Drive",
            toughness=Toughness.FRAGILE,
            damage_points=2,
            legality=True,
            value=50,
            blackmarket_value=50,
            size=Size.POCKET_SIZED,
        )
        self.sensitivity = sensitivity

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }

class Medkit(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name=Medkit,
            toughness=Toughness.FRAGILE,
            value=50,
            item_type=ItemType.GADGET  # This is correct for now
        )
        self.legality = True  # Define legality here
        self.damage_points = 2  # Assign to the instance
        self.blackmarket_value=50,
        self.size=Size.POCKET_SIZED,
        
    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }

class AdvancedMedkit(Medkit):
    def __init__(self):
        super().__init__()
        self.contains_xyz = True

    def _postprocess_percept(self, data, observer):
        if self.contains_xyz:
            data["tags"] = data.get("tags", []) + ["useful"]
            data["description"] = "Good to have when youre injured."
        return data


class FoodCrate(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name="Food Crate",
            toughness=Toughness.NORMAL,
            damage_points=3,
            legality=True,
            value=10,
            blackmarket_value=10,
            size=Size.TWO_HANDED,
        )

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }
    
class Laptop(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, sensitivity):
        super().__init__(
            name="Laptop",
            toughness=Toughness.FRAGILE,
            damage_points=3,
            legality=True,
            value=500,
            blackmarket_value=500,
            size=Size.TWO_HANDED,
        )
        self.sensitivity = sensitivity

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }
    
class MechanicalToolkit(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name="Mechanical Toolkit",
            toughness=Toughness.DURABLE,
            damage_points=25,
            legality=True,
            value=100,
            blackmarket_value=100,
            size=Size.TWO_HANDED,
        )

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }
    
class ElectricalToolkit(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name="Electrical Toolkit",
            toughness=Toughness.NORMAL,
            damage_points=5,
            legality=True,
            value=100,
            blackmarket_value=100,
            size=Size.POCKET_SIZED,
        )

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }
    
class PowerGenerator(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name="Power Generator",
            toughness=Toughness.DURABLE,
            damage_points=45,
            legality=True,
            value=500,
            blackmarket_value=300,
            size=Size.TWO_HANDED,
        )
    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }
    
class WaterPurifier(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name="Water Purifier",
            toughness=Toughness.DURABLE,
            damage_points=35,
            legality=True,
            value=150,
            blackmarket_value=150,
            size=Size.TWO_HANDED,
        )
    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }
    
class SmartPhone(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, price=200, quantity=1,):
        super().__init__(
            name="SmartPhone",
            toughness=Toughness.FRAGILE,
            damage_points=15,
            legality=True,
            item_type=ItemType.GADGET,
            blackmarket_value=50,
            price=price,
            size=Size.POCKET_SIZED,
        )
        self.quantity = quantity
        self.owner = None
        self.human_readable_id = "Unowned SmartPhone"

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "tags": self.tags,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }
    
    @property
    def tags(self):
        return ["electronic", "smartphone", "gadget"]

class CommoditiesBox(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name="Commodities Box",
            toughness=Toughness.NORMAL,
            damage_points=25,
            legality=True,
            value=200,
            blackmarket_value=200,
            size=Size.TWO_HANDED,
        )

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "item_type": self.item_type,
            "description": f"{self.name} ({self.item_type})"
            
        }

class CashRegister(ObjectInWorld):
    def __init__(self,  name, toughness, item_type, size, blackmarket_value, initial_cash=300):
        super().__init__(name, toughness, item_type, size, blackmarket_value)
        self.cash = initial_cash

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "origin": self,
            "tags": self.tags,
            "item_type": self.item_type,
            "description": self.name
            
        }

    @property
    def tags(self):
        return ["cash", "econonmic"]

    def deposit(self, amount):
        self.cash += amount

    def withdraw(self, amount):
        actual = min(self.cash, amount)
        self.cash -= actual
        return actual

    def create_cashwad(self):
        taken = self.withdraw(self.cash)
        return CashWad(taken)

class Container:
    def __init__(self, *, is_open=True, is_transparent=False):
        self.contents = []
        self.is_open = is_open
        self.is_transparent = is_transparent

    def visible_contents(self, observer=None):
        if self.is_open or self.is_transparent:
            return self.contents
        
    def add(self, item):
        self.contents.append(item)

    def remove(self, item):
        if item in self.contents:
            self.contents.remove(item)

    def list_items(self):
        return self.contents


class ToyBox(Container):
    def __repr__(self):
        return f"ToyBox({len(self.contents)} bricks)"


class MarbleBag(Container):
    def __repr__(self):
        return f"MarbleBag({len(self.inventory)} marbles)"

    # 💸 MONEY VARIABLE NAMING CONVENTION (Standardized for RPG Project)
#
# 🧱 CORE VARIABLES (Used throughout codebase):
#
# - `cash`: Physical cash held by a character (e.g., in wallet, cash register, CashWad).
# - `bankCardCash`: Virtual or digital cash accessible via bank card. Stored in Wallet.
#
# 📦 OBJECT-BASED MONEY:
#
# - `price`: Standard monetary value of an item or object. Used for trade/barter, store pricing.
# - `CashWad`: An object that *represents* a physical amount of `cash`. Stores value in `.price`.
#
# ❌ Avoid using `value` for monetary purposes — use `.price` instead.
#    If legacy code uses `.value` for money, convert it to `.price`, or assign:
#       `price = cashwad.value`
#    to maintain compatibility.
#
# 🧠 GUIDANCE:
# - In Wallet and other currency systems, always use `cash` and `bankCardCash`.
# - In trade/store systems and cash objects (CashWad, items), always use `price`.
# - If needed, alias temporarily for compatibility, but avoid mixing terms in the same scope.
#
# 📌 Example Usage:
#   wallet.add_cash(cashwad.price)     ✅
#   item.price = 250                   ✅
#   if wallet.cash >= item.price:     ✅
#
# 💡 Reminder:
# Keep it simple, searchable, and semantically clear to make the economy system easier to expand and debug.

class Vase(ObjectInWorld, Container):
    is_concrete = True

    def __init__(self, material="ceramic", placement_quality="perfect", quantity=1):
        ObjectInWorld.__init__(
            self,
            name=f"{material.title()} Vase",
            toughness=Toughness.FRAGILE,
            item_type=ItemType.CONTAINER,
            size=Size.MEDIUM,
            blackmarket_value=5,
            price=10,
            legality=True,
            quantity=quantity,
        )
        Container.__init__(self)

        self.material = material
        self.placement_quality = placement_quality
        self.base_ambience = {
            "peace": 0.2,
            "order": 0.1,
            "aesthetic": 0.3,
        }
        self.symbolism = ["grace", "containment", "ritual"]

    def compute_ambience_from_contents(self):
        ambience = self.base_ambience.copy()
        for item in self.inventory:
            if hasattr(item, "modulated_ambience"):
                for k, v in item.modulated_ambience().items():
                    ambience[k] = ambience.get(k, 0) + v
        return ambience

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        base.update({
            "description": f"{self.material.title()} Vase with {len(self.inventory)} item(s)",
            "tags": ["decor", "vessel", "peaceful", "container"],
            "contents": [item.name for item in self.inventory]
        })
        return base

    def __repr__(self):
        return f"<{self.name}: holds {len(self.inventory)} items>"

class Pot(ObjectInWorld, Container):
    is_concrete = True

    def __init__(self, material="ceramic", placement_quality="neutral", quantity=1):
        ObjectInWorld.__init__(
            self,
            name=f"{material.title()} Pot",
            toughness=Toughness.DURABLE if material == "ceramic" else Toughness.FRAGILE,
            item_type=ItemType.CONTAINER,
            size=Size.SMALL,
            blackmarket_value=3,
            price=8,
            legality=True,
            quantity=quantity,
        )
        Container.__init__(self)

        self.material = material
        self.placement_quality = placement_quality
        self.base_ambience = {
            "earth": 0.2,
            "rootedness": 0.2,
        }

        self.symbolism = []
        if material == "ceramic":
            self.symbolism.append("rustic")

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)#line 647
        visible = self.visible_contents(observer)

        if len(visible) == 1:
            item = visible[0]
            base["description"] = f"{item.name} in a {self.material} pot"
            base["primary"] = item
            base["secondary"] = self
        else:
            base["description"] = f"{self.material.title()} Pot"

        base["tags"] = ["container", "natural", "earthy"]
        base["symbolism"] = self.symbolism

        return base

class Statue(ObjectInWorld):
    is_concrete = True

    def __init__(self, material="stone", theme="contemplation"):
        super().__init__(
            name=f"{material.title()} Statue",
            toughness=Toughness.DURABLE,
            item_type="decor",
            size=Size.LARGE,
            blackmarket_value=150,
            price=200,
            legality=True
        )
        self.theme = theme
        self.symbolism = ["stillness", "legacy", theme]
        #"stillness" and "legacy" are literal strings, while theme is a variable that holds a string
        """ So, if theme = "contemplation", then the full list becomes:
        ["stillness", "legacy", "contemplation"] """
        
        self.base_ambience = {
            "contemplation": 0.4,
            "stillness": 0.3
        }

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        base.update({
            "tags": ["decor", "symbolic", "contemplative"],
            "theme": self.theme,
            "symbolism": self.symbolism
        })
        return base

class Lamp(ObjectInWorld):
    is_concrete = True

    def __init__(self, color="warm_white", intensity=0.5):
        super().__init__(
            name=f"{color.replace('_', ' ').title()} Lamp",
            toughness=Toughness.FRAGILE,
            item_type="light",
            size=Size.MEDIUM,
            blackmarket_value=20,
            price=40,
            legality=True
        )
        self.color = color
        self.intensity = intensity
        self.base_ambience = {
            "warmth": 0.2 * intensity,
            "safety": 0.1 * intensity
        }

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        base.update({
            "tags": ["light", "comfort"],
            "color": self.color
        })
        return base
    
class ColoredLightingArray(ObjectInWorld):
    is_concrete = True

    def __init__(self, scheme="sunset"):
        super().__init__(
            name=f"{scheme.title()} Light Array",
            toughness=Toughness.FRAGILE,
            item_type="light",
            size=Size.MEDIUM,
            blackmarket_value=40,
            price=70,
            legality=True
        )
        self.scheme = scheme
        self.base_ambience = {
            "aesthetic": 0.3,
            "emotion": 0.2 if scheme == "sunset" else 0.1
        }

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        base.update({
            "tags": ["light", "decor", "emotion"],
            "scheme": self.scheme
        })
        return base

