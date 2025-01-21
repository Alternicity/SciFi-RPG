""" Structure of generateCity.py
Aggregate Data: Collect data from the JSON files created by the lower-tier generators (generateRegions, generateShops, etc.).
Merge or Organize: Combine this data into a comprehensive city structure.
Save to test_city.json: Ensure the aggregated city data is stored in a single JSON file """

import json
from pathlib import Path

def aggregate_city_data(output_path="test_city.json"):
    """
    Aggregates data from lower-tier generators into a cohesive city representation.
    """
    base_dir = Path("data")  # Adjust the path as needed
    city_data = {"regions": [], "factions": [], "locations": []}

    # Load regions
    try:
        with open(base_dir / "regions.json", "r") as file:
            city_data["regions"] = json.load(file)["regions"]
    except FileNotFoundError:
        print("No regions data found. Skipping regions.")

    # Load factions (including gangs and corporations)
    try:
        with open(base_dir / "factions.json", "r") as file:
            city_data["factions"] = json.load(file)["factions"]
    except FileNotFoundError:
        print("No factions data found. Skipping factions.")

    # Load locations (shops, enrichment areas, etc.)
    try:
        with open(base_dir / "locations.json", "r") as file:
            city_data["locations"] = json.load(file)["locations"]
    except FileNotFoundError:
        print("No locations data found. Skipping locations.")

    # Write the aggregated city data to test_city.json
    with open(output_path, "w") as file:
        json.dump(city_data, file, indent=4)
    print(f"Aggregated city data saved to {output_path}")


if __name__ == "__main__":
    aggregate_city_data()
