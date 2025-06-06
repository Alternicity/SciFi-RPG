from dataclasses import field
import uuid
from enum import Enum
from perceptibility import PerceptibleMixin

#all references to "value" must be replaced with "value"
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

class ItemType(Enum):
    WEAPON = "Weapon"
    GADGET = "Gadget"
    ARMOR = "Armor"
    MEDKIT = "Medkit"

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
class ObjectInWorld(PerceptibleMixin):
    is_concrete = False  # An abstract class
    def __init__(self, name, toughness, item_type, size, blackmarket_value, price=0, damage_points=None, legality=True,  owner_name=None, **kwargs):
        PerceptibleMixin.__init__(self)

        self.name = name
        self.toughness = toughness
        self.item_type = item_type  # 'weapon', 'armor', etc.
        self.size = size
        self.blackmarket_value = blackmarket_value
        self.price = price
        self.damage_points = damage_points
        self.legality = legality
        #self.item_type = item_type
        #does this need to be here as well?
        self.owner_name = owner_name
        self.bloodstained = None  # Will hold a reference to a Character or a string of name/ID
#It's probably cleaner and safer if all items that go in inventory have quantity by default (even if quantity=1 for weapons).

#only concrete, fully implementable classes have the damage_points
#and legality attributes.
#Any object that represents something that could potentially break or
#degrade over time should have damage_points.

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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
            #"salience": 20 if observer and self.owner == observer else 3
        }

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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
        }

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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
        }
    
class SmartPhone(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, price=200, quantity=1,):
        super().__init__(
            name="SmartPhone",
            toughness=Toughness.FRAGILE,
            damage_points=15,
            legality=True,
            item_type="gadget",
            blackmarket_value=50,
            price=price,
            size=Size.POCKET_SIZED,
        )
        self.quantity = quantity
        self.owner_name = None
        self.human_readable_id = "Unowned SmartPhone"

    def get_percept_data(self, observer=None):
        return {
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
        }
    
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
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
        }

class CashRegister(ObjectInWorld):
    def __init__(self,  name, toughness, item_type, size, blackmarket_value, initial_cash=300):
        super().__init__(name, toughness, item_type, size, blackmarket_value)
        self.cash = initial_cash

    def get_percept_data(self, observer=None):
        return {
            "type": type(self).__name__,
            "name": self.name,
            "item_type": self.item_type,
            "owner": self.owner_name,
            "size": self.size.value if hasattr(self, "size") else None,
            "salience": self.compute_salience(observer)
        }
    
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
    def __init__(self):
        self.inventory = []

    def add(self, item):
        self.inventory.append(item)

    def remove(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def list_items(self):
        return self.inventory


class ToyBox(Container):
    def __repr__(self):
        return f"ToyBox({len(self.inventory)} bricks)"


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
