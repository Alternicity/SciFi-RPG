import sys
import os
import json
import random
from dataclasses import asdict
import logging
import weapons
import InWorldObjects

from common import get_project_root, get_file_path
#ALL files use this to get the project root


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from location import Shop, Stash, Vendor, CorporateStore, Security

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sample item pools for inventory generation
ITEM_POOLS = {
    "low": ["Pistol", "SmartPhone", "Shotgun", "Knife", "Sword", "Club"],
    "medium": ["Medkit", "FoodCrate", "MechanicalToolkit", "ElectricalToolkit", "PowerGenerator"],
    "high": ["HardDrive", "Laptop", "WaterPurifier", "CommoditiesBox", "Electrobaton"],
    "luxury": ["Exotic Food", "Rifle", "SMG"],
}

# Helper function to generate inventory based on wealth level
def generate_inventory(wealth_level):
    """
        Generate inventory for a shop based on the wealth level.
        
        Args:
        wealth_level (str): The wealth level of the shop (e.g., "low", "medium", "high").
    
    Returns:
        dict: Inventory with item names as keys and attributes like price and quantity as values.
        """

    # Fetch valid items from the imported modules
    valid_items = weapons.valid_items + InWorldObjects.valid_items
    
    # Filter out invalid items
    items = [item for item in ITEM_POOLS.get(wealth_level, []) if item in valid_items]

    # Create inventory for the shop
    inventory = {}
    for item in random.choices(items, k=random.randint(3, 7)):
        inventory[item] = {
            "price": valid_items[item]["value"],  # Use the value from imported modules
            "quantity": random.randint(1, 10),
        }
    return inventory

# Function to generate shops
def generate_shops():
    #Generate shops for each region based on wealth and region data.
    #print("Generating shops...")
    logger.debug(f"Generating {num_shops} shops for region {region_name} with wealth level {wealth_level}.")
    
    for region_name, region_info in region_data.items():
        wealth_level = region_info["wealth"]
        num_shops = max(3, random.randint(3, 7))  # Ensure at least 3 shops

        shops_data = []

        for i in range(num_shops):
                shop_type = random.choice(["Shop", "Vendor", "CorporateStore"])
                items_available = generate_inventory(wealth_level)

        shop_data = {
            "name": f"{shop_type}_{region_name}_{i+1}",
            "type": shop_type,
            "items_available": items_available,
            "cash": random.randint(100, 500),
            "legality": "legal",
            "upkeep": random.randint(10, 50),
            "is_concrete": True,
            "secret_entrance": random.choice([True, False]),
            "is_powered": random.choice([True, False]),
            "energy_cost": random.randint(0, 10),
            "security": {
                "level": random.randint(1, 5),
                "guards": random.choices(["Basic Guard", "Elite Guard"], k=random.randint(1, 3)),
                "difficulty_to_break_in": random.randint(1, 10),
                "surveillance": random.choice([True, False]),
                "alarm_system": random.choice([True, False])
            }
        }
        # Add generated shops to the region
        region_info["locations"].extend(shops_data)

        # Save the generated shop data to a JSON file
    output_path = f"{region_name}_shops.json"
    with open(output_path, "w") as file:
        json.dump(shops_data, file, indent=4)
    logger.info(f"Shops for region {region_name} saved to {output_path}.")

# Example usage
if __name__ == "__main__":
    # Define regions and their wealth levels
    regions_with_wealth = {
        "North": "high",
        "South": "medium",
        "East": "low",
        "West": "medium",
        "Central": "high"
    }

    # Generate shops for each region
    for region, wealth in regions_with_wealth.items():
        generate_shops(region, num_shops=5, wealth_level=wealth)

    print("Shop generation complete.")
