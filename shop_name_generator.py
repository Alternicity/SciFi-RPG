#shop_name_generator.py

import os
import random
from pathlib import Path
from typing import List, Optional
from common import BASE_CHARACTERNAMES_DIR


# === CONFIGURATION ===
DEFAULT_SPECIALIZATION = "general"

SUPPORTED_SPECIALIZATIONS = [
    "weapon", "electronics", "medical", "tools", "luxury", "general"
]

# -----------------------------
# FAMILY NAME LOADER
# -----------------------------
def load_family_names() -> List[str]:
    family_names = []
    for filename in os.listdir(BASE_CHARACTERNAMES_DIR):
        if not filename.endswith("Names.txt"):
            continue
        filepath = os.path.join(BASE_CHARACTERNAMES_DIR, filename)
        with open(filepath, newline='', encoding='utf-8') as f:
            section = None
            for line in f:
                line = line.strip()
                if line.lower().startswith("family"):
                    section = "family"
                    continue
                if line.lower() in ("male name", "female name"):
                    section = None
                elif section == "family" and line:
                    family_names.append(line)
    return family_names

FAMILY_NAMES = load_family_names()

SHOP_TYPES = {
    "weapon": ["Arms", "Armory", "Firearms", "Guns", "Ballistics"],
    "electronics": ["Tech", "Electronics", "Circuitry", "Gadgets"],
    "pharmacy": ["Pharma", "Health", "Meds", "FirstAid"],
    "general": ["Goods", "Mart", "Store", "Depot"],
    "tools": ["Workshop", "Tools", "Repairs", "Fixers"],
}

FAMILY_NAMES_POOL = load_family_names()

CORPORATE_PREFIXES = ["Neo", "Aether", "Lux", "Orbital", "Prime", "Hyper", "Meta"]
CORPORATE_SUFFIXES = ["Corp", "Group", "Industries", "Solutions", "Works", "Systems"]
OPTIONAL_SUFFIXES = ["Ltd.", "Emporium", "Bazaar", "Co.", "Holdings"]

REGIONAL_FLAVOR = {#line 35
    "NorthVille": ["Northern"],
    "SouthVille": ["Southern"],
    "Easternhole": ["Eastern", "Hollow"],
    "Westborough": ["Western", "Borough"],
    "Downtown": ["Metro", "Central"]
}

SPECIALIZATION_KEYWORDS = {
    "weapon": ["Arms", "Guns", "Weapons", "Armory"],
    "electronics": ["Circuits", "Gadgets", "Tech", "Devices"],
    "medical": ["Meds", "Pharma", "Health", "Remedy"],
    "mechanical": ["Gears", "Tools", "Fixit", "Workshop"],
    "electrical": ["Volts", "Electro", "Power", "Current"]
}

SHOP_SUFFIXES = ["Armory", "Emporium", "Outlet", "Depot", "Mart", "Bazaar", "Vault", "Shop", "Store"]
CORP_PREFIXES = ["Neo", "Quantum", "Aether", "Orion", "Meta", "Terra", "Nova", "Astro", "Hyper"]
CORP_SUFFIXES = ["Tech", "Dynamics", "Group", "Holdings", "Logistics", "Industries", "Solutions", "Global"]


# -----------------------------
# NAME GENERATOR
# -----------------------------
def generate_shop_name(specialization: Optional[str] = None, ownership: str = "family", region_name: Optional[str] = None) -> str:
    specialization = specialization or DEFAULT_SPECIALIZATION
    region_flavor = REGIONAL_FLAVOR.get(region_name, [])

    if ownership == "family" and FAMILY_NAMES:
        base = random.choice(FAMILY_NAMES)
        suffix = {
            "weapon": "Guns",
            "electronics": "Electrics",
            "medical": "Meds",
            "tools": "Hardware",
            "luxury": "Finery",
            "general": "Store"
        }.get(specialization, "Store")

        flavor = random.choice(region_flavor) if region_flavor and random.random() < 0.4 else ""
        name_parts = [flavor, f"{base}'s", suffix]
        return " ".join(part for part in name_parts if part)

    else:  # corporate
        prefix = random.choice(CORP_PREFIXES)
        suffix = random.choice(CORP_SUFFIXES)
        mid = {
            "weapon": "Ballistics",
            "electronics": "Circuits",
            "medical": "Pharma",
            "tools": "Works",
            "luxury": "Design",
            "general": "Mart"
        }.get(specialization, "Mart")

        flavor = random.choice(region_flavor) if region_flavor and random.random() < 0.3 else ""
        return " ".join(part for part in [flavor, prefix, mid, suffix] if part)

# === HELPERS ===
def get_all_family_names():
    family_names = []
    for file in BASE_CHARACTERNAMES_DIR.glob("*Names.txt"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if "Family Name" in lines:
                    idx = lines.index("Family Name")
                    family_names += [line.strip() for line in lines[idx + 1:] if line.strip()]
        except Exception as e:
            print(f"[ERROR] Could not read file {file}: {e}")
    return family_names

# -----------------------------
# SPECIALIZATION GUESSER
# -----------------------------
def guess_specialization_from_inventory(inventory) -> str:
    if inventory is None or not hasattr(inventory, "items"):
        return DEFAULT_SPECIALIZATION

    tags = []
    for item in inventory.items.values():
        if hasattr(item, "get_percept_data"):
            data = item.get_percept_data()
            tags.extend(data.get("tags", []))

    # Simplified heuristics
    if any("weapon" in tag for tag in tags):
        return "weapon"
    elif any(tag in ["electronics", "smartphone", "laptop"] for tag in tags):
        return "electronics"
    elif any("medical" in tag or tag == "medkit" for tag in tags):
        return "medical"
    elif any(tag in ["tool", "toolkit"] for tag in tags):
        return "tools"
    elif any(tag in ["luxury", "statue", "vase", "lamp"] for tag in tags):
        return "luxury"
    else:
        return DEFAULT_SPECIALIZATION

# -----------------------------
# DEBUG DISPLAY (hook in display.py)
# -----------------------------
def format_shop_debug(shop) -> dict:
    return {
        "Name": shop.name,
        "Type": shop.__class__.__name__,
        "Region": shop.region.name if hasattr(shop, "region") else "?",
        "Specialization": guess_specialization_from_inventory(shop.inventory),
        "OwnerType": "corporate" if any(corp for corp in getattr(shop.region, "region_corps", []) if corp.HQ == shop) else "family"
    }

# === TEST ===
if __name__ == "__main__":
    for _ in range(10):
        print(generate_shop_name("weapon", random.choice(["family", "corporate"]), region=random.choice(list(REGIONAL_FLAVOR.keys()))))
