def display_inventory(self):
        """Display items and their prices."""
        print(f"{self.name}'s Shop Inventory:")
        for item, details in self.inventory.items():
            print(f"{item}: ${details['price']} (Quantity: {details['quantity']})")



def     :
    """Display inventory of a specific shop."""
    print(f"\nShop: {shop.name}")
    inventory = shop.inventory
    if inventory:
        inventory_table = [
            [item, details.get("price", "N/A"), details.get("quantity", 0)]
            for item, details in inventory.items()
        ]
        print(tabulate(inventory_table, headers=["Item", "Price", "Quantity"], tablefmt="grid"))
    else:
        print("This shop has no items available.")