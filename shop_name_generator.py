#shop_name_generator.py

import os
import random
from pathlib import Path
from typing import List, Optional
from common import BASE_CHARACTERNAMES_DIR
from create.create_game_state import get_game_state
game_state = get_game_state()



CORPORATE_PREFIXES = ["Neo", "Aether", "Lux", "Orbital", "Prime", "Hyper", "Meta"]
CORPORATE_SUFFIXES = ["Corp", "Group", "Industries", "Solutions", "Works", "Systems"]
OPTIONAL_SUFFIXES = ["Ltd.", "Emporium", "Bazaar", "Co.", "Holdings"]


CORP_PREFIXES = ["Neo", "Quantum", "Aether", "Orion", "Meta", "Terra", "Nova", "Astro", "Hyper"]
CORP_SUFFIXES = ["Tech", "Dynamics", "Group", "Holdings", "Logistics", "Industries", "Solutions", "Global"]


# GENERIC NAME GENERATOR

def generate_shop_name(specialization, region_name):
    return f"Generic {specialization} Shop"



    """ # CORPORATE SHOP LOGIC
    # -------------------------
    prefix = random.choice(CORPORATE_PREFIXES)
    suffix = random.choice(CORPORATE_SUFFIXES)

    mid = {
        "weapon": "Ballistics",
        "electronics": "Circuits",
        "medical": "Pharma",
        "tools": "Works",
        "luxury": "Design",
        "general": "Mart",
    }.get(specialization, "Mart")

    flavor = random.choice(region_flavor) if region_flavor and random.random() < 0.3 else ""

    return " ".join(part for part in [flavor, prefix, mid, suffix] if part)
    """
# === TEST ===
if __name__ == "__main__":
    
    """ for _ in range(10):
        print(generate_shop_name("weapon", random.choice(["family", "corporate"]), region=random.choice(list(REGIONAL_FLAVOR.keys()))))
    """