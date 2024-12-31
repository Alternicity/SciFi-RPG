import os
import json
import random
from store import Store, Stash, Vendor, CorporateDepot, Dealer
from generateRegion import get_regions_with_wealth

# Path for saving generated store data
BASE_STORE_PATH = r"C:\Users\Stuart\Python Scripts\scifi RPG\data\Test City\Stores"

# Sample item pools for inventory generation
ITEM_POOLS = {
    "low": ["Basic Food", "Cheap Clothing", "Used Electronics"],
    "medium": ["Standard Food", "Stylish Clothing", "Electronics"],
    "high": ["Gourmet Food", "Designer Clothing", "Advanced Electronics"],
    "luxury": ["Exotic Food", "Luxury Clothing", "Cutting-Edge Gadgets"],
}

# Helper function to generate inventory based on wealth level
def generate_inventory(wealth_level):
    items = ITEM_POOLS.get(wealth_level, [])
    return random.choices(items, k=random.randint(3, 7))

# Function to generate stores
def generate_stores():
    print("Generating stores...")

    # Fetch regions and their wealth levels
    regions_with_wealth = get_regions_with_wealth()

    for region, wealth_level in regions_with_wealth.items():
        print(f"Generating stores for region: {region} (Wealth: {wealth_level})")

        # Determine the number of stores based on wealth level
        num_stores = random.randint(2, 5) if wealth_level in ["medium", "high"] else random.randint(1, 3)

        # Create region directory if it doesn't exist
        region_path = os.path.join(BASE_STORE_PATH, region)
        os.makedirs(region_path, exist_ok=True)

        for i in range(num_stores):
            store_type = random.choices(
                ["Stash", "Vendor", "CorporateDepot", "Dealer"],
                weights=[1, 4, 2, 3] if wealth_level in ["medium", "high"] else [3, 2, 1, 4],
            )[0]

            # Instantiate store based on type
            if store_type == "Stash":
                store = Stash(name=f"Hidden Stash {i+1}")
            elif store_type == "Vendor":
                store = Vendor(name=f"Vendor {i+1}")
            elif store_type == "CorporateDepot":
                store = CorporateDepot(name=f"Corp Depot {i+1}", corporation=f"Corp_{region}")
            elif store_type == "Dealer":
                store = Dealer(name=f"Dealer {i+1}", gang_affiliation=f"Gang_{region}", cash=500, bank_card_cash=1000)
            else:
                store = Store(name=f"Generic Store {i+1}")

            # Generate inventory based on wealth level
            store.inventory.items = generate_inventory(wealth_level)

            # Save store data to JSON
            store_data = {
                "name": store.name,
                "type": store_type,
                "region": region,
                "inventory": store.inventory.items,
                "cash": store.cash,
                "bank_card_cash": store.bank_card_cash,
                "legality": store.legality,
                "security": store.security,
            }

            store_file = os.path.join(region_path, f"{store.name.replace(' ', '_')}.json")
            with open(store_file, "w") as f:
                json.dump(store_data, f, indent=4)

    print("Store generation complete.")

if __name__ == "__main__":
    generate_stores()
