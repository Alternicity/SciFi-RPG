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

    def add_item(self, item):
        """Add an item to the inventory."""
        self._validate_item(item)
        if self.max_capacity and len(self.items) >= self.max_capacity:
            logging.warning(f"Inventory is full. Cannot add {item.name}.")
            return
        self.items.append(item)
        logging.info(f"{item.name} added to the inventory.")

    def update_quantity(self, item, quantity):
        """Update the quantity of a stackable item."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self._validate_item(item)
        for inv_item in self.items:
            if inv_item.name == item.name:
                if hasattr(inv_item, "quantity"):
                    inv_item.quantity += quantity
                    logging.info(f"{item.name} quantity updated to {inv_item.quantity}.")
                else:
                    logging.warning(f"{item.name} does not support quantities.")
                return
        logging.warning(f"{item.name} not found in inventory.")