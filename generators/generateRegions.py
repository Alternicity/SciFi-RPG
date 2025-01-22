#generateRegions
import random
import json
import os
import logging
import sys
from common import get_project_root, get_file_path, BASE_RUNTIME_DIR
#ALL files use this to get the project root
from yamlManager import YAMLManager


print(f"Current directory: {os.getcwd()}")

project_root = get_project_root()  # Call the function to get the project root
print(f"Project root: {project_root}")
print(f"sys.path: {sys.path}")

# Import from scifiRPG

from location import Region, Location
#print("Imported scifiRPG.location successfully!")

from location import (
    HQ, Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalRepairWorkshop, Stash,
    Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Park, Museum, Library
)

def generate_region(regions_with_wealth):
    """
    Generates a region and writes its data to a YAML file.

    Args:
        region_name (str): The name of the region (e.g., "North", "South").
        region_data (dict): The data structure containing the region's attributes and locations.
        yaml_manager (YAMLManager): The YAML manager instance for runtime data handling.
    """
    print("Generating city regions...")
    logging.debug("Entering generate_region function...")
    region_data = {}
    yaml_manager = YAMLManager(BASE_RUNTIME_DIR)  # Use the consolidated runtime directory

    # Directory for output files
    output_dir = r'C:\Users\Stuart\Python Scripts\scifiRPG\data\Test City\Regions'
    os.makedirs(output_dir, exist_ok=True)

    # Define types of locations by wealth level
    location_types_by_wealth = {
        "Rich": [(CorporateStore, 2), (Museum, 1), (Library, 1), (Shop, 3), (ElectricalRepairWorkshop, 1)],
        "Normal": [(Shop, 3), (Cafe, 3), (Park, 1), (Nightclub, 1), (ElectricalRepairWorkshop, 1), (Airport, 1), (Factory, 2), (HQ, 2)],
        "Poor": [(Stash, 5), (Factory, 2), (MechanicalRepairWorkshop, 1), (Shop, 3), (Mine, 1), (Powerplant, 1), (Port, 1), (Cafe, 3), (HQ, 3)],
    }

    # Predefined user-facing names for regions
    user_friendly_names = {
        "North": "NorthVille",
        "East": "Easternhole",
        "West": "Westborough",
        "South": "SouthVille",
        "Central": "Downtown",
    }

    for region, wealth in regions_with_wealth.items():
        locations = []  # Reset locations for each region
        wealth_location_types = location_types_by_wealth[wealth]

        # Ensure minimums first
        for loc_class, min_count in wealth_location_types:
            for _ in range(min_count):
                location = loc_class(
                    name=f"{loc_class.__name__}_{random.randint(1000, 9999)}",
                )
                locations.append(location.to_dict())

        # Add additional locations beyond the minimum
        additional_count = random.randint(3, 5)
        loc_classes, weights = zip(*wealth_location_types)
        for _ in range(additional_count):
            loc_class = random.choices(loc_classes, weights=weights, k=1)[0]
            location = loc_class(
                name=f"{loc_class.__name__}_{random.randint(1000, 9999)}",
            )
            locations.append(location.to_dict())

        # Create region data structure
        region_data[region] = {
            "name": region,
            "nameForUser": user_friendly_names.get(region, region),
            "wealth": wealth,
            "locations": locations,
        }

        # Serialize the region data to a JSON file
        region_file_path = os.path.join(output_dir, f"{region}.json")
        with open(region_file_path, 'w') as file:
            json.dump(region_data[region], file, indent=4)

        print(f"Data for {region} region written to {region_file_path}")

    print("City regions generation complete.")
    return region_data
