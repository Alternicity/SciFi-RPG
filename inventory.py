# Instead Inventory inheriting from another class, it contains instances
# of ObjectInWorld. This is a "has-a" relationship rather than an "is-a" relationship.
# Keeping the Inventory class standalone ensures modularity. You can later extend it to work with shops,
# NPCs, or even factions without tight coupling.

# The Inventory class can be reused for other entities like shops, factions, or NPCs without rewriting the logic
from weapons import Weapon

import logging
logging.basicConfig(level=logging.INFO)

class Inventory:
    """Manages a collection of items for characters, shops, or other entities."""

    def __init__(self, items=None, max_capacity=None, owner=None):
        """Initialize an inventory with optional maximum capacity."""
        self.items = {}  # key: item.name, value: item object
        self.max_capacity = max_capacity
        self.owner = owner
        
        if items:
            for item in items:
                self.add_item(item)

    def is_empty(self):
        return not bool(self.items)

    def _validate_item(self, item): #old code
        """Validate an item before adding or updating it."""
        if item is None:
            raise ValueError("Item cannot be None.")
        if not hasattr(item, "name"):
            raise ValueError("Item must have a 'name' attribute.")

    def find_item(self, item_name):
        """Find an item in the inventory by name."""
        for item in self.items.values():
            if item.name == item_name:
                return item
        return None

    def add_item(self, item, quantity=1):
        self._validate_item(item)

        if self.max_capacity and len(self.items) >= self.max_capacity:
            logging.warning(f"Inventory full. Can't add {item.name}")
            return False

        if item.name in self.items:
            existing_item = self.items[item.name]

            if hasattr(existing_item, "quantity"):
                existing_item.quantity += quantity
                logging.info(f"Updated {item.name} to quantity {existing_item.quantity}")
            else:
                logging.warning(f"{item.name} does not support quantity.")

            # Weapon logic
            if isinstance(item, Weapon) and self.owner:
                self.owner.weapons.append(item)
                self.update_primary_weapon()

        else:
            item.quantity = quantity
            self.items[item.name] = item
            #print(f"Added {item.name} to inventory with quantity {quantity}")

            # Weapon logic
            if isinstance(item, Weapon) and self.owner:
                self.owner.weapons.append(item)
                self.update_primary_weapon()

        return True


    def remove_item(self, item_name, quantity=1):
        item = self.items.get(item_name)
        if not item:
            logging.warning(f"{item_name} not found.")
            return False

        # Handle items with quantity
        if hasattr(item, "quantity"):
            if item.quantity > quantity:
                item.quantity -= quantity
                return True
            elif item.quantity == quantity:
                del self.items[item_name]
            else:
                logging.warning(f"Not enough {item_name}.")
                return False
        else:
            del self.items[item_name]

        # Clean up from owner's weapon list if it's a weapon
        if isinstance(item, Weapon) and self.owner:
            if item in self.owner.weapons:
                self.owner.weapons.remove(item)

            # Reevaluate primary weapon
            if self.owner.primary_weapon == item:
                if self.owner.weapons:
                    new_primary = max(
                        self.owner.weapons, key=lambda w: getattr(w, "damage", 0)
                    )
                    self.owner.primary_weapon = new_primary
                    print(f"{self.owner.name}'s primary weapon is now {new_primary.name}.")
                else:
                    self.owner.primary_weapon = None
                    print(f"{self.owner.name} now has no primary weapon.")

        return True

        
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
        if not self.owner or not self.owner.weapons:
            return

        best_weapon = max(self.owner.weapons, key=lambda w: getattr(w, "damage", 0))
        if self.owner.primary_weapon != best_weapon:
            self.owner.primary_weapon = best_weapon
            print(f"{self.owner.name}'s primary weapon is now {best_weapon.name}.")


# Example Usage
if __name__ == "__main__":
    inventory = Inventory(max_capacity=10)