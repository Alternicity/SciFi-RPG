import random
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

# Decorator definition (must be placed before the class definition)
def check_entrance_state(func):
    def wrapper(self, *args, **kwargs):
        if self.primary_entrance.state == "Open":  # Ensure entrance is open before calling function
            print(f"Access granted to {self.name}.")
            return func(self, *args, **kwargs)
        else:
            print(f"Access denied to {self.name}, entrance is closed.")
            return None  # or handle denied access differently
    return wrapper

@dataclass
class Location:
    name: str
    side: str
    security_level: int
    condition: str

    fun: int = 0
    is_concrete: bool = False
    secret_entrance: bool = False
    entrances: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        # Any additional setup logic if needed
        pass

    def add_entrances(self, *entrances):
        self.entrances.extend(entrances)
        print(f"Entrances added to {self.name}: {', '.join(entrances)}")

# Decorator to check entrance state
def check_entrance_state(func):
    def wrapper(self, *args, **kwargs):
        if self.secret_entrance:
            print(f"Accessing secret entrance to {self.name}.")
            return func(self, *args, **kwargs)
        else:
            print(f"Secret entrance not available at {self.name}.")
            return None
    return wrapper

@dataclass
class HQ(Location):
    name: str = "Base"
    items_available: list = field(default_factory=list) 
    resource_storage: dict = field(default_factory=dict)
    special_features: List[str] = field(default_factory=list)
    entrances: List[str] = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = True
    
    def __post_init__(self):
        # Any additional initialization logic
        print(f"Initialized HQ: {self.name}, Entrances: {', '.join(self.entrances)}")


@dataclass
class Vendor(Location):
    items_available: list = field(default_factory=list)
    items_available: List[str] = field(default_factory=list)
    is_concrete: bool = False
    secret_entrance: bool = True

    # No need to define __init__; @dataclass handles it
    def __post_init__(self):
        super().__post_init__()
        print(f"Initialized Vendor: {self.name}, Items Available: {', '.join(self.items_available)}")

@dataclass
class Shop(Vendor):
    name: str = "QQ Store"
    fun: int = 0
    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = False

    # No need to define __init__; @dataclass handles it
    def sell_item(self, character, item):
        if item in self.items_available:
            print(f"Item {item} sold to {character.name}")
            # Add item to character's inventory (or some similar behavior)
        else:
            print(f"Item {item} not available")

@dataclass
class CorporateStore(Vendor):
    name: str = "Stores"
    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = False

    def sell_item(self, character, item):
        if character.status >= self.required_status:
            if item in self.items_available:
                print(f"Corporate item {item} sold to {character.name}")
                # Add item to character's inventory (or some similar behavior)
            else:
                print(f"Item {item} not available")
        else:
            print(f"{character.name} does not have sufficient status to buy {item}")

from typing import List

@dataclass
class RepairWorkshop(Location, ABC):
    materials_required: List[str] = field(default_factory=list)
    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = False

    @abstractmethod
    def repair_item(self, item):
        """Repair the given item (to be implemented in subclasses)."""
        pass

@dataclass
class MechanicalRepairWorkshop(RepairWorkshop):
    name: str = "Greasehands"
    items_available: list = field(default_factory=list)
    # Inherit materials_required from the parent class (RepairWorkshop)
    materials_required: List[str] = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = False

    def repair_item(self, item):
        print(f"Repairing mechanical item {item} at {self.name}.")
        # Repair logic for mechanical items
        # Add the repair logic here, such as reducing item damage or restoring health

@dataclass
class ElectricalRepairWorkshop(RepairWorkshop):
    name: str = "Sparks"
    materials_required: List[str] = field(default_factory=list)  # An empty list
    items_available: list = field(default_factory=list)
    # Inherit materials_required from the parent class (RepairWorkshop)
    is_concrete: bool = True
    secret_entrance: bool = False

    def repair_item(self, item):
        print(f"Repairing electrical item {item} at {self.name}.")
        # Repair logic for electrical items
        # Add the repair logic here, such as restoring item durability or functionality

@dataclass
class Stash(Location):
    name: str = "Secret Stash 1"
    items_available: list = field(default_factory=list)
    stored_items: List[str] = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = True

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
    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = False

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
    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = True

    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
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
        print(f"{self.name} secret entrance accessed.")


@dataclass
class Mine(Location):
    name: str = "Typical Mine"
    
    fun: int = 1

    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = True

    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
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
        print(f"{self.name} secret entrance accessed.")

@dataclass
class Powerplant(Location):
    name: str = "Le PowerPlant 1"
    
    energy_output: int = 1000

    items_available: list = field(default_factory=list)
    connected_locations: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = True
    fun: int = -1

    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
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
        print(f"{self.name} secret entrance accessed.")

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
    
    connected_locations: list = field(default_factory=list)  # An empty list, no connected locations
    import_capacity: int = 0  # Zero capacity as a meaningless default
    materials_inventory: dict = field(default_factory=dict)  # An empty dictionary, no materials

    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = True
    fun: int = 0

    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
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
        print(f"{self.name} secret entrance accessed.")

    def import_materials(self, amount):
        if isinstance(amount, dict):  # Ensure amount is a dictionary
            print(f"Importing materials: {amount}")
            for material, qty in amount.items():
                self.materials_inventory[material] = self.materials_inventory.get(material, 0) + qty
                print(f"Imported {qty} of {material}.")
        else:
            print("Error: 'amount' should be a dictionary of materials.")

@dataclass
class Port(Location):
    name: str = "Edge Port"
    
    connected_locations: list = field(default_factory=list)  # An empty list, no connected locations
    import_capacity: int = 0  # Zero capacity as a meaningless default
    materials_inventory: dict = field(default_factory=dict)  # An empty dictionary, no materials

    items_available: list = field(default_factory=list)
    is_concrete: bool = True
    secret_entrance: bool = True
    fun: int = 0

    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
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
        print(f"{self.name} secret entrance accessed.")

    def import_materials(self, amount):
        if isinstance(amount, dict):  # Ensure amount is a dictionary
            print(f"Importing materials: {amount}")
            for material, qty in amount.items():
                self.materials_inventory[material] = self.materials_inventory.get(material, 0) + qty
                print(f"Imported {qty} of {material}.")
        else:
            print("Error: 'amount' should be a dictionary of materials.")

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

@dataclass
class Factory(Location):
    name: str = "Default Factory Name"
    # (what is this?)
    raw_materials_needed: int = 100
    output_rate: int = 100
    energy_needed: int = 100

    items_available: list = field(default_factory=list)
    workers_needed: int = 5
    workers_present: int = 0  # Updated dynamically
    products: int = 0  # Tracks produced goods
    is_concrete: bool = True
    secret_entrance: bool = False
    fun: int = -1

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

from dataclasses import dataclass, field

@dataclass
class Cafe(Location):
    name: str
    location: str
    security_level: int
    upkeep: int
    ambiance_level: int
    fun: int
    is_concrete: bool = True
    secret_entrance: bool = False

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



class Park(Location):
    def __init__(self, name, side, security_level, condition, fun, has_events=False, benches=0):
        super().__init__(name, "Park", side, security_level, condition, fun)
        self.has_events = has_events  # Whether there are events happening in the park
        self.benches = benches  # Number of benches in the park
        self.is_concrete = True
        self.secret_entrance = False

    def host_event(self):
        """Host an event in the park, increasing the fun level."""
        if self.has_events:
            print(f"{self.name} is hosting an event! It increases fun for everyone.")
            self.fun += 5  # Example: Increase fun for everyone at the park
        else:
            print(f"{self.name} is quiet today with no events.")
    
    def add_benches(self, num_benches):
        """Add benches to the park to enhance the atmosphere."""
        self.benches += num_benches
        print(f"{num_benches} new benches have been added to {self.name}.")
    
    def park_condition(self):
        """Display the condition of the park."""
        if self.condition > 7:
            print(f"{self.name} is in great condition!")
        elif self.condition > 4:
            print(f"{self.name} is in decent condition.")
        else:
            print(f"{self.name} is in poor condition and needs some maintenance.")



