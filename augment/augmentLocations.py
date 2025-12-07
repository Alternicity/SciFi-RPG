#augment.augmentLocations.py

import random
from create.create_game_state import get_game_state
from debug_utils import debug_print
game_state = get_game_state()
from region.region_flavor import REGION_CULTURAL_ADJECTIVES as REGIONAL_FLAVOR




DEFAULT_SPECIALIZATION = "general"

SUPPORTED_SPECIALIZATIONS = [
    "weapon", "electronics", "medical", "tools", "luxury", "general"
]

SHOP_TYPES = {#not used, and overalps with SPECIALIZATION_KEYWORDS
    "weapon": ["Arms", "Armory", "Firearms", "Guns", "Ballistics"],
    "electronics": ["Tech", "Electronics", "Circuitry", "Gadgets"],
    "pharmacy": ["Pharma", "Health", "Meds", "FirstAid"],
    "general": ["Goods", "Mart", "Store", "Depot"],
    "tools": ["Workshop", "Tools", "Repairs", "Fixers"],
}

#REGIONAL_FLAVOR = REGION_CULTURAL_ADJECTIVES

""" REGIONAL_FLAVOR = {
    "northville": ["Northern", "Breezy"],
    "southville": ["Southern", "Dusty"],
    "easternhole": ["Eastern", "Hollow"],
    "westborough": ["Western", "Borough"],
    "downtown": ["Metro", "Central"]
} """

SPECIALIZATION_KEYWORDS = {#apparently not used in this file, or anywhere, yet. Either it or SHOP_TYPES is probably best removed
    "weapon": ["Arms", "Guns", "Weapons", "Armory"],
    "electronics": ["Circuits", "Gadgets", "Tech", "Devices"],
    "medical": ["Meds", "Pharma", "Health", "Remedy"],
    "mechanical": ["Gears", "Tools", "Fixit", "Workshop"],
    "electrical": ["Volts", "Electro", "Power", "Current"]
}

spec_suffixes = ["Armory", "Emporium", "Outlet", "Depot", "Mart", "Bazaar", "Vault", "Shop", "Store"]
family_surnames = game_state.extant_family_names

def reassign_shop_names_after_character_creation():
    game_state = get_game_state()
    all_shops = game_state.all_shops
    family_pool = list(game_state.extant_family_names)

    #debug_print(None, f"[DEBUG] extant_family_names={game_state.extant_family_names}", "economy")

    if not family_pool:
        debug_print(None, "[WARN] No extant family names exist; shop renaming skipped.", "economy")
        return

    used_names = set()

    debug_print(None, f"[INFO] Reassigning names for {len(all_shops)} shops.", "shops")

    for shop in all_shops:

        if not shop.name.startswith("Generic"):
            continue  # Only rename placeholder names

        # 1. Choose unused family name

        available = [f for f in family_pool if f not in used_names]
        if not available:
            available = family_pool  # fallback, allow reuse

        family = random.choice(available)
        used_names.add(family)

        # 2. Determine region flavor

        region_name = shop.region.name if shop.region else "Unknown"
        region_flavor_list = REGIONAL_FLAVOR.get(region_name, [])
        flavor = random.choice(region_flavor_list) + " " if region_flavor_list and random.random() < 0.4 else ""

        # 3. Determine suffix based on specialization

        spec_suffix = {
            "weapon": "Guns",
            "electronics": "Electrics",
            "medical": "Meds",
            "tools": "Hardware",
            "luxury": "Finery",
            "general": "Store",
        }.get(shop.specialization, "Store")

        # 4. Assign final name
        shop.name = f"{family}'s {flavor}{spec_suffix}"
        #debug_print(None, f"Renamed shop → {shop.name}", "shops")





""" park_sublocs = [Playground(), Storeroom()]
nightclub_sublocs = [DanceFloor(), Storeroom(), Office()] """
