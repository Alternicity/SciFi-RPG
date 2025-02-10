#create.py
import logging
import json
from pathlib import Path

from loader import load_gang_names, get_gang_names_filepath
from base_classes import Location, Character
from location import Shop, CorporateStore, Stash, Region, UndevelopedRegion, VacantLot, HQ, MunicipalBuilding
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, GangMember, Child, Influencer,
                           Babe, Detective)
from faction import Corporation, Gang, State
from goals import Goal
from location_security import Security
from common import BASE_REGION_DIR, BASE_SHOPS_DIR
from typing import List, Dict, Union
import os

from character_creation_funcs import create_all_characters
import random


#from display import list_characters
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG, WARNING, ERROR as needed
    format="%(levelname)s:%(message)s"
)


    

def create_object(data):#Might still be useful, but need updating

    """
    Factory function to create an object dynamically based on its type.

    Args:
        data (dict): Data representing the object.

    Returns:
        An instance of the appropriate class.

    Raises:
        ValueError: If the object type is unsupported or required attributes are missing.
    """
    obj_type = data.get("type")
    if obj_type is None:
        raise ValueError("Missing 'type' in data.")

    logging.info(f"Creating object of type {obj_type} with data: {data}.")

    if obj_type == "gang":
        return create_gang(data)
    elif obj_type == "corporation":
        return create_corporation(data)
    elif obj_type == "weapon":
        return create_weapon(data)
    elif obj_type == "item":
        return create_item(data)
    else:
        raise ValueError(f"Unsupported type: {obj_type}")
    

def create_locations(region_name: str, wealth: str) -> List[Location]:
    """Creates a list of location objects for a region based on its wealth level."""
    location_objects = []

    # Fetch location types for this wealth level
    from location_types_by_wealth import LocationTypes
    location_types = LocationTypes.location_types_by_wealth.get(wealth, [])

    for location_class, count in location_types:
        for _ in range(count):  # Create the specified number of locations
            try:
                location_obj = location_class(name=f"{location_class.__name__} in {region_name}")
                location_objects.append(location_obj)
            except Exception as e:
                print(f"Error creating location {location_class.__name__} in {region_name}: {e}")

    # Always create a MunicipalBuilding
    municipal_building = MunicipalBuilding(name=f"Municipal Building in {region_name}")
    location_objects.append(municipal_building)
    return location_objects

def create_regions():
    """Create and return a list of Region objects with Locations inside them."""
    print("Initializing regions as objects...")

    region_wealth_levels = {
        "NorthVille": "Normal",
        "Easternhole": "Poor",
        "Westborough": "Rich",
        "SouthVille": "Normal",
        "Downtown": "Rich",
    }

    # Store region objects
    region_objects = []

    for region, wealth in region_wealth_levels.items():
        try:
            location_list = create_locations(region, wealth)  # Get Location objects

            region_obj = Region(
                name=region,
                shops=[loc for loc in location_list if isinstance(loc, Shop)],  # Extract Shops separately
                locations=location_list,  # Full list of Locations
                factions=[],
                DangerLevel=None,
            )

            region_objects.append(region_obj)
            print(f"Created region: {region} with {len(region_obj.locations)} locations.")

        except Exception as e:
            print(f"Error creating region '{region}': {e}")

    return region_objects

all_regions = create_regions()  # Ensure regions exist before creating factions




def generate_gang_name(first_parts, second_parts):
    """Generates a gang name by randomly combining first and second parts."""
    return f"{random.choice(first_parts)} {random.choice(second_parts)}"

def create_factions(locations):
    """
    Creates a State, gangs, and corporations for each region.
    Assigns HQ locations from available locations.
    """
    print("Creating factions...")

    factions = []  # Store created factions

    # Find the Downtown region in all_regions
    downtown_region = next((region for region in all_regions if region.name == "Downtown"), None)
    if downtown_region is None:
        raise ValueError("Error: Downtown region not found in all_regions.")
    
    all_characters = []
    state = State(name="Unified Government", resources={"money": 1000000}, laws=["No theft", "Corporate tax"], region=downtown_region)
    factions.append(state)

    # Get the file path dynamically from loader.py
    GANG_NAMES_FILE = get_gang_names_filepath()

    if os.path.exists(GANG_NAMES_FILE):
        first_parts, second_parts = load_gang_names(GANG_NAMES_FILE)
    else:
        first_parts, second_parts = ["Default"], ["Gang"]

    # Create 10 gangs
    for _ in range(10):
        gang_name = generate_gang_name(first_parts, second_parts)
        gang = Gang(name=gang_name, violence_disposition="High")
        factions.append(gang)

    # Create 10 corporations
    for _ in range(10):
        corp = Corporation(name=f"Corp_{random.randint(100, 999)}", violence_disposition="Low")
        factions.append(corp)

    # Now, create all characters for these factions
    all_characters = create_all_characters(factions, locations, all_regions)

    return factions, all_characters





def assign_hq(faction, region):
    """Assigns an HQ to a faction and updates its attributes. If no HQ is found, assigns an 'acquire HQ' goal."""
    available_hqs = [loc for loc in region.locations if isinstance(loc, HQ) and loc.faction is None]
    
    if available_hqs:
        hq = available_hqs[0]  # Assign the first available HQ
        hq.faction = faction
        hq.name = f"{faction.name} HQ"  # Update HQ name
        faction.HQ = hq  # Update faction's HQ attribute
        print(f"{faction.name} HQ assigned: {hq.name} in {region.name}")
    else:
        print(f"No available HQ for {faction.name} in {region.name}. Assigning 'acquire HQ' goal.")
        faction.add_goal(Goal(description="Acquire an HQ", goal_type="acquire HQ"))
    

from character_creation_funcs import create_all_characters
def create_characters(factions, locations, all_regions):  
    return create_all_characters(factions, locations)

# Generate factions and characters
all_factions, all_characters = create_factions(all_regions)
all_characters = create_characters(all_factions, all_regions)
