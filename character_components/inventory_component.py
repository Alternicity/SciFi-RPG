#character_components.inventory_components.py

from weapons import Weapon

class InventoryComponent:
    def __init__(self, character, initial_items=None):
        from inventory import Inventory
        self.character = character
        self.inventory = Inventory(items=initial_items, owner=character)
        #this line is different from your example code, and appears to be where Inventory is currently getting
        #instantiated

    def has_recently_acquired(self, tag: str) -> bool:
        return self.inventory.has_recently_acquired(tag)

    def clear_recently_acquired(self):
        return self.inventory.clear_recently_acquired()

    def add_item(self, item, quantity=1):#ADDS OWNERSHIP
        item.owner = self.owner.name
        self.items.append(item)

        return self.inventory.add_item(item)

    def has_item(self, item):
        return self.inventory.has_item(item)

    def update_primary_weapon(self):
        return self.inventory.update_primary_weapon()
