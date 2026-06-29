#objects.furniture.py
from objects.InWorldObjects import ObjectInWorld, Toughness, ItemType, Size
from typing import Optional
from base.character import Character
from debug_utils import debug_print
#from social.social_utils import social_scan

class Furniture(ObjectInWorld):
    #Add ambience?
    is_concrete = False

    def __init__(
        self,
        name,
        size,
        toughness=Toughness.DURABLE,
        seating_capacity=0,
        
        **kwargs
    ):
        super().__init__(
            name=name,
            toughness=toughness,
            item_type=ItemType.FURNITURE,
            size=size,
            blackmarket_value=0,
            price=0,
            legality=True,
            **kwargs
        )

        self.seating_capacity = seating_capacity
        self.occupants = []          # list[Character]
        self.surface_items = []      # for food, phones, etc.

    # ---------------------------
    # Occupancy
    # ---------------------------

    def has_free_seat(self):
        return len(self.occupants) < self.seating_capacity

    def seat(self, character):
        if not self.has_free_seat():
            return False
        self.occupants.append(character)
        return True

    def leave(self, character):
        if character in self.occupants:
            self.occupants.remove(character)

    # ---------------------------
    # Tags
    # ---------------------------

    @property
    def tags(self):
        base = ["furniture"]
        if self.seating_capacity > 0:
            base.append("seating")
        return base

    # ---------------------------
    # Percepts
    # ---------------------------

    def get_percept_data(self, observer=None):
        data = super().get_percept_data(observer)

        if self.occupants:
            occupant_names = ", ".join(o.name for o in self.occupants)
            data["description"] = f"{self.name} (Occupied: {occupant_names})"
        else:
            data["description"] = f"{self.name}"

        data["origin"] = self
        return data


class Table(Furniture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chairs = []

    def add_chair(self, chair):
        chair.table = self
        self.chairs.append(chair)

    def get_occupants(self):
        return [c.occupied_by for c in self.chairs if c.occupied_by]

    def has_free_seat(self):
        return any(c.is_free() for c in self.chairs)

    def get_free_chair(self):
        for c in self.chairs:
            if c.is_free():
                return c

class Chair(Furniture):
    is_concrete = False  # base class

    def __init__(self, name="Chair", size=Size.MEDIUM, toughness=Toughness.NORMAL):
        super().__init__(
            name=name,
            size=size,
            seating_capacity=1,
            toughness=toughness,
        )
        self.occupied_by: Optional["Character"] = None
        self.table = None  # optional link (can be None)

    def is_free(self):
        return self.occupied_by is None

    def occupy(self, npc):
        if self.occupied_by is None:
            self.occupied_by = npc
            npc.current_chair = self

            # Only set if part of a table
            if self.table:
                npc.seated_at = self.table

            return True
        return False

    def vacate(self):
        npc = self.occupied_by
        if npc:
            npc.current_chair = None
            npc.seated_at = None

            # FIX: avoid hard dependency
            if hasattr(npc, "social_scan"):
                npc.social_scan()

        self.occupied_by = None

    @property
    def tags(self):
        return ["furniture", "chair", "seating"]

class CafeTable(Furniture):
    is_concrete = True
    
    def __init__(self, name="Cafe Table"):
        super().__init__(
            name=name,
            size=Size.LARGE,#Be cautious of adding untyped categorical attributes, ie str here
            seating_capacity=4,
            toughness=Toughness.DURABLE,
        )
        self.chairs = []
    
    def has_any_occupants(self, location):
        return any(c.occupied_by for c in self.chairs)

    def has_free_seating(self, location):

        # TC2 rule: table must be completely empty
        if self.has_any_occupants(location):
            return False

        return any(c.is_free() for c in self.chairs)

    def get_free_chair(self):
        for chair in self.chairs:
            if chair.is_free():
                return chair
    
    def occupied_chairs(self):
        return [c for c in self.chairs if c.occupied_by]
    
    @property
    def tags(self):
        return ["furniture", "table", "social", "surface"]


class CafeChair(Chair):
    is_concrete = True

    def __init__(self, name="Cafe Chair"):
        super().__init__(
            name=name,
            size=Size.MEDIUM,
            toughness=Toughness.NORMAL,
        )

class Bench(Chair):
    is_concrete = True

    def __init__(self, name="Bench", capacity=2):
        super().__init__(name=name, size=Size.LARGE, toughness=Toughness.DURABLE)
        self.seating_capacity = capacity

class Sofa(Chair):
    is_concrete = True

    def __init__(self, name="Sofa", capacity=3):
        super().__init__(
            name=name,
            size=Size.LARGE,
            toughness=Toughness.DURABLE,
        )
        self.seating_capacity = capacity
    #Be cautious of adding untyped categorical attributes, ie str here
    #see CafeTable


class CafeCounter(Furniture):
    is_concrete = True

    def __init__(self, name="Cafe Counter"):
        super().__init__(
            name=name,
            size=Size.LARGE,
            seating_capacity=1,  # manager behind counter
            toughness=Toughness.DURABLE,
        )

        self.display_items = []     # visible goods
        self.concealed_items = []   # hidden storage

    @property
    def tags(self):
        return ["furniture", "counter", "service", "surface"]

    def add_display_item(self, item):
        self.display_items.append(item)

    def add_concealed_item(self, item):
        self.concealed_items.append(item)

    def get_percept_data(self, observer=None):
        data = super().get_percept_data(observer)

        if self.display_items:
            item_names = ", ".join(i.name for i in self.display_items)
            data["description"] += f" (Display: {item_names})"

        return data

# objects/furniture.py

class Bed(Furniture):
    is_concrete = True

    def __init__(self, name="Bed", capacity=1):
        super().__init__(
            name=name,
            size=Size.LARGE,
            toughness=Toughness.DURABLE,
            seating_capacity=capacity,
        )
        self.occupied_by = None
        self.base_ambience = {"peace": 0.3, "rest": 0.4}

    def is_free(self):
        return self.occupied_by is None

    def occupy(self, npc):
        if self.is_free():
            self.occupied_by = npc
            npc.current_bed = self
            return True
        return False

    def vacate(self):
        if self.occupied_by:
            self.occupied_by.current_bed = None
        self.occupied_by = None

    @property
    def tags(self):
        return ["furniture", "bed", "rest", "sleep"]
    

from objects.InWorldObjects import Size, Toughness
from enum import Enum

class FridgeTemp(Enum):
    COLD = "cold"
    FREEZER = "freezer"

class Fridge(Furniture):
    def __init__(
        self,
        name="Refrigerator",
        size=Size.LARGE,
        toughness=Toughness.DURABLE,
        seating_capacity=0,
        has_freezer=True,
        freezer_temp=-18,
        fridge_temp=4,
        current_temp_mode=FridgeTemp.COLD,
        is_plugged_in=True,
        is_cooling=True,
        **kwargs
    ):
        super().__init__(
            name=name,
            size=size,
            toughness=toughness,
            seating_capacity=seating_capacity,
            **kwargs
        )
        
        # Fridge-specific attributes
        self.has_freezer = has_freezer
        self.freezer_temp = freezer_temp  # in Celsius
        self.fridge_temp = fridge_temp    # in Celsius
        self.current_temp_mode = current_temp_mode
        self.is_plugged_in = is_plugged_in
        self.is_cooling = is_cooling
        
        # Storage compartments
        self.fridge_contents = []      # Perishable and non-perishable items
        self.freezer_contents = []     # Frozen items (if has_freezer)
        self.door_shelves = []         # For eggs, butter, condiments
        
        # State tracking
        self.current_temperature = fridge_temp
        self.is_door_open = False
        self.light_on = False
        self.power_consumption = 150    # Watts
        self.cleanliness = 100          # 0-100 scale
        self.last_defrost_time = 0      # Sim time
        
    def open_door(self):
        """Open the fridge door"""
        if not self.is_door_open:
            self.is_door_open = True
            self.light_on = True
            print(f"{self.name} door opened. Light turns on.")
            return True
        return False
    
    def close_door(self):
        """Close the fridge door"""
        if self.is_door_open:
            self.is_door_open = False
            self.light_on = False
            print(f"{self.name} door closed. Light turns off.")
            return True
        return False
    
    def add_item(self, item, location="fridge"):
        """Add an item to the fridge"""
        if location == "fridge":
            self.fridge_contents.append(item)
        elif location == "freezer" and self.has_freezer:
            self.freezer_contents.append(item)
        elif location == "door":
            self.door_shelves.append(item)
        else:
            return False
        print(f"{item.name} added to {self.name} {location}")
        return True
    
    def remove_item(self, item, location="fridge"):
        """Remove an item from the fridge"""
        if location == "fridge" and item in self.fridge_contents:
            self.fridge_contents.remove(item)
            return item
        elif location == "freezer" and self.has_freezer and item in self.freezer_contents:
            self.freezer_contents.remove(item)
            return item
        elif location == "door" and item in self.door_shelves:
            self.door_shelves.remove(item)
            return item
        return None
    
    def set_temperature(self, temp, mode=None):
        """Set the temperature of the fridge"""
        if mode is None:
            mode = self.current_temp_mode
            
        if mode == FridgeTemp.COLD:
            self.fridge_temp = temp
            self.current_temperature = temp
        elif mode == FridgeTemp.FREEZER and self.has_freezer:
            self.freezer_temp = temp
            if self.current_temp_mode == FridgeTemp.FREEZER:
                self.current_temperature = temp
        
        print(f"{self.name} {mode.value} temperature set to {temp}°C")
        return True
    
    def toggle_power(self):
        """Turn fridge on/off"""
        self.is_plugged_in = not self.is_plugged_in
        self.is_cooling = self.is_plugged_in
        
        status = "on" if self.is_plugged_in else "off"
        print(f"{self.name} turned {status}")
        
        if not self.is_plugged_in:
            self.light_on = False
        return self.is_plugged_in
    
    def defrost(self):
        """Defrost the freezer compartment"""
        if self.has_freezer:
            self.last_defrost_time = 0  # Reset in sim time
            self.cleanliness = min(100, self.cleanliness + 20)
            print(f"{self.name} freezer defrosted and cleaned")
            return True
        return False
    
    def clean(self):
        """Clean the fridge interior"""
        self.cleanliness = 100
        print(f"{self.name} is now sparkling clean")
        return True
    
    def get_contents_summary(self):
        """Get a summary of all items in the fridge"""
        summary = {
            "fridge_items": [item.name for item in self.fridge_contents],
            "freezer_items": [item.name for item in self.freezer_contents],
            "door_items": [item.name for item in self.door_shelves],
            "total_items": len(self.fridge_contents) + len(self.freezer_contents) + len(self.door_shelves)
        }
        return summary
    
    def update(self, sim_time=None):
        """Update fridge state (called each sim tick)"""
        if not self.is_plugged_in:
            # Warming up when unplugged
            self.current_temperature += 0.1
            return
        
        if sim_time:
            # Regular maintenance tracking
            self.last_defrost_time += 1
            
            # Auto-defrost reminder after 30 days
            if self.last_defrost_time > 30 and self.has_freezer:
                print(f"{self.name} freezer needs defrosting!")
    
    def __str__(self):
        door_status = "open" if self.is_door_open else "closed"
        power_status = "on" if self.is_plugged_in else "off"
        return (f"{self.name} ({self.size.value}) - Door: {door_status}, "
                f"Power: {power_status}, Temp: {self.current_temperature}°C, "
                f"Cleanliness: {self.cleanliness}%")

class DJBooth(Furniture):
    is_concrete = True

    def __init__(self):
        super().__init__(
            name="DJ Booth",
            size=Size.LARGE,
            toughness=Toughness.DURABLE
        )

    @property
    def tags(self):
        return ["music", "entertainment", "nightclub"]