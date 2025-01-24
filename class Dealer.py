class Dealer(Store):
    def __init__(self, name, gang_affiliation, cash, bankCardCash):
        super().__init__(name, legality=False, cash=cash, bankCardCash=bankCardCash)
        self.gang_affiliation = gang_affiliation

    def issue_item(self, receiver, item, price=None):
        # Issues an item to a character based on conditions.
        # If the receiver is a gang member and the item is a weapon, it's free.
        # Otherwise, the item is sold at the given price.
        if item in self.inventory.items:  # Check if the item is in inventory
            # Check if the receiver is in the same gang and if the item is a weapon
            if (
                receiver.gang_membership == self.gang_affiliation
                and item.type == "weapon"
            ):
                # Issue weapon for free to gang members
                print(f"Issuing {item.name} to gang member {receiver.name}.")
                self.inventory.remove_item(item)
                receiver.inventory.add_item(item)
            elif price is not None and receiver.cash >= price:
                # Sell the item for cash
                print(f"{receiver.name} buys {item.name} for {price}.")
                self.inventory.remove_item(item)
                receiver.inventory.add_item(item)
                receiver.cash -= price
                self.cash += price
            else:
                print(f"{receiver.name} cannot afford {item.name}.")
        else:
            print(f"{item.name} is not available.")