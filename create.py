#create.py
import logging
import json
from pathlib import Path
from loader import load_region_data, load_shops
from location import Shop, CorporateStore, Stash, Region
from location_security import Security
from common import BASE_REGION_DIR, BASE_SHOPS_DIR
from typing import List, Dict, Union
import os
from typing import List, Union

#from display import list_characters
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG, WARNING, ERROR as needed
    format="%(levelname)s:%(message)s"
)

def create_and_serialize_characters(): #for pre grame start world building
    characters = [
        RiotCop(name="John", faction="The State"),
        CorporateAssasin(name="Jane", faction="BlueCorp"),
    ]
    with open("characters.json", "w") as f:
        json.dump([char.__dict__ for char in characters], f, indent=4)
    logging.info("Characters serialized to characters.json")

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

    logger.info(f"Creating object of type {obj_type} with data: {data}.")

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
    
def create_all_regions() -> list:
    """
    Creates all region objects by loading their JSON data.

    Returns:
        list: A list of instantiated Region objects.

    Raises:
        FileNotFoundError: If the region directory is missing or empty.
        ValueError: If a region JSON file is invalid.
    """
    regions = []
    if not os.path.exists(BASE_REGION_DIR) or not os.listdir(BASE_REGION_DIR):
        raise FileNotFoundError(f"No region JSON files found in {BASE_REGION_DIR}")

    for file_name in os.listdir(BASE_REGION_DIR):
        if file_name.endswith(".json"):
            region_name = os.path.splitext(file_name)[0]  # Extract region name from filename
            try:
                region = create_region(region_name)
                regions.append(region)
            except Exception as e:
                print(f"Error creating region for {region_name}: {e}")
    
    print(f"All {len(regions)} regions have been created as objects.")
    return regions

def create_region(region_name: str) -> Region:
    """
    Reads JSON region data, instantiates a Region object, and populates it with locations.
    Args: region_name (str): The name of the region (e.g., 'North').
    Returns: Region: The instantiated Region object with associated locations.
    """
    region_file_path = Path(BASE_REGION_DIR) / f"{region_name}.json"

    try:
        with open(region_file_path, "r") as file:
            region_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Region data file for '{region_name}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file: {region_file_path}")
        
        # Create the Region object
    region = Region(
        name=region_data["name"],
        nameForUser=region_data.get("nameForUser", region_data["name"]),
        shops=[],  # Initialize empty shops list
        locations=[],  # Initialize empty locations list
        factions=region_data.get("factions", [])
    )

    """ return region
    except FileNotFoundError as e:
        print(f"Region data file for '{region_name}' not found.")
        raise
    except KeyError as e:
        print(f"Missing required field in region data for '{region_name}': {e}")
        raise """

def create_locations(region_name: str) -> List[Union[Shop, CorporateStore, Stash]]:
    """
    Creates location objects (shops, corporate stores, stashes) for the specified region.
    Returns:
        list: A list of instantiated location objects.
    """
    # Load raw shop data
    #shops_data = load_shops(region_name)

    shops_file_path = Path(BASE_SHOPS_DIR) / f"{region_name}.json"

try:
        with open(shops_file_path, "r") as file:
            shops_data = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"Shops data file for '{region_name}' not found.")
except json.JSONDecodeError:
    raise ValueError(f"Invalid JSON data in file: {shops_file_path}")

# Create location objects
locations = []
for shop_data in shops_data:
    if shop_data["type"] == "Shop":
        location = Shop(
            region=None,  # Pass region (or the actual Region object)
            location=None,  # Pass location (or the actual Location object)
            name=shop_data["name"],
            inventory=shop_data["inventory"],
            cash=shop_data["cash"],
            bankCardCash=shop_data["bankCardCash"],
            legality=shop_data["legality"],
            security=Security(**shop_data["security"])
        )
    elif shop_data["type"] == "CorporateStore":
        location = CorporateStore(
            region=None,  # Pass region (or the actual Region object)
            location=None,  # Pass location (or the actual Location object)
            name=shop_data["name"],
            corporation=shop_data["corporation"],
            inventory=shop_data.get("inventory", {}),
            cash=shop_data.get("cash", 0),
            bankCardCash=shop_data.get("bankCardCash", 0),
            legality=shop_data.get("legality", "Legal"),
            security=Security(**shop_data.get("security", {}))
        )
    elif shop_data["type"] == "Stash":
        location = Stash(
            region=None,  # Pass region (or the actual Region object)
            location=None,  # Pass location (or the actual Location object)
            name=shop_data["name"],
            inventory=shop_data.get("inventory", {}),
            cash=shop_data.get("cash", 0),
            bankCardCash=shop_data.get("bankCardCash", 0),
            legality=shop_data.get("legality", "Illegal"),
            security=Security(**shop_data.get("security", {}))
        )
    locations.append(location)

    return locations

def associate_locations_with_region(region: Region, locations: List[Union[Shop, CorporateStore, Stash]]) -> Region:
    """
    Associates location objects with a region by 
    updating the region's shops and locations lists.
    Args:
        region (Region): The Region object to update.
        locations (list): A list of location objects (Shop, CorporateStore, Stash).
    Returns:
        Region: The updated Region object.
    """
    for location in locations:
        if isinstance(location, Shop):
            region.shops.append(location)  # Add shops to the shops list
        else:
            region.locations.append(location)  # Add non-shops to the locations list

    return region

# Example usage
if __name__ == "__main__":
    try:
        region_name = "North"  # Example region name
        region = create_region(region_name)
        print(f"Successfully created region: {region}")
    except Exception as e:
        print(f"Error: {e}")