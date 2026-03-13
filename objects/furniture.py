#objects.furniture.py
from objects.InWorldObjects import ObjectInWorld, Toughness, ItemType, Size
from typing import Optional
from base.character import Character
from debug_utils import debug_print


class Furniture(ObjectInWorld):
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


class Table:
    pass

class Chair:
    pass

class CafeTable(Furniture):
    is_concrete = True

    def __init__(self, name="Cafe Table"):
        super().__init__(
            name=name,
            size=Size.LARGE,#Be cautious of adding untyped categorical attributes, ie str here
            seating_capacity=4,
            toughness=Toughness.DURABLE,
        )
        
    def has_any_occupants(self, location):
        #from objects.furniture import CafeChair

        chairs = [
            obj for obj in location.items.objects_present
            if isinstance(obj, CafeChair)
            and obj.table is self
            and not obj.is_free()
        ]
        return len(chairs) > 0

    def has_free_seating(self, location):
        #from objects.furniture import CafeChair

        chairs = [
            obj for obj in location.items.objects_present
            if isinstance(obj, CafeChair)
            and obj.table is self
            and obj.is_free()
        ]
        
        #TMP
        for obj in location.items.objects_present:
            if isinstance(obj, CafeChair) and obj.table is self:
                pass
                #debug_print(None, f"[CHAIR DEBUG] {obj.name} occupied_by={obj.occupied_by}")

        # TC2 rule: table must be completely empty
        if self.has_any_occupants(location):
            return False

        return len(chairs) > 0

    def get_free_chair(self, location):
        for obj in location.items.objects_present:
            if isinstance(obj, CafeChair) and obj.table is self and obj.is_free():
                return obj
    
    def occupied_chairs(self):
        return [c for c in self.chairs if c.occupied_by]
    
    @property
    def tags(self):
        return ["furniture", "table", "social", "surface"]


class CafeChair(Furniture):
    is_concrete = True

    def __init__(self, name="Cafe Chair"):
        super().__init__(
            name=name,
            size=Size.MEDIUM,
            seating_capacity=1,
            toughness=Toughness.NORMAL,
        )
        self.occupied_by: Optional["Character"] = None
        self.table = None

    def is_free(self):
        return self.occupied_by is None

    def occupy(self, npc):
        if self.occupied_by is None:
            self.occupied_by = npc
            return True
        return False

    def vacate(self):
        pass
    
    @property
    def tags(self):
        return ["furniture", "chair", "seating"]


class Sofa:
    #Be cautious of adding untyped categorical attributes, ie str here
    #see CafeTable
    pass

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