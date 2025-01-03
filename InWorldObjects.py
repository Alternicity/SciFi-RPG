from enum import Enum

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

# abstract or mid-abstract classes should not directly require 
#specific attributes like damage or damage points. Instead, these attributes
#  should be defined in the concrete classes, which will instantiate objects.

# Base class for all objects in the world
class ObjectInWorld:
    is_concrete = False  # An abstract class
    def __init__(self, name, toughness, value, item_type):
        self.name = name
        self.toughness = toughness
        self.value = value
        self.item_type = item_type  # 'weapon', 'armor', etc.


#only concrete, fully implementable classes have the damage_points
#and legality attributes.
#Any object that represents something that could potentially break or
#degrade over time should have damage_points.

class CashWad(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, value):
        super().__init__(
            name="Cash Wad",
            toughness="Fragile",  # Assuming 'Fragile' is an attribute, you can adjust this
            damage_points=3,
            legality=True,
            value=value,
            blackmarket_value=value,
            size="Pocket Sized"  # Assuming 'Pocket Sized' is a defined Size type
        )
        damage_points=3,
        legality=True,
        
    def get_value(self):
        """Return the value of the CashWad.
        A CashWad in an in game object that is a quantity of money"""
        return self.value

    def add_to_wallet(self, wallet):
        """Add the value of the CashWad to the wallet."""
        wallet.add_cash(self.value)
        print(f"Added {self.value} cash from CashWad to wallet.")
        self.value = 0  # Cash has been transferred to the wallet

class Wallet:
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, cash=0, bank_card_cash=0):
        self.cash = cash  # Cash for normal purchases (or black market)
        self.bank_card_cash = bank_card_cash  # Cash available via bank card

    def total_balance(self):
        """Return the total money in the wallet (cash + bank card balance)."""
        return self.cash + self.bank_card_cash

    def add_cash(self, amount):
        """Add cash to the wallet."""
        self.cash += amount

    def add_bank_card_cash(self, amount):
        """Add money to the bank card balance."""
        self.bank_card_cash += amount

    def spend_cash(self, amount):
        """Spend cash, return True if successful, False if not enough."""
        if self.cash >= amount:
            self.cash -= amount
            return True
        return False

    def spend_bank_card_cash(self, amount):
        """Spend bank card cash, return True if successful, False if not enough."""
        if self.bank_card_cash >= amount:
            self.bank_card_cash -= amount
            return True
        return False


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

class SmartPhone(ObjectInWorld):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        super().__init__(
            name="SmartPhone",
            toughness=Toughness.FRAGILE,
            damage_points=15,
            legality=True,
            value=200,
            blackmarket_value=200,
            size=Size.POCKET_SIZED,
        )

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

