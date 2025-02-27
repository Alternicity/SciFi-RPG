import logging
import os
import json
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
#🟢 🔴 🔵 🟡 🟠 🟣 ⚫ ⚪ 🟤
from city_vars import game_state

def get_region_by_name(name, all_regions): #these get functions get the object from a "string"
    """Finds and returns the region object by name."""
    return next((r for r in all_regions if r.name == name), None)

def get_valid_races():
    from base_classes import Character  # Lazy import to avoid circular dependency
    return list(Character.VALID_RACES)

def get_faction_by_name(faction_name, factions):
    matches = [f for f in factions if f.name == faction_name]
    
    if not matches:
        print(f"❌ ERROR: No faction found with name '{faction_name}'")
        return None
    
    if len(matches) > 1:
        print(f"⚠️ WARNING: Multiple factions found for '{faction_name}', returning first match")

    return matches[0]  # Ensure a single object is returned

def get_location_by_name(name, all_regions):
    """Find and return a location by name from game_state.all_locations."""
    print(f"DEBUG: Searching for '{name}' in game_state.all_locations...")

    for location in game_state.all_locations:
        print(f"DEBUG: Checking location: {location.name}")

        if location.name.lower() == name.lower():  # Case-insensitive comparison
            return location

    print(f"WARNING: Could not find specified location '{name}'.")
    return None

from faction import Gang
def create_gang(data): #
    """Create a Gang object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Gang.")
    return Gang(name=data["name"], affiliation=data.get("affiliation", "unknown"))

from faction import Corporation
def create_corporation(data): 
    """Create a Corporation object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Corporation.")
    return Corporation(name=data["name"])#what does this do?

def create_weapon(data): #Might still be useful, but need updating
    """Create a Weapon object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Weapon.")
    return Weapon(
        name=data["name"],
        damage=data.get("damage", 0),
        ammo=data.get("ammo", 0),
        range_limit=data.get("range_limit", 0),
        toughness=data.get("toughness", "normal"),
        size=data.get("size", "pocket_sized"),
    )

def create_item(data): #Might still be useful, but need updating
    """Create an ObjectInWorld object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Item.")
    return ObjectInWorld(
        name=data["name"],
        toughness=data.get("toughness", "normal"),
        damage_points=data.get("damage_points", 0),
        legality=data.get("legality", True),
        legitimate_value=data.get("value", 0),
        blackmarket_value=data.get("blackmarket_value", 0),
        size=data.get("size", "pocket_sized"),
    )

def get_project_root():
    # Set the project root directory explicitly
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    