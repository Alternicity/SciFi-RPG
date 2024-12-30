from inventory import Inventory
from faction import Faction
import random


class Store:
    def __init__(
        self, name, legality=True, cash=100, bank_card_cash=1000, security=None
    ):

        self.name = name
        self.inventory = Inventory()
        self.cash = cash
        self.legality = legality
        self.cash = cash
        self.bank_card_cash = bank_card_cash
        self.security = security if security else []

    def sell_item(self, buyer, item, price):
        if item in self.inventory.items and buyer.cash >= price:
            self.inventory.remove_item(item)
            buyer.inventory.add_item(item)
            buyer.cash -= price
            self.cash += price
            print(f"{buyer.name} bought {item.name} for {price}.")
        else:
            print(f"Transaction failed. Insufficient funds or item not available.")

    def issue_item(self, receiver, item, quantity=1):
        if item in self.inventory.items and buyer.cash >= price:
            buyer.inventory.add_item(item)
            buyer.cash -= price
            self.cash += price
            receiver.inventory.add_item(item)
            self.inventory.remove_item(item)

            print(f"{buyer.name} bought {item.name} for {price}.")
        else:
            print(f"Transaction failed: insufficient funds or item unavailable.")


class Stash(Store):
    def __init__(self, name):
        super().__init__(name, legality=False)
        self.hidden = True
        # affliated with gangs, and hidden

    def IssueItem(self, receiver, item, quantity):

        def add_item(self, dealer, item):
            if dealer.gang_affiliation:
                print(f"Dealer{dealer.name} adds {item.name} to stash.")

    def issue_item(self, dealer, item):
        if dealer.gang_affiliation:
            print(f"Dealer {dealer.name} retrieves {item.name} from stash.")


class Vendor(Store):

    def sell_item(self, buyer, item, base_price):
        price = base_price + random.randint(-5, 5)  # Simple dynamic pricing
        super().sell_item(
            buyer, item, price
        )  # Call the base class method with calculated price


class CorporateDepot(Store):
    def __init__(self, name, corporation, cash=5000, bank_card_cash=1000):
        super().__init__(name, legality=True, cash=cash, bank_card_cash=bank_card_cash)
        self.corporation = corporation

    def issue_item(
        self,
        receiver,
        item,
    ):
        if (
            receiver.status in ["high", "elite"]
            and receiver.corporation == self.corporation
        ):
            print(f"Issuing {item.name} to {receiver.name}.")
            self.inventory.remove_item(item)
            receiver.inventory.add_item(
                item
            )  # Works if receiver.inventory is an Inventory instance
        else:
            print(f"{receiever.name} does not meet the requirements for {item.name}.")


class Dealer(Store):
    def __init__(self, name, gang_affiliation, cash, bank_card_cash):
        super().__init__(name, legality=False, cash=cash, bank_card_cash=bank_card_cash)
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
