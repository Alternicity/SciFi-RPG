import random
import string

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

class Location:
    def __init__(self, name, location_type, side, security_level, condition, fun=0, **kwargs):
        self.name = name
        self.location_type = location_type
        self.side = side
        self.security_level = security_level
        self.condition = condition
        self.fun = fun
        self.is_concrete = False  # Default value, can be overridden in subclasses
        self.secret_entrance = False  # Default value, can be overridden
        # Handle additional properties dynamically based on kwargs (for flexibility)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_secret_entrance(self, entrance):
        self.secret_entrance = entrance


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

class HQ(Location):
    def __init__(self, name, side, security_level, condition, defense_rating, resource_storage=None, special_features=None, fun=0):
        super().__init__(name, "HQ", side, security_level, condition, fun)
        self.security_level = security_level
        self.resource_storage = resource_storage or {}
        self.special_features = special_features or []
        self.entrances = []
        self.is_concrete = True
        self.secret_entrance = True

    def add_entrances(self, *entrances):
        self.entrances.extend(entrances)
        print(f"Entrances added to {self.name}: {', '.join(entrances)}")

    
class Vendor(Location):
    def __init__(self, name, location, security_level, upkeep, items_available):
        super().__init__(name, location, security_level, upkeep)
        self.items_available = items_available  # Items that the vendor has available for sale
        self.is_concrete = False
        self.secret_entrance = True

class Shop(Vendor):
    def __init__(self, name, location, security_level, upkeep, items_available, fun):
        super().__init__(name, location, security_level, upkeep, items_available, fun)
        self.is_concrete = True
        self.secret_entrance = False

    def sell_item(self, character, item):
        if item in self.items_available:
            print(f"Item {item} sold to {character.name}")
            # Add item to character's inventory (or some similar behavior)
        else:
            print(f"Item {item} not available")
        
class CorporateStore(Vendor):
    def __init__(self, name, location, security_level, upkeep, items_available, required_status):
        super().__init__(name, location, security_level, upkeep, items_available)
        self.required_status = required_status  # Minimum status required to buy
        self.is_concrete = True
        self.secret_entrance = False

    def sell_item(self, character, item):
        if character.status >= self.required_status:
            if item in self.items_available:
                print(f"Corporate item {item} sold to {character.name}")
                # Add item to character's inventory (or some similar behavior)
            else:
                print(f"Item {item} not available")
        else:
            print(f"{character.name} does not have sufficient status to buy {item}")

class RepairWorkshop(Location):
    def __init__(self, name, location, security_level, upkeep, materials_required):
        super().__init__(name, location, security_level, upkeep)
        self.materials_required = materials_required  # Materials required for repairs
        self.is_concrete = True
        self.secret_entrance = False

    @abstractmethod
    def repair_item(self, item):
        pass


class MechanicalRepairWorkshop(RepairWorkshop):
    def __init__(self, name, location, security_level, upkeep, materials_required):
        super().__init__(name, location, security_level, upkeep, materials_required)
        self.is_concrete = True
        self.secret_entrance = False

    def repair_item(self, item):
        print(f"Repairing mechanical item {item} at {self.name}.")
        # Repair logic for mechanical items

class ElectricalRepairWorkshop(RepairWorkshop):
    def __init__(self, name, location, security_level, upkeep, materials_required):
        super().__init__(name, location, security_level, upkeep, materials_required)
    
    def repair_item(self, item):
        print(f"Repairing electrical item {item} at {self.name}.")
        # Repair logic for electrical items


class Stash(Location):
    def __init__(self, name, location, security_level, upkeep):
        super().__init__(name, location, security_level, upkeep)
        self.stored_items = []  # List of items hidden in the stash
        self.is_concrete = True
        self.secret_entrance = True

    def store_item(self, item):
        self.stored_items.append(item)
        print(f"Item {item} stored in stash")
    
    def retrieve_item(self, item):
        if item in self.stored_items:
            self.stored_items.remove(item)
            print(f"Item {item} retrieved from stash")
        else:
            print(f"Item {item} not found in stash")

class Factory(Location):
    def __init__(self, name, location, security_level, upkeep, materials_available, goods_produced, fun):
        super().__init__(name, location, security_level, upkeep)
        self.materials_available = materials_available  # Materials that the factory receives
        self.goods_produced = goods_produced  # Goods produced by the factory
        self.is_concrete = True
        self.secret_entrance = False

    def produce_goods(self):
        print(f"Factory at {self.name} is producing goods.")
        # Logic for processing materials into goods
        for material in self.materials_available:
            # Example: produce goods based on materials
            self.goods_produced.append(f"Produced {material} good")
            print(f"Produced {material} good")



class Nightclub(Location):
    def __init__(self, name, side, security_level, condition, fun):
        super().__init__(name, "Nightclub", side, security_level, condition, fun)
        self.is_concrete = True
        self.secret_entrance = True

    @check_entrance_state
    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
        func()


class Mine(Location):
    def __init__(self, name, side, security_level, condition, fun):
        super().__init__(name, "Mine", side, security_level, condition, fun)
        self.is_concrete = True
        self.secret_entrance = True

    @check_entrance_state
    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
        func()


class Powerplant(Location):
    def __init__(self, name, side, security_level, condition, energy_output, fun=-1):
        super().__init__(name, "Powerplant", side, security_level, condition, fun)
        self.energy_output = energy_output
        self.connected_locations = []
        self.is_concrete = True
        self.secret_entrance = True

    @check_entrance_state
    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
        func()

    def distribute_energy(self):
        energy_per_location = self.energy_output // len(self.connected_locations)
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


class Airport(Location):
    def __init__(self, name, side, security_level, condition, connected_locations, import_capacity, materials_inventory, fun=0):
        super().__init__(name, "Airport", side, security_level, condition, fun)
        self.connected_locations = connected_locations
        self.import_capacity = import_capacity
        self.materials_inventory = materials_inventory
        self.is_concrete = True
        self.secret_entrance = True

    @check_entrance_state
    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
        func()

    def import_materials(self, amount):
        if isinstance(amount, dict):  # Ensure amount is a dictionary
            print(f"Importing materials: {amount}")
            for material, qty in amount.items():
                if material in self.materials_inventory:
                    self.materials_inventory[material] += qty
                else:
                    self.materials_inventory[material] = qty
        else:
            print("Error: 'amount' should be a dictionary of materials.")


class Port(Location):
    def __init__(self, name, side, security_level, condition, connected_locations, import_capacity, materials_inventory, fun):
        super().__init__(name, "Port", side, security_level, condition, fun)
        self.connected_locations = connected_locations
        self.import_capacity = import_capacity
        self.materials_inventory = materials_inventory
        self.is_concrete = True
        self.secret_entrance = True

    @check_entrance_state
    def secret_entrance_decorator(self, func):
        """Decorator method to allow access based on entrance state."""
        func()

    def import_materials(self, amount):
        if isinstance(amount, dict):  # Ensure amount is a dictionary
            print(f"Importing materials: {amount}")
            self.materials_inventory += sum(amount.values())  # Adjusted for simplicity
        else:
            print("Error: 'amount' should be a dictionary of materials.")


class Factory(Location):
    def __init__(self, name, side, security_level, condition, raw_materials_needed, output_rate, energy_needed, workers_needed=5, fun=-1):
        super().__init__(name, "Factory", side, security_level, condition, fun)
        self.raw_materials_needed = raw_materials_needed
        self.output_rate = output_rate
        self.energy_needed = energy_needed
        self.workers_needed = workers_needed
        self.workers_present = 0  # Updated dynamically
        self.products = 0  # Add this attribute to track produced goods
        self.is_concrete = True
        self.secret_entrance = False

    def can_produce(self):
        """Check if the factory can produce goods."""
        return self.is_powered and self.workers_present >= self.workers_needed and self.raw_materials_needed > 0

    def produce_goods(self):
        """Produce goods if conditions are met."""
        if self.can_produce():
            self.products += self.output_rate
            self.raw_materials_needed -= 1
            logging.info(f"{self.name} produced {self.output_rate} goods.")
        else:
            logging.warning(f"{self.name} cannot produce goods. Not enough workers, power, or raw materials.")

class Cafe(Location):
    def __init__(self, name, location, security_level, upkeep, fun):
        super().__init__(name, location, security_level, upkeep)
        self.ambiance_level = ambiance_level  # Level of ambiance or mood of the cafe
        self.is_concrete = True
        self.secret_entrance = False

    def serve_customer(self, character):
        print(f"{character.name} is enjoying the ambiance at {self.name}.")
        # Further logic for interaction with customers


class Park(Location):
    def __init__(self, name, side, security_level, condition, fun):
        super().__init__(name, "Park", side, security_level, condition, fun)
        self.is_concrete = True
        self.secret_entrance = False


# Example use case
hq = HQ(
    name="Alpha HQ",
    side="East Side",
    security_level="High",
    condition="Well Maintained",
    fun = 1,
)
hq.add_entrances("Main Entrance", "Side Door")
hq.set_secret_entrance("Underground Tunnel")

# Accessing the secret entrance via decorator
hq.secret_entrance_decorator(lambda: print("Entered secret section!"))()

print(hq)
