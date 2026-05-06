#objects.furniture.py
from objects.InWorldObjects import ObjectInWorld, Toughness, ItemType, Size
from typing import Optional
from base.character import Character
from debug_utils import debug_print
from social.social_utils import social_scan

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