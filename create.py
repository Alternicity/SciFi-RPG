#create.py
import logging
import json
from loader import load_region_data
from location import Region
from common import BASE_REGION_DIR
import os

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
    Reads JSON region data and instantiates a Region object.

    Args:
        region_name (str): The name of the region (e.g., 'North').

    Returns:
        Region: The instantiated Region object.

    Raises:
        FileNotFoundError: If the JSON file for the region is not found.
        ValueError: If the JSON data is invalid.
    """
    try:
        # Load region data from JSON
        region_data = load_region_data(region_name)
        
        # Instantiate the Region object
        region = Region(
            name=region_data["name"],
            nameForUser=region_data.get("nameForUser", region_data["name"]),
            shops=region_data.get("shops", []),
            locations=region_data.get("locations", []),
            factions=region_data.get("factions", [])
        )
        
        # Additional setup or validation if needed
        # e.g., region.validate_data() or enrich_region(region)

        return region
    except FileNotFoundError as e:
        print(f"Region data file for '{region_name}' not found.")
        raise
    except KeyError as e:
        print(f"Missing required field in region data for '{region_name}': {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        region_name = "North"  # Example region name
        region = create_region(region_name)
        print(f"Successfully created region: {region}")
    except Exception as e:
        print(f"Error: {e}")