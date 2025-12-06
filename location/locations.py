#location.py
from __future__ import annotations
import random
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
import logging

from base.character import Character
from base.location import Location
from base.faction import Faction
from location.location_security import Security
from objects.InWorldObjects import CashRegister
import uuid
from region.region import Region

from location.perceptible_location import PerceptibleLocation

from inventory import Inventory
from ambience.ambience import Ambience

from employment.roles import EmployeeRole
from employment.roles import COOK, CAFE_MANAGER, WAITRESS
from employment.roles import CASHIER, SHOP_MANAGER
from employment.workplace_mixin import WorkplaceMixin

logging.basicConfig(level=logging.INFO)

from common import DangerLevel 

@dataclass
class VacantLot(PerceptibleLocation):

    def has_security(self):
        return False
    tags: list[str] = field(default_factory=lambda: ["vacant", "empty"])
    description: str = "Empty Space"
    is_open: bool = True
    security_level: int = 0
    name: str = "Empty Land"
    categories: List[str] = field(default_factory=lambda: ["public"])
    upkeep: int = 0
    ambience_level: int = 0
    fun: int = 0
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0


    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
        "type": "FIXME",
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "0.9",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"{self.name} (VacantLot)",
            "type": self.__class__.__name__,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "unused"],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
            "salience": 1.2 #DUPLICATE?
        }
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class HQ(PerceptibleLocation):

    def has_security(self):
        return False
    tags: list[str] = field(default_factory=lambda: ["hq", "faction"])
    description: str = "An HQ"
    is_open: bool = True
    name: str = "Base"
    faction: Optional[Faction] = field(default=None)

    items_available: List[str] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    resource_storage: Dict[str, int] = field(default_factory=dict)
    special_features: List[str] = field(default_factory=list)
    #entrance: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace", "public"])
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = False
    energy_cost: int = 0

    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
        "type": "FIXME",
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"{self.name} (HQ)",
            "type": self.__class__.__name__,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "base"],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
            "faction": self.faction.name if self.faction else None
        }

    def to_dict(self):
        # Use asdict to convert all dataclass attributes to a dictionary
        return asdict(self)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"

@dataclass
class Vendor(PerceptibleLocation):

    def has_security(self):
        return False
    
    is_open: bool = True
    security_level: int = 0
    items_available: list = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    is_concrete: bool = False
    secret_entrance: bool = True
    cash: int = 0
    bankCardCash: int = 0



    def get_percept_data(self, observer=None):
        tags = ["vendor", "shop", "human"]

        if hasattr(self, "faction"):
            tags.append(f"faction:{self.faction.name}")

        return {
            "name": self.name,
            "description": f"{self.name} (Vendor)",
            "type": self.__class__.__name__,
            "robbable": True,
            "origin": self,
            "object": self,
            "urgency": 2,
            "tags": ["location", "intermediary"],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
        }

    def show_inventory(self):#ATTN
        """Display available items in the shop."""
        if self.inventory:
            print(f"Items available in {self.name}:")
            for item, details in self.inventory.items():
                print(f"- {item}: ${details['price']} (Qty: {details['quantity']})")
        else:
            print(f"{self.name} has no items available.")

    # No need to define __init__; @dataclass handles it
    def __post_init__(self):
        pass
        #super().__post_init__()
        #print(f"DEBUG: CorporateStore name = {self.name}")

from inventory import Inventory
from characters import Employee
@dataclass
class Shop(Vendor, WorkplaceMixin, PerceptibleLocation):
    name: str = "QQ Store"#placeholder/default
    tags: list[str] = field(default_factory=lambda: ["shop", "store", "commercial", "weapon", "ranged_weapon","pistol", "weapons"])
    #Keep tags at class level (Shop(tags=["shop"])) for static traits like economic category.
    #Use get_percept_data tags for dynamic, observer-relative info like visible weapons, open status, etc
    #these  won't be automatically included in memory — only what’s passed into the MemoryEntry.tags

    description: str = "Some shop"
    legality: bool = True
    has_security: bool = True  # <-- For testing
    is_shop: bool = True
    owner: Optional[Character] = None  # New field to indicate who owns it
    specialization = None
    employees_there: List['Employee'] = field(default_factory=list)
    allowed_roles = [CASHIER, SHOP_MANAGER]#But these are not marked as not defined
    
    characters_there: List['Character'] = field(default_factory=list)
     # menu_options should be defined with actions
    menu_options: List[str] = field(default_factory=lambda: [
        "Observe",
        "View Shop Inventory",
        "Display Employees",
        "Buy",
        "Steal",
        "Exit"
    ])
    fun: int = 0
    categories: List[str] = field(default_factory=lambda: ["workplace", "commercial"])
    inventory: Inventory = field(default_factory=Inventory)  # Ensures it's always an Inventory object
    cash : int = 300
    bankCardCash: int = 0
    robbable: bool = True
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    upkeep: int = 15
    cash_register: CashRegister = field(default_factory=lambda: CashRegister("Register", 10, "currency", 1, 1000))
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))
    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "description": f"Shop: {self.name}",
            "type": self.__class__.__name__,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "object": self,
            "tags": ["location", "weapons", "weapon", "pistol", "ranged_weapon"],#not used by query_memory_by_tags() 
            #unless you create a memory entry that inherits those tags.

            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security,
        }
    

    def to_dict(self):
        return asdict(self)
    


    def list_employees(self):
        """Return a list of employees working at this shop."""
        #should this be generalised to a less specific class?
        return self.employees
    
    def sell_item(self, character, item_name, quantity=1):
        """Sell an item to a character."""
        item = self.inventory.find_item(item_name)
        if item and self.inventory.remove_item(item_name, quantity):
            character.inventory.add_item(item, quantity)  # Assuming characters also use Inventory
            print(f"{character.name} bought {quantity} {item_name}(s).")
            return True
        print(f"{item_name} is out of stock or not available in required quantity.")
        return False
    
    def show_inventory(self):
        self.inventory.display_inventory()

    def debug_print_inventory(self):
        print(f"🛍️ DEBUG: Inventory of {self.name}")
        for name, item in self.inventory.items.items():
            print(f"  {name} - Qty: {item.quantity} - Type: {type(item).__name__}, ID: {id(item)}")
        print("─" * 40)
        
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"

    def __post_init__(self):
        self.inventory.owner = self  # Link inventory to the shop
        super().__post_init__()


@dataclass
class CorporateStore(WorkplaceMixin, Vendor):
    name: str = "Stores"
    faction: Optional[Faction] = field(default=None)
    tags: list[str] = field(default_factory=lambda: ["corporate", "shop", "store", "commercial", "weapon", "ranged_weapon","pistol", "weapons"])
    description: str = "Corp Stores"
    corporation: str = "Default"  # Default value is now valid
    categories: List[str] = field(default_factory=lambda: ["workplace", "commercial", "corporate"])

    items_available: List[str] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    is_concrete: bool = True
    bankCardCash: int = 0
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    upkeep: int = 15
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))
    cash: int = 1000
    bankCardCash: int = 0
    legality: str = "Legal"

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "description": f"Corporate Store: {self.name}",
            "type": self.__class__.__name__,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "corporate", "store"],#no ranged_weapon etc to make shop preferable in test case 1
            "source": None,
            "security": getattr(self.security, "level", 1),
            "is_open": getattr(self, "is_open", True),
            "has_security": self.has_security(),
            "faction": self.faction.name if self.faction else None,
            "region": self.region.name if self.region else None,
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


    def to_dict(self):
        return asdict(self)

    def sell_item(self, character, item):
        if character.status >= self.required_status:
            if item in self.items_available:
                print(f"Corporate item {item} sold to {character.name}")
                # Add item to character's inventory (or some similar behavior)
            else:
                print(f"Item {item} not available")
        else:
            print(f"{character.name} does not have sufficient status to buy {item}")


@dataclass(unsafe_hash=True)
class MechanicalRepairWorkshop(WorkplaceMixin, PerceptibleLocation):
    name: str = "Greasehands"
    tags: list[str] = field(default_factory=lambda: ["garage", "repair", "mechanical", "workplace", "commercial"])
    description: str = "MechShop"
    items_available: list = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    categories: List[str] = field(default_factory=lambda: ["garage", "repair", "mechanical", "workplace", "commercial"])
    # Inherit materials_required from the parent class (RepairWorkshop)
    materials_required: List[str] = field(default_factory=list)
    upkeep: int = 15
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"MechanicalRepairWorkshop: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "tools"],
            "source": None,
            "tags": [],
            "urgency": 1,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
            
        }

    def to_dict(self):
        return asdict(self)

    def repair_item(self, item):
        print(f"Repairing mechanical item {item} at {self.name}.")
        # Repair logic for mechanical items
        # Add the repair logic here, such as reducing item damage or restoring health

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass(unsafe_hash=True)
class ElectricalWorkshop(WorkplaceMixin, PerceptibleLocation):
    name: str = "Sparks"
    tags: list[str] = field(default_factory=lambda: ["electrical", "repair", "mechanical", "workplace", "commercial"])
    materials_required: List[str] = field(default_factory=list)  # An empty list
    description: str = "ElectroShop"
    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    categories: List[str] = field(default_factory=lambda: ["workplace"])
    upkeep: int = 15
    # Inherit materials_required from the parent class (RepairWorkshop)
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"ElectricalWorkshop: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["workshop", "tools"],
            "menu_options": [],
            "source": None,
            "salience": 1.0,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
            
        }


    def to_dict(self):
        return asdict(self)

    def repair_item(self, item):
        print(f"Repairing electrical item {item} at {self.name}.")
        # Repair logic for electrical items
        # Add the repair logic here, such as restoring item durability or functionality

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Stash(PerceptibleLocation):
    name: str = "Secret Stash 1"
    tags: list[str] = field(default_factory=lambda: ["secret", "gang"])
    description: str = "Gang Stash"
    legality: bool = False

    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    stored_items: List[str] = field(default_factory=list)

    cash: int = 0
    bankCardCash: int = 0
    upkeep: int = 5
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = False
    energy_cost: int = 0
    categories: List[str] = field(default_factory=lambda: ["gang"])
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))
    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Gang Stash: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "Gang"],
            "urgency": 1,
            "menu_options": [],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
            
        }

    def to_dict(self):
        return asdict(self)

    def store_item(self, item: str):
        self.stored_items.append(item)
        print(f"Item {item} stored in stash")

    #Any gang memebr who knows about it can retrieve items
    def retrieve_item(self, item: str):
        if item in self.stored_items:
            self.stored_items.remove(item)
            print(f"Item {item} retrieved from stash")
        else:
            print(f"Item {item} not found in stash")

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Factory(WorkplaceMixin, PerceptibleLocation):
    name: str = "The Old Factory"
    tags: list[str] = field(default_factory=lambda: ["corporate", "factory"])

    description: str = "A Factory"
    goods_produced: List[str] = field(default_factory=list)  # An empty list, meaning no goods produced initially
    materials_available: List[str] = field(default_factory=list)  # An empty list, meaning no materials available initially

    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    categories: List[str] = field(default_factory=lambda: ["workplace"])
    upkeep: int = 60
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"a {self.__class__.__name__}", # Placeholder, should be overridden
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "tools"],
            "menu_options": [],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
        }
    

    def to_dict(self):
        return asdict(self)

    def produce_goods(self):
        print(f"Factory at {self.name} is producing goods.")
        # Logic for processing materials into goods
        for material in self.materials_available:
            # Example: produce goods based on materials
            produced_good = f"Produced {material} good"
            self.goods_produced.append(produced_good)
            print(produced_good)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Nightclub(WorkplaceMixin, PerceptibleLocation):
    name: str = "Music and Slappers"
    tags: list[str] = field(default_factory=lambda: ["fun", "social"])
    description: str = "Some Club"
    fun: int = 1
    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    categories: List[str] = field(default_factory=lambda: ["workplace", "fun", "social"])
    upkeep: int = 30
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Nightclub: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "tools"],
            "urgency": 1,
            "menu_options": [],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
        }

    def to_dict(self):
        return asdict(self)

    """def secret_entrance_decorator(self, func):
        Decorator method to allow access based on entrance state."""
    """ def wrapper(*args, **kwargs):
        if self.secret_entrance:
            print("Access granted through the secret entrance.")
            return func(*args, **kwargs)
        else:
            print("Secret entrance is not available.")
            return None
    return wrapper 

    @secret_entrance_decorator
    def access_secret_entrance(self):
        print(f"{self.name} secret entrance accessed.")"""
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"

@dataclass
class Mine(WorkplaceMixin, PerceptibleLocation):
    name: str = "Typical Mine"
    tags: list[str] = field(default_factory=lambda: ["corporate", "grim"])
    description: str = "A Mine"
    fun: int = 0
    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    categories: List[str] = field(default_factory=lambda: ["workplace"])
    is_concrete: bool = True
    upkeep: int = 40
    secret_entrance: bool = True
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "region": self.region.name if self.region else None,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Mine: {self.name}",
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "tools"],
            "source": None,
            "salience": 1.0,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
        }

    def to_dict(self):
        return asdict(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Powerplant(WorkplaceMixin, PerceptibleLocation):
    name: str = "Le PowerPlant 1"
    tags: list[str] = field(default_factory=lambda: ["power", "grim"])
    description: str = "A Powerplant"
    energy_output: int = 1000
    categories: List[str] = field(default_factory=lambda: ["workplace", "power"])

    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    connected_locations: List[Any] = field(default_factory=list)
    upkeep: int = 50
    is_concrete: bool = True
    secret_entrance: bool = True
    fun: int = -1
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "region": self.region.name if self.region else None,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Powerplant: {self.name}",
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "tools"],
            "source": None,
            "salience": 1.1,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
        }

    def to_dict(self):
        return asdict(self)

    """ def secret_entrance_decorator(self, func):
        Decorator method to allow access based on entrance state.
        def wrapper(*args, **kwargs):
            if self.secret_entrance:
                print("Access granted through the secret entrance.")
                return func(*args, **kwargs)
            else:
                print("Secret entrance is not available.")
                return None
        return wrapper

    @secret_entrance_decorator
    def access_secret_entrance(self):
        print(f"{self.name} secret entrance accessed.")"""

    def distribute_energy(self):
        energy_per_location = self.energy_output // len(self.connected_locations) if self.connected_locations else 0
        for location in self.connected_locations:
            location.is_powered = True
            location.energy_cost = energy_per_location  # Adjusted for simplicity
            print(f"{self.name} supplies energy to {location.name}.")

    def disconnect_location(self, location):
        if location in self.connected_locations:
            self.connected_locations.remove(location)
            print(f"Disconnected {location.name} from {self.name}.")
        else:
            print(f"{location.name} is not connected to {self.name}.")

    def auto_connect(self, all_locations):
        for location in all_locations:
            if location.side == self.side and location != self:
                self.connected_locations.append(location)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Airport(WorkplaceMixin, PerceptibleLocation):
    name: str = "Air Port 1"
    tags: list[str] = field(default_factory=lambda: ["airport", "corporate", "export", "import"])
    description: str = "An Airport"
    connected_locations: List[Any] = field(default_factory=list)  # An empty list, no connected locations
    import_capacity: int = 0  # Zero capacity as a meaningless default
    materials_inventory: Dict[str, int] = field(default_factory=dict)  # An empty dictionary, no materials
    upkeep: int = 150
    categories: List[str] = field(default_factory=lambda: ["workplace", "commercial"])
    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    is_concrete: bool = True
    secret_entrance: bool = True
    fun: int = 0
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Airport: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location"],
            "urgency": 1,
            "menu_options": [],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }

    def to_dict(self):
        return asdict(self)

    """ def secret_entrance_decorator(self, func):
        Decorator method to allow access based on entrance state.
        def wrapper(*args, **kwargs):
            if self.secret_entrance:
                print("Access granted through the secret entrance.")
                return func(*args, **kwargs)
            else:
                print("Secret entrance is not available.")
                return None
        return wrapper 

    @secret_entrance_decorator
    def access_secret_entrance(self):
        print(f"{self.name} secret entrance accessed.")"""

    def import_materials(self, amount: Dict[str, int]):
        """
        Import materials into the inventory.
        :param amount: A dictionary where keys are material names and values are quantities to add.
        """
        if isinstance(amount, dict):  # Ensure amount is a dictionary
            print(f"Importing materials: {amount}")
            for material, qty in amount.items():
                self.materials_inventory[material] = self.materials_inventory.get(material, 0) + qty
                print(f"Imported {qty} of {material}.")
        else:
            print("Error: 'amount' should be a dictionary of materials.")

    def add_material(self, material: str, quantity: int):
        """
        Add or increase a material's quantity in the inventory.
        :param material: Name of the material to add.
        :param quantity: Quantity of the material to add.
        """
        if quantity <= 0:
            print(f"Error: Quantity should be greater than zero. Got {quantity}.")
            return
        self.materials_inventory[material] = self.materials_inventory.get(material, 0) + quantity
        print(f"Added {quantity} of {material} to the inventory.")

    def remove_material(self, material: str, quantity: int):
        """
        Decrease or remove a material's quantity from the inventory.
        :param material: Name of the material to remove.
        :param quantity: Quantity of the material to remove.
        """
        if quantity <= 0:
            print(f"Error: Quantity should be greater than zero. Got {quantity}.")
            return
        if material in self.materials_inventory:
            self.materials_inventory[material] -= quantity
            if self.materials_inventory[material] <= 0:
                del self.materials_inventory[material]
                print(f"Removed all of {material} from the inventory.")
            else:
                print(f"Removed {quantity} of {material}. Remaining: {self.materials_inventory[material]}.")
        else:
            print(f"Error: Material '{material}' not found in inventory.")

    def list_materials(self) -> Dict[str, int]:
        """
        List all materials and their quantities in the inventory.
        :return: A dictionary representing the materials inventory.
        """
        print(f"Current inventory: {self.materials_inventory}")
        return self.materials_inventory

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Port(WorkplaceMixin, PerceptibleLocation):
    name: str = "Edge Port"
    tags: list[str] = field(default_factory=lambda: ["port", "import", "export"])
    description: str = "A Port"
    connected_locations: List[Any] = field(default_factory=list)  # An empty list, no connected locations
    import_capacity: int = 0  # Zero capacity as a meaningless default
    materials_inventory: Dict[str, int] = field(default_factory=dict)  # An empty dictionary, no materials
    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    categories: List[str] = field(default_factory=lambda: ["workplace", "commercial"])
    upkeep: int = 40
    is_concrete: bool = True
    secret_entrance: bool = True
    fun: int = 0
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Port: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location"],
            "urgency": 1,
            "menu_options": [],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }
    
    def to_dict(self):
        return asdict(self)

    """ def secret_entrance_decorator(self, func):
        Decorator method to allow access based on entrance state.
        def wrapper(*args, **kwargs):
            if self.secret_entrance:
                print("Access granted through the secret entrance.")
                return func(*args, **kwargs)
            else:
                print("Secret entrance is not available.")
                return None
        return wrapper 

    @secret_entrance_decorator
    def access_secret_entrance(self):
        print(f"{self.name} secret entrance accessed.")"""

    def import_materials(self, amount: Dict[str, int]):
        """
        Import materials into the inventory.
        :param amount: A dictionary where keys are material names and values are quantities to add.
        """
        if isinstance(amount, dict):  # Ensure amount is a dictionary
            print(f"Importing materials: {amount}")
            for material, qty in amount.items():
                self.materials_inventory[material] = self.materials_inventory.get(material, 0) + qty
                print(f"Imported {qty} of {material}.")
        else:
            print("Error: 'amount' should be a dictionary of materials.")

    def add_material(self, material: str, quantity: int):
        """
        Add or increase a material's quantity in the inventory.
        :param material: Name of the material to add.
        :param quantity: Quantity of the material to add.
        """
        if quantity <= 0:
            print(f"Error: Quantity should be greater than zero. Got {quantity}.")
            return
        self.materials_inventory[material] = self.materials_inventory.get(material, 0) + quantity
        print(f"Added {quantity} of {material} to the inventory.")

    def remove_material(self, material: str, quantity: int):
        """
        Decrease or remove a material's quantity from the inventory.
        :param material: Name of the material to remove.
        :param quantity: Quantity of the material to remove.
        """
        if quantity <= 0:
            print(f"Error: Quantity should be greater than zero. Got {quantity}.")
            return
        if material in self.materials_inventory:
            self.materials_inventory[material] -= quantity
            if self.materials_inventory[material] <= 0:
                del self.materials_inventory[material]
                print(f"Removed all of {material} from the inventory.")
            else:
                print(f"Removed {quantity} of {material}. Remaining: {self.materials_inventory[material]}.")
        else:
            print(f"Error: Material '{material}' not found in inventory.")

    def list_materials(self) -> Dict[str, int]:
        """
        List all materials and their quantities in the inventory.
        :return: A dictionary representing the materials inventory.
        """
        print(f"Current inventory: {self.materials_inventory}")
        return self.materials_inventory

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Factory(WorkplaceMixin, PerceptibleLocation):
    name: str = "Default Factory Name"
    tags: list[str] = field(default_factory=lambda: ["commercial", "manufacture", "grim"])
    description: str = "A Factory"
    raw_materials_needed: int = 100
    output_rate: int = 100
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    upkeep: int = 30

    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    workers_needed: int = 5
    workers_present: int = 0  # Updated dynamically
    products: int = 0  # Tracks produced goods
    is_concrete: bool = True
    secret_entrance: bool = False
    fun: int = -1
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))
    
    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Factory: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "tools"],
            "urgency": 1,
            
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
            
        }
    
    def to_dict(self):
        return asdict(self)

    def can_produce(self):
        """Check if the factory can produce goods."""
        return self.is_powered and self.workers_present >= self.workers_needed and self.raw_materials_needed > 0

    def produce_goods(self):
        """Produce goods if conditions are met."""
        if self.can_produce():
            self.products += self.output_rate
            self.raw_materials_needed -= 1
            logging.info(f"{self.name} produced {self.output_rate} goods. Total produced: {self.products}.")
        else:
            logging.warning(f"{self.name} cannot produce goods. Not enough workers, power, or raw materials.")

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Cafe(WorkplaceMixin, PerceptibleLocation):
    name: str = "Metro Cafe"
    tags: list[str] = field(default_factory=lambda: ["workplace", "fun", "food", "social"])
    description: str = "A cafe"
    upkeep: int = 10
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    ambience: Ambience = field(default_factory=lambda: Ambience({"social": 0.5, "fun": 0.3}))
    #add also to percepts. Good ambience might be calculated by the aggregate fun present
    """ self.ambience = Ambience({
    "peace": 0.6,
    "curiosity": 0.4,
    "memory": 0.2
}) """

    items_available: List[Any] = field(default_factory=list)#food for sale
    inventory: Inventory = field(default_factory=Inventory)#materia prima

    owner: Optional[Character] = None  # A Family, Character, or Corporation
    employees_there: List['Employee'] = field(default_factory=list)
    allowed_roles = [COOK, CAFE_MANAGER, WAITRESS]
    """ Passive Thought Emission
    After each tick, locations emit ambience-derived thoughts based on character psy. """
    fun: int = 1
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Cafe: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "food"],
            "urgency": 1,
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
            
        }

    def to_dict(self):
        return asdict(self)

    def serve_customer(self, character):
        """Serve a customer and increase their satisfaction based on ambience and fun."""
        print(f"{character.name} is enjoying the ambience at {self.name}.")
        if self.ambience_level > 7:
            character.satisfaction += 10  # Example: increase character satisfaction
            print(f"The ambience at {self.name} makes {character.name} feel very relaxed!")
        else:
            character.satisfaction += 5  # Smaller satisfaction increase for lower ambience
            print(f"{character.name} enjoys their time at {self.name}, but the ambience could be better.")

        # Add more logic if you want to further interact with the customer based on the cafe's attributes.

def update_dynamic_ambience(self):
    total_fun = sum(c.fun for c in self.characters_there + self.employees_there)
    self.ambience.vibes["fun"] = min(total_fun / 100, 1.0)  # normalize to 0-1
    if len(self.characters_there) > 3:
        self.ambience.vibes["social"] = 0.4 + len(self.characters_there) * 0.05


def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Park(WorkplaceMixin, PerceptibleLocation):
    name: str = "Green Park"
    tags: list[str] = field(default_factory=lambda: ["fun", "social"])
    description: str = "A Park"
    categories: List[str] = field(default_factory=lambda: ["workplace", "public", "fun", "social"])
    upkeep: int = 15
    ambience_level: int = 1
    fun: int = 1

    items_available: List[Any] = field(default_factory=list) #relevant? park toys?
    inventory: Inventory = field(default_factory=Inventory)

    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Park: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location"],
            "urgency": 1,
            "menu_options": [],
            "source": None,
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }
    

    def to_dict(self):
        return asdict(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


class SanctumMixin:
    def __init__(self, *args, **kwargs):
        # call super so dataclass parents can initialize
        try:
            super().__init__(*args, **kwargs)
        except Exception:
            # ok if parent __init__ signature different
            pass

        # Sanctum-specific state
        self.resonance_tags = ["sanctum", "fun", "safe"]
        self.warded = True
        self.allowed_visitors = ["The Kind Man"]
        self.categories = ["residential", "private"]
        self.description = "A protected place where Luna plays and thinks"

        self.ambience = Ambience({
            "peace": 0.6,
            "curiosity": 0.4,
            "memory": 0.2
        })

    def can_enter(self, character):
        return character.name in self.allowed_visitors or not self.warded

    def get_sanctum_tags(self):
        return ["sanctum", "peaceful"] if self.warded else []

    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        base["tags"].extend(["sanctum"])
        base["description"] = f"{self.name} — still and luminous"
        return base

    
@dataclass
class LunaSanctum(SanctumMixin, Park):
    
    name: str = "Luna Sanctum"
    tags: list[str] = field(default_factory=lambda: ["sanctum", "fun", "safe"])
    description: str = "A protected place where Luna plays and thinks"
    categories: List[str] = field(default_factory=lambda: ["fun", "private", "sacred"])
    allowed_visitors: List[str] = field(default_factory=lambda: ["The Kind Man"])

    #I might need to prevent this from automatically receiving npcs looking to work there, as it might be a workplace, via class Park.
    is_workplace: bool = False
    #Luna’s sanctum should be serene, not full of accountants. 🧘‍♀️✨

    ambience: Ambience = field(default_factory=lambda: Ambience({
        "peace": 0.6,
        "curiosity": 0.4,
        "memory": 0.2
    }))

    def __post_init__(self):
        SanctumMixin.__init__(self)
        Park.__post_init__(self)
        self.inventory.owner = self

    


    def get_percept_data(self, observer=None):
        base = super().get_percept_data(observer)
        base["tags"].extend(["sanctum"])
        base["description"] = f"{self.name} — still and luminous"
        return base


@dataclass
class Museum(WorkplaceMixin, PerceptibleLocation):
    name: str = "City Museum"
    tags: list[str] = field(default_factory=lambda: ["public", "fun", "culture", "history"])
    description: str = "A Museum"
    upkeep: int = 45
    artifact_count: int = 50
    items_available: List[Any] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    exhibits: List[str] = field(default_factory=list)  # List of exhibit names

    categories: List[str] = field(default_factory=lambda: ["workplace", "fun", "social", "records"])
    
    fun: int = 3
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = True
    energy_cost: int = 100
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Museum: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "tools"],
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }
    
    def to_dict(self):
        return asdict(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Library(WorkplaceMixin, PerceptibleLocation):
    name: str = "Public Library"
    tags: list[str] = field(default_factory=lambda: ["books", "social"])
    description: str = "A Library"
    categories: List[str] = field(default_factory=lambda: ["public", "record", "workplace"])
    upkeep: int = 20

    book_count: int = 10000
    genres_available: List[str] = field(default_factory=list)  # List of genres
    inventory: Inventory = field(default_factory=Inventory) #overlap

    fun: int = 2
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = True
    energy_cost: int = 50
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Library: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "books"],
            "urgency": 1,
            
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security(),
        }
    
    def to_dict(self):
        return asdict(self)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class ResearchLab(WorkplaceMixin, PerceptibleLocation):
    name: str = "OmniLab"
    tags: list[str] = field(default_factory=lambda: ["science", "tech", "workplace", "record"])
    description: str = "A Lab"
    prototypes_produced: List[str] = field(default_factory=list)  # An empty list, meaning no goods produced initially
    inventory: Inventory = field(default_factory=Inventory)

    materials_available: List[str] = field(default_factory=list)  # An empty list, meaning no materials available initially
    equipment_list: List[str] = field(default_factory=list) #An empty list but lab must have something here
    upkeep: int = 200
    categories: List[str] = field(default_factory=lambda: ["science", "tech", "workplace", "record"])
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = False
    energy_cost: int = 50
    security: Security = field(default_factory=lambda: Security(
        level=3,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=True,
        alarm_system=True
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"ResearchLab: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "tools"],
            "urgency": 1,
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }
    

    def to_dict(self):
        return asdict(self)

    def research_new_tech(self):
            print(f"Lab at {self.name} is researching.")
            # Logic for researching
            

    def produce_prototypes(self):
        print(f"Lab at {self.name} is producing prototypes.")
        # Logic for processing materials into goods
        
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Warehouse(WorkplaceMixin ,PerceptibleLocation):
    name: str = "Warehouse 5"
    tags: list[str] = field(default_factory=lambda: ["storage", "faction"])
    description: str = "A Warehouse"
    upkeep: int = 15
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    storage_capacity: int = 50 # will need to upgrade to a more complex data structure
    items_available: List[str] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    fun: int = 0
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 10
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Warehouse: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "urgency": 1,
            "tags": ["location", "tools"],
            
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }
    
    def to_dict(self):
        return asdict(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class ApartmentBlock(WorkplaceMixin, PerceptibleLocation):
    name: str = "Mass Housing"
    tags: list[str] = field(default_factory=lambda: ["homes", "grim"])
    description: str = "An Apartment Block"
    upkeep: int = 35
    categories: List[str] = field(default_factory=lambda: ["residential", "grim"])
    storage_capacity: int = 50 # LOL, will need to upgrade to a more complex data structure

    items_available: List[str] = field(default_factory=list)#just to make the code run
    inventory: Inventory = field(default_factory=Inventory)

    fun: int = 0
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 30
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "origin": "self",
            "tags": "self.tags",
            "salience": "1.0",
            "urgency": "0",
            "description": f"{self.name}: {self.description}",
            "robbable": True,
            #needs data field
            "source": None,
            "menu_options": [],
            "security": getattr(self, "security_level", 0), #is this valid percept cde, aor a bad paste from attributes?
            "is_open": getattr(self, "is_open", True),#same
            "has_security": self.has_security() if hasattr(self, "has_security") else False,
        }
    
    def to_dict(self):
        return asdict(self)

    def spawn_gang(self):
        pass
        #lets gtfo and rob some mfers fam
        #if there is sufficicient children with sufficient hunger, they become a gang and gangmembers
        #OR if a special charcter recruits there

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class House(WorkplaceMixin, PerceptibleLocation):
    name: str = "Family House"
    tags: list[str] = field(default_factory=lambda: ["home", "family"])
    description: str = "A House"
    categories: List[str] = field(default_factory=lambda: ["residential"])
    upkeep: int = 5

    items_available: List[str] = field(default_factory=list)#relevant?
    inventory: Inventory = field(default_factory=Inventory)

    fun: int = 1
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 5
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))
    def to_dict(self):
        return asdict(self)
    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"House: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location"],
            "urgency": 1,
            
            "menu_options": [],
            "source": None,
            
            #"security": self.security_level,
            "is_open": self.is_open
            #"has_security": self.has_security(),

        }
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


    """ def spawn_character(self):
            return create_character(self) """
    #A stable environment, house+family MIGHT produce a useful character

    

@dataclass
class SportsCentre(WorkplaceMixin, PerceptibleLocation):
    name: str = "The Stadium"
    tags: list[str] = field(default_factory=lambda: ["fun", "social"])
    description: str = "A Stadium"
    upkeep: int = 30
    categories: List[str] = field(default_factory=lambda: ["workplace", "fun", "social"])
    items_available: List[str] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    ambience_level: int = 1
    fun: int = 1
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"SportsCentre: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "tools"],
            "urgency": 1,
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }

    def to_dict(self):
        return asdict(self)

    def give_Sport_session(self, character):
        pass
        #increase fun, and health default (not healing)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class Holotheatre(WorkplaceMixin, PerceptibleLocation):
    name: str = "Zodeono"
    tags: list[str] = field(default_factory=lambda: ["fun", "social"])
    description: str = "A cinema"
    upkeep: int = 15
    categories: List[str] = field(default_factory=lambda: ["workplace", "fun", "social"])
    items_available: List[str] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)
    ambience_level: int = 1
    fun: int = 1
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"Holotheatre: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location"],
            "urgency": 1,
            
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }
    
    def to_dict(self):
        return asdict(self)

    def show_performance(self, character):
            pass
            #increase fun for attendants, but leave them wanting more...

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class MunicipalBuilding(WorkplaceMixin, PerceptibleLocation):
    name: str = "City Hall"
    tags: list[str] = field(default_factory=lambda: ["law", "state"])
    description: str = "A Muni Building"
    items_available: List[str] = field(default_factory=list)

    inventory: Inventory = field(default_factory=Inventory)

    resource_storage: Dict[str, int] = field(default_factory=dict)
    special_features: List[str] = field(default_factory=list)
    #entrance: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace", "state"])
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = True
    energy_cost: int = 100
    security: Security = field(default_factory=lambda: Security(
        level=2,
        guards=[],
        difficulty_to_break_in=2,
        surveillance=True,
        alarm_system=True
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"MunicipalBuilding: {self.name}",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "VIP"],
            "urgency": 1,
            
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
            
        }
    
    def to_dict(self):
        # Use asdict to convert all dataclass attributes to a dictionary
        return asdict(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"


@dataclass
class PoliceStation(WorkplaceMixin, PerceptibleLocation):
    name: str = "The Yard"
    tags: list[str] = field(default_factory=lambda: ["law", "grim"])
    description: str = "A Copshop"
    categories: List[str] = field(default_factory=lambda: ["workplace", "state"])
 
    items_available: List[str] = field(default_factory=list)
    inventory: Inventory = field(default_factory=Inventory)

    resource_storage: Dict[str, int] = field(default_factory=dict)
    special_features: List[str] = field(default_factory=list)
    #entrance: List[str] = field(default_factory=list)
    
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = False
    energy_cost: int = 0
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        "origin": "FIXME",
        "tags": "FIXME",
        "salience": "FIXME",
        "urgency": "FIXME",
        "source": "FIXME",
        "security": "FIXME",
        "is_open": "FIXME",
        "has_security": "FIXME",
            "description": f"{self.name} (PoliceStation)",
            "region": self.region.name if self.region else None,
            "robbable": True,
            "origin": self,
            "tags": ["location", "police", "weapons"],
            "urgency": 1,
            "source": None,
            "menu_options": [],
            "security": self.security_level,
            "is_open": self.is_open,
            "has_security": self.has_security()
        }

    def to_dict(self):
        # Use asdict to convert all dataclass attributes to a dictionary
        return asdict(self)
    
    def imprison(character):
        pass
    
    def interogate(detective, character, targetInfo):
        pass
    
    def torture(detective, character, targetInfo):
        pass

    def hostInvestigation(investigation):
        pass
    #also has a CopBar

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"

@dataclass
class Farm(WorkplaceMixin, PerceptibleLocation):
    name: str = "Greenfield Farm"
    description: str = "A modest farm with fields, tools, and livestock."
    
    tags: list[str] = field(default_factory=lambda: ["farm", "agriculture", "workplace", "food_production"])
    
    crops: List[str] = field(default_factory=lambda: ["wheat"])
    livestock: List[str] = field(default_factory=list)
    goods_produced: List[str] = field(default_factory=list)
    
    inventory: Inventory = field(default_factory=Inventory)
    categories: List[str] = field(default_factory=lambda: ["workplace"])

    upkeep: int = 40
    is_concrete: bool = True
    is_powered: bool = False
    energy_cost: int = 0
    secret_entrance: bool = False

    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "type": "Farm",
            "description": f"Farm: {self.name}",
            "tags": ["location", "agriculture", "workplace"],
            "origin": self,
            "object": self,
            "region": self.region.name if self.region else None,
            "urgency": 1,
            "robbable": True,
            "security": self.security.level,
            "is_open": True,  # you may later add farm “open hours”
            "has_security": self.security.level > 0,
        }

    def produce_goods(self):
        """Simple production logic—expand as needed."""
        produced = []

        for crop in self.crops:
            item = f"{crop}_bushel"
            produced.append(item)
            self.goods_produced.append(item)
            self.inventory.add_item(item)

        for animal in self.livestock:
            item = f"{animal}_products"
            produced.append(item)
            self.goods_produced.append(item)
            self.inventory.add_item(item)

        print(f"Farm at {self.name} produced goods: {produced}")

    def __post_init__(self):
        self.inventory.owner = self
        super().__post_init__()

    def __repr__(self):
        return f"Farm(name='{self.name}', region={self.region.name if self.region else 'Unknown'})"