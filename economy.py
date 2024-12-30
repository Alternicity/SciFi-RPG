import logging
logging.basicConfig(level=logging.INFO)
logging.info(f"{char.name} earned money at {char.current_location.name}.")


class EconomyManager:
    def __init__(self):
        self.power_stations = []
        self.ports = []
        self.factories = []
        self.shops = []

    def run_daily_simulation(self):
        for station in self.power_stations:
            station.distribute_energy()

        for port in self.ports:
            port.import_materials()

        for factory in self.factories:
            factory.produce_goods()

        for shop in self.shops:
            self.simulate_shop_sales(shop)

    def simulate_shop_sales(self, shop):
        # Simulate random sales
        for product in shop.products_for_sale.keys():
            quantity_sold = min(shop.products_for_sale[product], random.randint(1, 5))
            revenue = shop.sell_goods(product, quantity_sold)
            print(f"Shop {shop.name} sold {quantity_sold} of {product} for revenue: {revenue}")
    
    def assign_workers_to_locations(characters, locations):
    """
    Assign workers to locations based on their workforce needs.
    """
    for location in locations:
        required_workers = location.required_workers
        assigned_workers = 0

        for char in characters:
            if assigned_workers >= required_workers:
                break
            if char.role == 'Worker' and not char.is_working:
                char.current_location = location
                char.is_working = True
                location.add_worker(char)  # A method to register workers in a location
                assigned_workers += 1

        if assigned_workers < required_workers:
            print(f"Location {location.name} is understaffed. Needed: {required_workers}, Assigned: {assigned_workers}.")

    
    #Generate and Distribute Energy:    
    #Import Raw Materials: Ports/Airports bring in resources to supply factories.
    #Factory Production: Factories use raw materials and energy to produce goods.
    #Shop Sales: Shops sell goods to characters or factions, generating money.

def calculate_item_cost(self, item):
        """
        Determine the cost of an item based on its legality.
        """
        if not hasattr(item, "legality"):
            raise ValueError("The item must have a 'legality' attribute.")
        return item.value if item.legality == True else item.blackmarket_value


    #possibly deprecated, legacy code
    def buy(self, item, use_bank_card=False):
        amount = self.calculate_item_cost(item)

        # Check legality, which is now a boolean (True/False)
        if item.legality is True:
            self.make_normal_purchase(amount, use_bank_card)
        elif item.legality is False:
            self.make_black_market_purchase(amount)
        else:
            raise ValueError(f"Unknown legality type: {item.legality}")
        

        def make_black_market_purchase(self, amount):
        """Make a purchase on the black market (only cash can be used)."""
        if self.wallet.spend_cash(amount):
            print(f"Black market purchase of {amount} successful.")
        else:
            print(f"Not enough cash for black market purchase.")

    def make_normal_purchase(self, amount, use_bank_card=False):
        """Make a normal purchase, either using cash or bank card."""
        if use_bank_card:
            if self.wallet.spend_bank_card_cash(amount):
                print(f"Purchase of {amount} using bank card successful.")
            else:
                print(f"Not enough bank card balance for purchase.")
        else:
            if self.wallet.spend_cash(amount):
                print(f"Purchase of {amount} using cash successful.")
            else:
                print(f"Not enough cash for purchase.")

    def pick_up_cashwad(self, cashwad):
        """Pick up a CashWad and add the value to the wallet."""
        print(f"Picked up a CashWad worth {cashwad.get_value()} cash.")
        cashwad.add_to_wallet(self.wallet)

    def print_wallet(self):
        """Print the wallet's current balance (for debugging purposes)."""
        print(f"Cash in wallet: {self.wallet.cash}")
        print(f"Bank card balance: {self.wallet.bank_card_cash}")

        #possibly deprecated function, pasted here
    def get_total_money(self):
    """Return the total money available (cash + bank card)."""
    return self.wallet.total_balance()