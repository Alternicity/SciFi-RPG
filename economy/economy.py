#economy.economy.py
import json
import os
import logging
from location.locations import Shop
import random
from objects.InWorldObjects import Wallet
from dataclasses import dataclass
from typing import Any, Literal

logging.basicConfig(level=logging.INFO)

#this is one of the first two places i want to incorporate scalar fields

@dataclass
class Ownership:
    owner_type: Literal["family", "gang", "corporation", "state"]#these are showing as not defined, despite looking like strings here
    owner_ref: Any  # Family, Gang, Corporation, etc. 
    share: float = 1.0  # Later: partial ownership


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
    
    def assign_workers_to_locations(characters, all_locations):
        """
        Assign workers to locations based on their workforce needs.
        """
        for location in all_locations:
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


