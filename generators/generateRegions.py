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
def generate_region():
    """
    Generate city regions, assign them specific locations, 
    and assign a wealth level to each region. 
    Ensure no ports are located in the Central region.
    """
    print("Generating city regions...")

    # Define the city regions
    regions = ['North', 'South', 'East', 'West', 'Central']

    # Define types of locations that may be generated within each region
    region_types = {
        'North': [Shop, Cafe, Nightclub, Stash, Park],
        'South': [Shop, HQ, Factory, Nightclub, Powerplant],
        'East': [Cafe, MechanicalRepairWorkshop, ElectricalRepairWorkshop, Mine, Airport],
        'West': [HQ, Cafe, CorporateStore, Stash, Nightclub],
        'Central': [HQ, CorporateStore, Museum, ElectricalRepairWorkshop, Shop, Library],
    }

    # Define possible wealth levels for regions
    wealth_levels = ['Rich', 'Normal', 'Poor']

    # Ensure no ports are in the Central region
    region_types['Central'] = [loc for loc in region_types['Central'] if loc != Port]

    # Directory for output files
    output_dir = r'C:\Users\Stuart\Python Scripts\scifiRPG\data\Test City\Regions'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate and serialize data for each region
    for region in regions:
        region_data = {
            'wealth': random.choice(wealth_levels),
            'locations': []
        }

        # Instantiate location objects
        for loc_class in region_types[region]:
            num_locations = random.randint(1, 3)  # Number of locations per type
            for _ in range(num_locations):
                location = loc_class(
                    name=f"{loc_class.__name__}_{random.randint(1000, 9999)}",
                    security=Security(
                        level=random.randint(1, 5),
                        guards=random.choices(["Basic Guard", "Elite Guard"], k=random.randint(1, 3)),
                        difficulty_to_break_in=random.randint(1, 10),
                        surveillance=random.choice([True, False]),
                        alarm_system=random.choice([True, False])
    ),
                    
                    entrance=random.randint(1, 3),
                    secret_entrance=random.choice([True, False]),
                    upkeep=random.randint(10, 100)  # This is fine because upkeep is defined in the base class
                )
                # Serialize location attributes
                region_data['locations'].append(location.to_dict())

        # Serialize the region data to a JSON file
        region_file_path = os.path.join(output_dir, f"{region}.json")
        with open(region_file_path, 'w') as file:
            json.dump(region_data, file, indent=4)

        print(f"Data for {region} region written to {region_file_path}")

    print("City regions generation complete.")

# Example usage
if __name__ == "__main__":
    generate_region()
