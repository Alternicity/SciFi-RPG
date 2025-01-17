import sys
import os
import json
import random
from dataclasses import asdict
import logging

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
            wealth_level (str): Wealth level of the region.
        
        Returns:
            list: List of items with their prices.
        """

    # Ensure the wealth_level exists in ITEM_POOLS
    items = ITEM_POOLS.get(wealth_level, ITEM_POOLS["medium"])  # Fallback to "medium" if wealth_level is invalid
    return [{"item": item, "price": random.randint(10, 100)} for item in random.choices(items, k=random.randint(3, 7))]
    #if the wealth_level key is not found in ITEM_POOLS, the function defaults to using the "medium" item pool.

# Function to generate shops
def generate_shops():
    #print("Generating shops...")
    logger.debug("Generating shops...")

    # Define regions and their wealth levels
    regions_with_wealth = {
        "North": "high",  # Changed from "Rich" to "high"
        "South": "medium",  # Changed from "Normal" to "medium"
        "East": "low",  # Changed from "Poor" to "low"
        "West": "medium",  # Changed from "Medium" to "medium"
        "Central": "high"  # Changed from "High" to "high"
    }

    shops_data = {}

    for region, wealth_level in regions_with_wealth.items():
        print(f"Generating shops for region: {region} (Wealth: {wealth_level})")

        # Determine the number of shops based on wealth level
        num_shops = random.randint(2, 5) if wealth_level in ["medium", "high"] else random.randint(1, 3)

        shops_data[region] = []

        for i in range(num_shops):
            shop_type = random.choices(
                ["Shop", "CorporateStore", "Stash"],
                weights=[4, 2, 1] if wealth_level in ["medium", "high"] else [3, 1, 2],
            )[0]

            # Generate common attributes
            common_attributes = {
                "name": f"{shop_type}_{region}_{i+1}",
                "items_available": generate_inventory(wealth_level),
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


            # Add type-specific attributes
            if shop_type == "Shop":
                shop = {
                    "type": "Shop",
                    "fun": random.randint(0, 5),
                    **common_attributes
                }
            elif shop_type == "CorporateStore":
                shop = {
                    "type": "CorporateStore",
                    "corporation": f"Corp_{region}",
                    **common_attributes
                }
            elif shop_type == "Stash":
                shop = {
                    "type": "Stash",
                    "stored_items": [],  # Initially empty
                    **common_attributes
                }

            shops_data[region].append(shop)

    print("Shop generation complete.")
    return shops_data

# Save shops data to JSON files
def save_shops_to_json(shops_data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for region, shops in shops_data.items():
        region_path = os.path.join(output_dir, f"{region}_shops.json")
        with open(region_path, "w") as f:
            json.dump(shops, f, indent=4)
        logger.debug(f"Shops data for {region} saved to {region_path}")

# Example usage
if __name__ == "__main__":
    shops_data = generate_shops()
    output_dir = r"C:\Users\Stuart\Python Scripts\scifiRPG\data\Test City\Shops"
    save_shops_to_json(shops_data, output_dir)