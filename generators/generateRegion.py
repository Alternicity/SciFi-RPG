# generateRegion.py
# Generates city regions and assigns locations within them.

import random
import json

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
        'North': ['Shop', 'Cafe', 'Nightclub', 'Warehouse'],
        'South': ['Shop', 'HQ', 'Factory', 'Nightclub'],
        'East': ['Cafe', 'Sports Centre', 'Warehouse', 'Research Lab'],
        'West': ['HQ', 'Cafe', 'Shop', 'Nightclub'],
        'Central': ['HQ', 'Museum', 'Power Plant', 'Repair Workshops']
    }

    # Define possible wealth levels for regions
    wealth_levels = ['Rich', 'Normal', 'Poor']

    # Locations data structure for storing regions and their locations
    city_regions = {}

    # Assign locations and wealth levels to each region
    for region in regions:
        city_regions[region] = {
            'wealth': random.choice(wealth_levels),
            'locations': []
        }

        # Ensure no ports are in the Central region
        if region == 'Central':
            location_types = [location for location in region_types[region] if location != 'Port']
        else:
            location_types = region_types[region]

        # Randomly assign locations to each region
        for location_type in location_types:
            num_locations = random.randint(1, 3)  # Number of locations to generate per region
            for _ in range(num_locations):
                location_name = f"{location_type}_{random.randint(1000, 9999)}"
                city_regions[region]['locations'].append({
                    'name': location_name,
                    'type': location_type,
                    'security': random.choice(['Low', 'Medium', 'High']),
                    'upkeep': random.choice(['Low', 'Medium', 'High']),
                    'entrances': random.randint(1, 3),
                    'secret_entrances': random.choice([True, False]),
                })

    # Serialize the city regions data to a JSON file
    output_file = r'C:\Users\Stuart\Python Scripts\scifi RPG\data\Test City\Regions\city_regions.json'
    with open(output_file, 'w') as file:
        json.dump(city_regions, file, indent=4)

    print("City regions generation complete.")
    print(f"Data written to {output_file}")

# Example usage
if __name__ == "__main__":
    generate_region()
