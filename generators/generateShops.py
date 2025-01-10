import sys
import os
import json
import random
from dataclasses import dataclass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from location import Shop, Stash, Vendor, CorporateStore
#from generateRegion import get_regions_with_wealth

# Path for saving generated Shop data
BASE_STORE_PATH = r"C:\Users\Stuart\Python Scripts\scifi RPG\data\Test City\Stores"

# Sample item pools for inventory generation
ITEM_POOLS = {
    "low": ["Basic Food", "Cheap Clothing", "Used Electronics"],
    "medium": ["Standard Food", "Stylish Clothing", "Electronics"],
    "high": ["Gourmet Food", "Designer Clothing", "Advanced Electronics"],
    "luxury": ["Exotic Food", "Luxury Clothing", "Cutting-Edge Gadgets"],
} #does not correlate with InWorldObjects,these objects have no data yet

# Helper function to generate inventory based on wealth level
def generate_inventory(wealth_level):
    items = ITEM_POOLS.get(wealth_level, [])
    return random.choices(items, k=random.randint(3, 7))

# Function to generate shops
def generate_shop():
    print("Generating shops...")

    # Fetch regions and their wealth levels
    regions_with_wealth = get_regions_with_wealth()

    for region, wealth_level in regions_with_wealth.items():
        print(f"Generating stores for region: {region} (Wealth: {wealth_level})")

        # Determine the number of shops based on wealth level
        num_shops = random.randint(2, 5) if wealth_level in ["medium", "high"] else random.randint(1, 3)

        # Create region directory if it doesn't exist
        region_path = os.path.join(BASE_STORE_PATH, region)
        os.makedirs(region_path, exist_ok=True)

        for i in range(num_stores):
            shop_type = random.choices(
                ["Stash", "Vendor", "CorporateDepot", "Dealer"],
                weights=[1, 4, 2, 3] if wealth_level in ["medium", "high"] else [3, 2, 1, 4],
            )[0]

            # Instantiate Shop based on type
            if shop_type == "Stash":
                shop = Stash(name=f"Hidden Stash {i+1}")
            elif shop_type == "Vendor":
                shop = Vendor(name=f"Vendor {i+1}")
            elif shope_type == "CorporateDepot":
                sshop = CorporateDepot(name=f"Corp Depot {i+1}", corporation=f"Corp_{region}")
            elif shop_type == "Dealer":
                shop = Dealer(name=f"Dealer {i+1}", gang_affiliation=f"Gang_{region}", cash=500, bankCardCash=1000)
            else:
                shop = Shop(name=f"Generic Shop {i+1}")

            # Generate inventory based on wealth level
            Shop.inventory.items = generate_inventory(wealth_level)

            # Save Shop data to JSON
            Shop_data = {
                "name": Shop.name,
                "type": shop_type,
                "region": region,
                "inventory": Shop.inventory.items,
                "cash": shop.cash,
                "bankCardCash": Shop.bankCardCash,
                "legality": Shop.legality,
                "security": Shop.security,
            }

            store_file = os.path.join(region_path, f"{Shop.name.replace(' ', '_')}.json")
            with open(store_file, "w") as f:
                json.dump(store_data, f, indent=4)

    print("Shop generation complete.")

if __name__ == "__main__":
    generate_stores()
