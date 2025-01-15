# Instead Inventory inheriting from another class, it contains instances
# of ObjectInWorld. This is a "has-a" relationship rather than an "is-a" relationship.
# Keeping the Inventory class standalone ensures modularity. You can later extend it to work with shops,
# NPCs, or even factions without tight coupling.

# The Inventory class can be reused for other entities like shops, factions, or NPCs without rewriting the logic


import logging
logging.basicConfig(level=logging.INFO)

class Inventory:
    """Manages a collection of items for characters, shops, or other entities."""

    def __init__(self, max_capacity=None):
        """Initialize an inventory with optional maximum capacity."""
        self.items = []
        self.max_capacity = max_capacity

    def _validate_item(self, item):
        """Validate an item before adding or updating it."""
        if item is None:
            raise ValueError("Item cannot be None.")
        if not hasattr(item, "name"):
            raise ValueError("Item must have a 'name' attribute.")

    def find_item(self, item_name):
        """Find an item in the inventory by name."""
        for item in self.items:
            if item.name == item_name:
                return item
        return None

    def add_item(self, item, quantity=1):
        """Add an item to the inventory or update quantity if stackable.."""
        self._validate_item(item)

        if self.max_capacity and len(self.items) >= self.max_capacity:
            logging.warning(f"Inventory is full. Cannot add {item.name}.")
            return False
        # Check if item already exists (stackable)
        existing_item = self.find_item(item.name)
        if existing_item:
            if hasattr(existing_item, "quantity"):
                existing_item.quantity += quantity
                logging.info(f"{item.name} quantity updated to {existing_item.quantity}.")
            else:
                logging.warning(f"{item.name} does not support quantities.")
            return True
        
        # Add new item
        if hasattr(item, "quantity"):
            item.quantity = quantity
        self.items.append(item)
        logging.info(f"{item.name} added to the inventory.")
        return True

    def remove_item(self, item_name, quantity=1):
        """Remove an item or decrease its quantity if stackable."""
        item = self.find_item(item_name)
        if not item:
            logging.warning(f"{item_name} not found in inventory.")
            return False

        if hasattr(item, "quantity"):
            if item.quantity > quantity:
                item.quantity -= quantity
                logging.info(f"{quantity} of {item_name} removed. Remaining: {item.quantity}.")
                return True
            elif item.quantity == quantity:
                self.items.remove(item)
                logging.info(f"{item_name} completely removed from inventory.")
                return True
            else:
                logging.warning(f"Not enough {item_name} to remove. Current quantity: {item.quantity}.")
                return False
        else:
            self.items.remove(item)
            logging.info(f"{item_name} removed from inventory.")
            return True
        
    def display_inventory(self):
        """Display the inventory contents."""
        if not self.items:
            logging.info("Inventory is empty.")
            return
        logging.info("Inventory contents:")
        for item in self.items:
            if hasattr(item, "quantity"):
                print(f"- {item.name} (x{item.quantity})")
            else:
                print(f"- {item.name}")

# Example Usage
if __name__ == "__main__":
    inventory = Inventory(max_capacity=10)