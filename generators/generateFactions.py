import os
import json
import yaml
import random
from .generateCorps import generate_corporations
from .generateGangs import generate_gangs
from characters import VIP, RiotCop
from generators.generateState import generate_state
from common import get_project_root, get_file_path
#ALL files use this to get the project root

def generate_factions():
    """
    Generate factions (gangs and corporations) for the city.
    Assign them HQ locations and update the city data.
    """
    print("Generating factions...")

    """ # Load existing city data
    with open("test_city.json", "r") as file:
        city_data = json.load(file)
    # Load locations data
    with open("locations.json", "r") as file:
        locations_data = json.load(file) """

    # Determine the number of gangs and corporations
    num_gangs = random.randint(2, 3)
    num_corps = random.randint(4, 5)

    print(f"Generating {num_gangs} gangs and {num_corps} corporations.")

    # Generate gang and corporation data
    generate_gangs()  # Ensure gangs.json is created
    generate_corporations()  # Ensure corporations.json is created
    generate_state()
    # Combine gangs and corporations into a single factions structure
    factions = []

    # Load gangs
    try:
        with open("data/gangs.json", "r") as file:
            gangs = json.load(file)
            factions.extend(gangs)
    except FileNotFoundError:
        print("No gangs data found. Skipping gangs.")

    # Load corporations
    try:
        with open("data/corporations.json", "r") as file:
            corporations = json.load(file)
            factions.extend(corporations)
    except FileNotFoundError:
        print("No corporations data found. Skipping corporations.")


    # Load the State
    try:
        with open("data/state.json", "r") as file:
            state = json.load(file)
            factions.append(state)
    except FileNotFoundError:
        print("No State data found. Skipping the State.")

    # Save combined factions data
    with open(output_path, "w") as file:
        json.dump({"factions": factions}, file, indent=4)
    print(f"Factions data saved to {output_path}")

    # Save combined factions data
    with open(output_path, "w") as file:
        json.dump({"factions": factions}, file, indent=4)
    print(f"Factions data saved to {output_path}")

    # Assign HQs for gangs and corporations
    available_locations = [
        loc for loc in locations_data if loc["type"] == "HQ"
    ]
    random.shuffle(available_locations)

    # Check if there are enough HQs
    if len(available_locations) < (num_gangs + num_corps):
        raise ValueError("Not enough HQ locations available!")

    gang_hqs = available_locations[:num_gangs]
    corp_hqs = available_locations[num_gangs:num_gangs + num_corps]

    # Assign gangs and corporations to regions
    for region in city_data["city"]:
        if region != "Central":
            city_data["city"][region]["factions"] = random.sample(
                gangs + corps, k=random.randint(1, len(gangs + corps))
            )

    #upadte this using from common import get_project_root, get_file_path
region_file = get_file_path("data", "Test City", "Locations", "test_city.json")

try:
    with open(region_file, "w") as file:
        json.dump(city_data, file, indent=4)
    print(f"Updated: {region_file}")
except FileNotFoundError as e:
    print(f"Error updating region file: {e}")

    print("Factions generated and test_city.json updated.")




