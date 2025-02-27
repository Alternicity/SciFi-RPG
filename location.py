import random
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
import logging
from faction import Faction
#shop/vendor specific (at least at first)
from base_classes import Character, Location, Faction
from location_security import Security
logging.basicConfig(level=logging.INFO)

from common import DangerLevel #this was commented out once, probs for a circular imprt problem..

@dataclass
class Region:
    name: str
    wealth: str = "Normal"
    shops: List[str] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    factions: List[str] = field(default_factory=list)
    danger_level: Optional[DangerLevel] = None
    region_gangs: List = field(default_factory=list) #dataclass syntax.  ensures each instance of Region
    #gets a unique list for region_gangs
    
    region_corps: List = field(default_factory=list)

#Each region will contain a list of Shop and other Location objects
    def add_location(self, location: Location):
        """Adds a location to this region and updates the location's region reference."""
        location.region = self
        self.locations.append(location)
        print(f"Added {location.name} to region {self.name}.")

    def trigger_event(self, event_type: str):
        print(f"Event triggered: {event_type} in {self.name}")
        
    def __str__(self):
        return self.name  # Ensures `str(region)` returns just its name
    
@dataclass
class UndevelopedRegion(Region):
    name: str
    locations: List[str] = field(default_factory=list)
    factions: List[str] = field(default_factory=list)

@dataclass
class VacantLot(Location):
    name: str = "Empty Land"
    location: str = "N/A"
    categories: List[str] = field(default_factory=lambda: ["public"])
    upkeep: int = 0
    ambiance_level: int = 0
    fun: int = 0
    is_concrete: bool = True
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0

@dataclass
class HQ(Location):
    name: str = "Base"
    faction: Optional[Faction] = field(default=None)
    items_available: List[str] = field(default_factory=list) 
    resource_storage: Dict[str, int] = field(default_factory=dict)
    special_features: List[str] = field(default_factory=list)
    #entrance: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["residential", "workplace", "public"])
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

    def to_dict(self):
        # Use asdict to convert all dataclass attributes to a dictionary
        return asdict(self)

@dataclass
class Vendor(Location):
    items_available: list = field(default_factory=list)
    #items_available: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    is_concrete: bool = False
    secret_entrance: bool = True
    cash: int = 0
    bankCardCash: int = 0
    # No need to define __init__; @dataclass handles it
    def __post_init__(self):
        super().__post_init__()


@dataclass
class Shop(Vendor):
    name: str = "QQ Store"
    legality: bool = True
    fun: int = 0
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    inventory: dict = field(default_factory=dict)  # Replaces items_available
    cash : int = 300
    bankCardCash: int = 0
    is_concrete: bool = True
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

    def to_dict(self):
        return asdict(self)

    

    def sell_item(self, character, item_name):
        """Sell an item to a character."""
        if item_name in self.inventory:
            item_details = self.inventory[item_name]
            if character.bankCardCash >= item_details['price']:
                # Deduct money and update inventory
                character.bankCardCash -= item_details['price']
                character.inventory.append(item_name)
                item_details['quantity'] -= 1
                print(f"{item_name} sold to {character.name} for ${item_details['price']}. Remaining balance: ${character.bankCardCash}")
                # Placeholder for economy.py processing
                # economy.process_transaction(character, self, item_name, item_details['price'])
            else:
                print(f"{character.name} doesn't have enough money to buy {item_name}.")
        else:
            print(f"{item_name} is not available in {self.name}'s inventory.")


@dataclass
class CorporateStore(Vendor):
    name: str = "Stores"
    corporation: str = "Default"  # Default value is now valid
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    items_available: List[str] = field(default_factory=list)
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
    inventory: dict = field(default_factory=dict)
    legality: str = "Legal"

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

@dataclass
class RepairWorkshop(Location, ABC):
    materials_required: List[str] = field(default_factory=list)
    items_available: List[Any] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    is_concrete: bool = False
    secret_entrance: bool = False
    is_powered: bool = False
    energy_cost: int = 0

    def to_dict(self):
        return asdict(self)

    @abstractmethod
    def repair_item(self, item):
        """Repair the given item (to be implemented in subclasses)."""
        pass

@dataclass
class MechanicalRepairWorkshop(RepairWorkshop):
    name: str = "Greasehands"
    items_available: list = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace"])
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

    def to_dict(self):
        return asdict(self)

    def repair_item(self, item):
        print(f"Repairing mechanical item {item} at {self.name}.")
        # Repair logic for mechanical items
        # Add the repair logic here, such as reducing item damage or restoring health

@dataclass
class ElectricalRepairWorkshop(RepairWorkshop):
    name: str = "Sparks"
    materials_required: List[str] = field(default_factory=list)  # An empty list
    items_available: List[Any] = field(default_factory=list)
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


    def to_dict(self):
        return asdict(self)

    def repair_item(self, item):
        print(f"Repairing electrical item {item} at {self.name}.")
        # Repair logic for electrical items
        # Add the repair logic here, such as restoring item durability or functionality

@dataclass
class Stash(Location):
    name: str = "Secret Stash 1"
    legality: bool = False
    items_available: List[Any] = field(default_factory=list)
    stored_items: List[str] = field(default_factory=list)
    inventory: dict = field(default_factory=dict)
    cash: int = 0
    bankCardCash: int = 0
    upkeep: int = 5
    is_concrete: bool = True
    secret_entrance: bool = True
    is_powered: bool = False
    energy_cost: int = 0
    categories: List[str] = field(default_factory=lambda: ["residential", "workplace", "public"])
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))

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

@dataclass
class Factory(Location):
    name: str = "The Old Factory"
    goods_produced: List[str] = field(default_factory=list)  # An empty list, meaning no goods produced initially
    materials_available: List[str] = field(default_factory=list)  # An empty list, meaning no materials available initially
    items_available: List[Any] = field(default_factory=list)
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

@dataclass
class Nightclub(Location):
    name: str = "Music and Slappers"
    fun: int = 1
    items_available: List[Any] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace"])
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


@dataclass
class Mine(Location):
    name: str = "Typical Mine"
    fun: int = 0
    items_available: List[Any] = field(default_factory=list)
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

    def to_dict(self):
        return asdict(self)


@dataclass
class Powerplant(Location):
    name: str = "Le PowerPlant 1"
    energy_output: int = 1000
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    items_available: List[Any] = field(default_factory=list)
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

@dataclass
class Airport(Location):
    name: str = "Air Port 1"
    connected_locations: List[Any] = field(default_factory=list)  # An empty list, no connected locations
    import_capacity: int = 0  # Zero capacity as a meaningless default
    materials_inventory: Dict[str, int] = field(default_factory=dict)  # An empty dictionary, no materials
    upkeep: int = 150
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    items_available: List[Any] = field(default_factory=list)
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

@dataclass
class Port(Location):
    name: str = "Edge Port"
    connected_locations: List[Any] = field(default_factory=list)  # An empty list, no connected locations
    import_capacity: int = 0  # Zero capacity as a meaningless default
    materials_inventory: Dict[str, int] = field(default_factory=dict)  # An empty dictionary, no materials
    items_available: List[Any] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace"])
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

@dataclass
class Factory(Location):
    name: str = "Default Factory Name"
    raw_materials_needed: int = 100
    output_rate: int = 100
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    upkeep: int = 30
    items_available: List[Any] = field(default_factory=list)
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

@dataclass
class Cafe(Location):
    name: str = "Metro Cafe"
    location: str = "North"
    upkeep: int = 10
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    ambiance_level: int = 1
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

    def to_dict(self):
        return asdict(self)

    def serve_customer(self, character):
        """Serve a customer and increase their satisfaction based on ambiance and fun."""
        print(f"{character.name} is enjoying the ambiance at {self.name}.")
        if self.ambiance_level > 7:
            character.satisfaction += 10  # Example: increase character satisfaction
            print(f"The ambiance at {self.name} makes {character.name} feel very relaxed!")
        else:
            character.satisfaction += 5  # Smaller satisfaction increase for lower ambiance
            print(f"{character.name} enjoys their time at {self.name}, but the ambiance could be better.")

        # Add more logic if you want to further interact with the customer based on the cafe's attributes.


@dataclass
class Park(Location):
    name: str = "Green Park"
    location: str = "Central"
    categories: List[str] = field(default_factory=lambda: ["residential", "workplace", "public"])
    upkeep: int = 15
    ambiance_level: int = 1
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

    def to_dict(self):
        return asdict(self)

@dataclass
class Museum(Location):
    name: str = "City Museum"
    location: str = "Central"
    upkeep: int = 45
    artifact_count: int = 50
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    exhibits: List[str] = field(default_factory=list)  # List of exhibit names
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

    def to_dict(self):
        return asdict(self)

@dataclass
class Library(Location):
    name: str = "Public Library"
    location: str = "West"
    categories: List[str] = field(default_factory=lambda: ["public"])
    upkeep: int = 20
    book_count: int = 10000
    genres_available: List[str] = field(default_factory=list)  # List of genres
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

    def to_dict(self):
        return asdict(self)

@dataclass
class ResearchLab(Location):
    name: str = "OmniLab"
    prototypes_produced: List[str] = field(default_factory=list)  # An empty list, meaning no goods produced initially
    materials_available: List[str] = field(default_factory=list)  # An empty list, meaning no materials available initially
    equipment_list: List[str] = field(default_factory=list) #An empty list but lab must have something here
    upkeep: int = 200
    categories: List[str] = field(default_factory=lambda: ["workplace"])
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


    def to_dict(self):
        return asdict(self)

    def research_new_tech(self):
            print(f"Lab at {self.name} is researching.")
            # Logic for researching
            

    def produce_prototypes(self):
        print(f"Lab at {self.name} is producing prototypes.")
        # Logic for processing materials into goods
        
@dataclass
class Warehouse(Location):
    name: str = "Warehouse 5"
    location: str = "wherever"
    upkeep: int = 15
    categories: List[str] = field(default_factory=lambda: ["residential", "workplace", "public"])
    storage_capacity: int = 50 # will need to upgrade to a more complex data structure
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

    def to_dict(self):
        return asdict(self)

        

@dataclass
class ApartmentBlock(Location):
    name: str = "Mass Housing"
    location: str = "wherever"
    upkeep: int = 35
    categories: List[str] = field(default_factory=lambda: ["residential"])
    storage_capacity: int = 50 # LOL, will need to upgrade to a more complex data structure
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

    def to_dict(self):
        return asdict(self)

    def spawn_gang(self):
        pass
        #lets gtfo and rob some mfers fam
        #if there is sufficicient children with sufficient hunger, they become a gang and gangmembers
        #OR if a special charcter recruits there



@dataclass
class House(Location):
    name: str = "Fam House"
    location: str = "wherever"
    categories: List[str] = field(default_factory=lambda: ["residential"])
    upkeep: int = 5
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

    def spawn_character(self):
            return create_character(self)
    #A stable environment, house+family MIGHT produce a useful character

    

@dataclass
class SportsCentre(Location):
    name: str = "The Stadium"
    location: str = "wherever"
    upkeep: int = 30
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    ambiance_level: int = 1
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

    def to_dict(self):
        return asdict(self)

    def give_Sport_session(self, character):
        pass
        #increase fun, and health default (not healing)

        
@dataclass
class Holotheatre(Location):
    name: str = "Zodeono"
    location: str = "wherever"
    upkeep: int = 15
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    ambiance_level: int = 1
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

    def to_dict(self):
        return asdict(self)

    def show_performance(self, character):
            pass
            #increase fun for attendants, but leave them wanting more...

@dataclass
class MunicipalBuilding(Location):
    name: str = "City Hall" 
    items_available: List[str] = field(default_factory=list) 
    resource_storage: Dict[str, int] = field(default_factory=dict)
    special_features: List[str] = field(default_factory=list)
    #entrance: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["workplace"])
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

    def to_dict(self):
        # Use asdict to convert all dataclass attributes to a dictionary
        return asdict(self)

@dataclass
class PoliceStation(Location):
    name: str = "The Yard"
    categories: List[str] = field(default_factory=lambda: ["workplace"])
    items_available: List[str] = field(default_factory=list) 
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

    def to_dict(self):
        # Use asdict to convert all dataclass attributes to a dictionary
        return asdict(self)
    
    def imprison(character):
        return idk(self)
    
    def interogate(detective, character, targetInfo):
        return(results)
    
    def torture(detective, character, targetInfo):
        return(results)

    def hostInvestigation(investigation):
        return(results)
    #also has a CopBar