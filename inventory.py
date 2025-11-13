#inventory.py

from weapons import Weapon
from debug_utils import debug_print
import gc, traceback
import traceback
import logging
logging.basicConfig(level=logging.INFO)




class Inventory:
    """Manages a collection of items for characters, shops, or other entities."""

    def has_ranged_weapon(self):
        from weapons import RangedWeapon

        # Must iterate values, not keys
        for item in self.items.values():
            if isinstance(item, RangedWeapon):
                return True

        # Tag fallback
        for item in self.items.values():
            tags = getattr(item, "tags", [])
            if "ranged_weapon" in tags or ("weapon" in tags and "ranged" in tags):
                return True

        return False


    #code doesnt use recent npc attributes
    def has_melee_weapon(self):
        from weapons import MeleeWeapon

        items = list(self.items.values())

        # ✅ Direct type check
        for item in items:
            if isinstance(item, MeleeWeapon):
                return True

        # ✅ Tag fallback (if you use tags for melee items)
        for item in items:
            tags = getattr(item, "tags", [])
            if "melee_weapon" in tags or ("weapon" in tags and "melee" in tags):
                return True

        return False

    
    def update_weapon_flags(self):
        #you can call inventory.update_weapon_flags() whenever an item is added, removed, or evaluated
        from weapons import MeleeWeapon, RangedWeapon
        has_melee = any(isinstance(item, MeleeWeapon) for item in self.items)
        has_ranged = any(isinstance(item, RangedWeapon) for item in self.items)

        if hasattr(self.owner, "hasRangedWeapon"):
            self.owner.hasRangedWeapon = has_ranged
        if hasattr(self.owner, "hasMeleeWeapon"):
            self.owner.hasMeleeWeapon = has_melee
        if hasattr(self.owner, "isArmed"):
            self.owner.isArmed = has_melee or has_ranged

    def __init__(self, items=None, max_capacity=None, owner=None):
        """Initialize an inventory with optional maximum capacity."""

        self.items = {}  # key: item.name, value: item object
        """ self.items = ValidatingDict()
        self.items._is_inventory_dict = True """

        #self.items._is_inventory_dict = True
        self.max_capacity = max_capacity
        self.owner = owner
        self.primary_weapon = None
        self.weapons = []
        self.recently_acquired = [] 
        #You can let the AI treat new items with a kind of “spotlight” attention ie make it their attention_focus
        #Perhaps recently_acquired could be a dictionary of Object/Time entries, and the clear_recently_acquired can work on how many
        #  (sim) days the object has been in inventory
        #This might also be of eventual use in economy.py as shops use class Inventory as well.
        
        # Debug hook: store stack trace where this Inventory was created
        # (temporary; remove after you fix origin)
        try:
            self._creation_stack = traceback.format_stack(limit=6)
        except Exception:
            self._creation_stack = ["<no stack available>"]
        
        if items:
            for item in items:
                self.add_item(item)

    def ensure_owner(self, fallback=None):
        npc =self.owner.npc
        if not getattr(self, "owner", None):
            if fallback:
                self.owner = fallback
            elif hasattr(self, "_owner_name"):
                self.owner = self._owner_name
            else:
                debug_print(npc, f"[inventory] Warning: Inventory {id(self)} still ownerless after ensure_owner()", category ="inventory")


    def clear_recently_acquired(self, current_day=None):
        if current_day is None:
            from create_game_state import get_game_state
            current_day = get_game_state().day

        cleaned = []
        for entry in self.recently_acquired:
            # New format: (item, day_added)
            if isinstance(entry, tuple) and len(entry) == 2:
                item, day_added = entry
                if current_day - day_added < 1:
                    cleaned.append((item, day_added))

            # Old format: just the item (keep it one more day so nothing breaks)
            else:
                cleaned.append((entry, current_day))  # normalize it

        self.recently_acquired = cleaned

    def is_empty(self):
        return not bool(self.items)

    def _validate_item(self, item): #old code
        """Validate an item before adding or updating it."""
        if item is None:
            raise ValueError("Item cannot be None.")
        if isinstance(item, (str, int, float, bool)):
            raise ValueError(f"Invalid item type {type(item).__name__} — inventory items must be objects.")

        if not hasattr(item, "name"):
            raise ValueError("Item must have a 'name' attribute.")


    def find_item(self, item_name):
        """Find an item in the inventory by name."""
        for item in self.items.values():
            if item.name == item_name:
                return item
        return None

    def add_item(self, item, quantity=1):

        if self.max_capacity and len(self.items) >= self.max_capacity:
            logging.warning(f"Inventory full. Can't add {item.name}")
            return False
        
        if not hasattr(item, "name"):
            raise ValueError("Inventory.add_item expects an object with a 'name' attribute.")

        if isinstance(item, str):
            raise TypeError("Inventory ERROR: attempted to add string into inventory.")

        """ if isinstance(item, dict):
            raise TypeError("Raw dict inserted into inventory.") """

        if item.name in self.items:
            existing_item = self.items[item.name]

            # ✅ If item is a weapon, NEVER stack quantities
            if isinstance(item, Weapon):
                # Treat each weapon as a separate object
                new_item = item
                self.items[f"{item.name}_{id(new_item)}"] = new_item
                self.weapons.append(new_item)
                if self.owner:
                    self.update_primary_weapon()
                    return True

                logging.info(f"Updated {item.name} to quantity {existing_item.quantity}")
            else:
                logging.warning(f"{item.name} does not support quantity.")

            # Weapon logic
            if isinstance(item, Weapon) and self.owner:
                self.weapons.append(item)
                self.update_weapon_flags()
                self.update_primary_weapon()
            if "weapon" in item.tags:
                self.recently_acquired.append(item)

        else:
            item.quantity = quantity
            self.items[item.name] = item
            #print(f"Added {item.name} to inventory with quantity {quantity}")

            # Weapon logic
            if isinstance(item, Weapon) and self.owner:
                self.weapons.append(item)
                self.update_primary_weapon()

        return True

    def has_item(self, item) -> bool:
        return item in self.items.values()
        #If items is a dict keyed by name, you can do:
        """ def has_item(self, item) -> bool:
            return item.name in self.items """

    def add_recently_acquired(self, item, state):
        # Always insert in canonical (item, day) format
        self.recently_acquired.append((item, state.day))

    def has_recently_acquired(self, item_type_or_tag: str) -> bool:
        for item in self.recently_acquired:
            tags = getattr(item, "tags", [])
            if item_type_or_tag in tags:
                return True
        return False

    def has_illegal_items(self):
        """Returns True if any item in the inventory is illegal (legality=False)."""
        return any(not item.legality for item in self.items.values())

    def remove_item(self, item_name, quantity=1):
    
        item = self.items.get(item_name)
        if not item:
            return None

        # For weapons / non-stackable, remove exact key
        if isinstance(item, Weapon):
            key_to_remove = next((k for k, v in self.items.items() if v is item), None)
            if key_to_remove:
                return self.items.pop(key_to_remove)
            else:
                return None
        else:
            # For stackable items
            removed_quantity = min(quantity, getattr(item, "quantity", 1))
            item.quantity -= removed_quantity
            if item.quantity <= 0:
                self.items.pop(item_name)
            return item

    def display_inventory(self):
        if not self.items:
            print("Inventory is empty.")
            return
        print("Inventory contents:")
        for item in self.items.values():
            q = getattr(item, "quantity", "N/A")
            print(f"- {item.name} (x{q})")
            
    def get_inventory_summary(self):
        if not self.items:
            return "(inv Empty)"
        return ", ".join(f"{item.name} (x{getattr(item, 'quantity', 1)})" for item in self.items.values())

    # make Inventory itself iterable:
    def __iter__(self):
        return iter(self.items.values())

    def update_primary_weapon(self):
        from base_classes import Character, Location

        # If  there are no weapons → nothing to do
        if not self.weapons:
            return

        # Pick the best weapon by damage (default 0 if missing)
        best_weapon = max(self.weapons, key=lambda w: getattr(w, "damage", 0))

        # If the owner is a Location → update and print
        if isinstance(self.owner, Location):
            # update the primary weapon silently if needed
            
                self.primary_weapon = best_weapon
                #possibly illogical
                #self.owner.primary_weapon = best_weapon
                #possibly illogical

                #so which of the preceding loines is correct. A Shop has an inventory

                #debug_print(self.owner, f"{self.owner.name}'s primary weapon is now {best_weapon.name}.", category="inventory")
                return

        # If the owner is a Character → update and print
        if isinstance(self.owner, Character):
            if self.primary_weapon != best_weapon:
                self.primary_weapon = best_weapon
                # ✅ FIX: write back into the Character object
                self.owner.primary_weapon = best_weapon
                debug_print(self.owner, f"[INV] Primary weapon now {best_weapon.name}", category="inventory")
            
#inventory.py
#added as a utility function after class Inventory
# --- DEBUG LAYER FOR add_item() ---
_old_add_item = Inventory.add_item

def debug_add_item(self, item, quantity=1):
    if isinstance(item, str):
        import traceback
        print("\n***** STRING DETECTED IN add_item *****")
        print(f"Bad value: {item!r}")
        print("STACK:")
        print("".join(traceback.format_stack()))
        print("**************************************\n")
    return _old_add_item(self, item, quantity)

Inventory.add_item = debug_add_item

# Example Usage
if __name__ == "__main__":
    inventory = Inventory(max_capacity=10)