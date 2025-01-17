import random
import json
import os

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from location import (
    HQ, Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalRepairWorkshop, Stash,
    Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Park, Museum, Library
)
from location_security import Security
def generate_region(regions_with_wealth):
    """
    Generate regions and return their wealth levels and locations.
    """
    print("Generating city regions...")

    region_data = {}

    # Directory for output files
    output_dir = r'C:\Users\Stuart\Python Scripts\scifiRPG\data\Test City\Regions'
    os.makedirs(output_dir, exist_ok=True)

    # Define types of locations by wealth level
    location_types_by_wealth = {
        "Rich": [CorporateStore, Museum, Library, HQ],
        "Normal": [Shop, Cafe, Park, Nightclub],
        "Poor": [Stash, Factory, MechanicalRepairWorkshop],
    }

    for region, wealth in regions_with_wealth.items():
        locations = []
        wealth_location_types = location_types_by_wealth[wealth]

        for loc_class in wealth_location_types:
            num_locations = max(3, random.randint(1, 5))  # Minimum 3 locations per type
            for _ in range(num_locations):
                location = loc_class(
                    name=f"{loc_class.__name__}_{random.randint(1000, 9999)}",
                    # Add location-specific details...
                )
                locations.append(location.to_dict())

        region_data[region] = {
            "wealth": wealth,
            "locations": locations,
        }

        # Serialize the region data to a JSON file
        region_file_path = os.path.join(output_dir, f"{region}.json")
        with open(region_file_path, 'w') as file:
            json.dump(region_data, file, indent=4)

        print(f"Data for {region} region written to {region_file_path}")

    print("City regions generation complete.")
    return region_data

# Example usage
if __name__ == "__main__":
    # Example region wealth mapping
    regions_with_wealth = {
        "North": "Rich",
        "South": "Normal",
        "East": "Poor",
        "West": "Normal",
        "Central": "Rich",
    }
    generate_region(regions_with_wealth)
