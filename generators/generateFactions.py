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


    # Determine the number of gangs and corporations
    num_gangs = random.randint(2, 3)
    num_corps = random.randint(4, 5)
    print(f"Generating {num_gangs} gangs and {num_corps} corporations.")

    # Generate gang and corporation data
    generate_gangs()  # Ensure gangs.json is created
    generate_corporations()  # Ensure corporations.json is created
    generate_state()
    # Combine gangs and corporations into a single factions structure

    # Load gang and corporation data
    gangs = []
    corporations = []
    try:
        with open(r"scifiRPG\data\Test City\Factions\Gangs", "r") as file:
            gangs = json.load(file)
    except FileNotFoundError:
        print("No gangs data found.")

    try:
        with open(r"scifiRPG\data\Test City\Factions\Corps", "r") as file:
            corporations = json.load(file)
    except FileNotFoundError:
        print("No corporations data found.")


    # Load the State
    try:
        with open(r"scifiRPG\data\Test City\Factions\TheState", "r") as file:
            state = json.load(file)
            factions.append(state)
    except FileNotFoundError:
        print("No State data found. Skipping the State.")

    # Load region files dynamically
    regions_path = get_file_path("data", "Regions")
    region_files = [f for f in os.listdir(regions_path) if f.endswith(".json")]

    for region_file in region_files:
        region_path = os.path.join(regions_path, region_file)
        print(f"Processing region: {region_file}")

        # Load region data
        with open(region_path, "r") as file:
            region_data = json.load(file)

        # Find HQ locations
        hq_locations = [
            loc for loc in region_data.get("locations", []) if loc.get("type") == "HQ"
        ]
        if not hq_locations:
            print(f"No HQ locations in {region_file}. Skipping.")
            continue

        # Assign factions to HQs
        random.shuffle(hq_locations)
        num_to_assign = min(len(hq_locations), num_gangs + num_corps)
        assigned_gangs = gangs[:num_to_assign // 2]
        assigned_corps = corporations[:num_to_assign // 2]

        for idx, hq in enumerate(hq_locations):
            if idx < len(assigned_gangs):
                hq["faction"] = assigned_gangs[idx]
            elif idx < len(assigned_gangs) + len(assigned_corps):
                hq["faction"] = assigned_corps[idx - len(assigned_gangs)]

        # Save updated region data
        with open(region_path, "w") as file:
            json.dump(region_data, file, indent=4)
        print(f"Updated region: {region_file}")

    print("Faction assignment complete.")




