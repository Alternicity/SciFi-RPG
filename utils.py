import logging
import os
import json
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
#🟢 ⚪🔴 🔵 🟡 🟠 🟣 ⚫  🟤
from create_game_state import get_game_state  # Ensure we get the latest game state

def get_region_by_name(name, all_regions): #these get functions get the object from a "string"
    """Finds and returns the region object by name."""
    return next((r for r in all_regions if r.name == name), None)


def get_faction_by_name(faction_name, factions):
    matches = [f for f in factions if f.name == faction_name]
    
    if not matches:
        print(f"❌ ERROR: No faction found with name '{faction_name}'")
        return None
    
    if len(matches) > 1:
        print(f"⚠️ WARNING: Multiple factions found for '{faction_name}', returning first match")

    return matches[0]  # Ensure a single object is returned

def get_location_by_name(name, all_regions):
    """Find and return a location by name by searching through regions."""
    if not all_regions:
        print("ERROR: all_regions is not initialized or empty!")
        return None
    
    for region in all_regions:
        for location in getattr(region, "locations", []):
            if location.name.lower() == name.lower():  # Case-insensitive
                return location
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
    from weapons import Weapon
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
    from InWorldObjects import ObjectInWorld
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


# ✅ Move the test outside the function to prevent recursion
if __name__ == "__main__":
    from create_game_state import get_game_state
    game_state = get_game_state()

    if not hasattr(game_state, "all_locations") or game_state.all_locations is None:
        print("ERROR: game_state.all_locations is None or uninitialized!")
    else:
        pass
        #print(f"DEBUG: game_state.all_locations contains {len(game_state.all_locations)} locations.")
        #verbose
        
    # Test valid location
    test_location = get_location_by_name("Municipal Building", game_state.all_locations)
    print(f"DEBUG: Found location: {test_location.name if test_location else 'None'}")

    # Test invalid location
    test_location = get_location_by_name("Nonexistent Place", game_state.all_locations)
    print(f"DEBUG: Found location: {test_location.name if test_location else 'None'}")

def audit_game_state():
    """Audit consistency between regions and global location lists."""
    game_state = get_game_state()
    issues_found = False

    for region in game_state.all_regions:
        for loc in region.locations:
            if loc not in game_state.all_locations:
                print(f"🧪 Audit: {loc.name} is in {region.name} but missing from game_state.all_locations")
                issues_found = True

    if not issues_found:
        print("✅ Audit passed: All region locations are synced with game_state.all_locations.")

def dev_mode():
    print("🔧 Dev Mode Activated: Auditing Game State...")
    audit_game_state()

def get_region_for_location(location, all_regions):
    for region in all_regions:
        if location.region == region.name or location.region == region:
            print(f"✅ get_region_for_location: Found match - {region.name} for location {location.name}")
            return region
    print(f"🟣🟢 No matching region found for location: {location.name} with region = {location.region}")
    return None

def normalize_location_regions(all_locations, all_regions):
    """
    Ensures all Location objects reference a Region object, not a string.
    Fixes any locations with region as a str by matching it to a Region by name.
    """
    from location import Region  # or wherever your Region class is

    for loc in all_locations:
        if isinstance(loc.region, str):
            region_name = loc.region.strip().lower()
            matched_region = next(
                (reg for reg in all_regions if reg.name.strip().lower() == region_name),
                None
            )
            if matched_region:
                print(f"🛠️ Fixed region for location: {loc.name} (was '{loc.region}', now Region object)")
                loc.region = matched_region
                matched_region.add_location(loc)
            else:
                print(f"⚠️ Could not resolve region '{loc.region}' for location '{loc.name}'")