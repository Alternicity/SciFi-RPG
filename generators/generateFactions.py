import json
import yaml
import random
from .generateCorps import generate_corporations
from .generateGangs import generate_gangs
from characters import VIP, RiotCop

def generate_factions():
    """
    Generate factions (gangs and corporations) for the city.
    Assign them HQ locations and update the city data.
    """
    print("Generating factions...")

    # Load existing city data
    with open("test_city.json", "r") as file:
        city_data = json.load(file)

    # Load locations data
    with open("locations.json", "r") as file:
        locations_data = json.load(file)

    # Determine the number of gangs and corporations
    num_gangs = random.randint(2, 3)
    num_corps = random.randint(4, 5)

    print(f"Generating {num_gangs} gangs and {num_corps} corporations.")

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

    # Generate gangs
    gangs = generate_gangs(num_gangs, gang_hqs)

    # Generate corporations
    corps = generate_corps(num_corps, corp_hqs)

    # Assign gangs and corporations to regions
    for region in city_data["city"]:
        if region != "Central":
            city_data["city"][region]["factions"] = random.sample(
                gangs + corps, k=random.randint(1, len(gangs + corps))
            )

    # Update test_city.json
    with open("test_city.json", "w") as file:
        json.dump(city_data, file, indent=4)

    print("Factions generated and test_city.json updated.")

def generate_state(file_path="data/state.yaml", tax_rate=0.15, num_riot_cops=10):
    """
    Generates or overwrites the state.yaml file with the State's details.
    
    Args:
        file_path (str): The path to save the state.yaml file.
        tax_rate (float): The tax rate applied by the State.
        num_riot_cops (int): The number of RiotCops to assign to the State.
    """
    # Create a VIP character for the State
    vip = VIP(name="State Leader", position="Governor", influence=90)

    # Generate RiotCops
    riot_cops = [
        RiotCop(name=f"RiotCop_{i+1}")
        for i in range(num_riot_cops)
    ]

    # Define the State's details
    state_data = {
        "name": "The State",
        "type": "corporation",
        "affiliation": "none",
        "resources": 10000,
        "tax_rate": tax_rate,
        "laws": ["Law 1", "Law 2", "Law 3"],
        "goals": [
            {"goal": "retain dominance", "priority": "high", "reward": 2000},
            {"goal": "extract value", "priority": "high", "reward": 1500},
        ],
        "personnel": {
            "VIP": {
                "name": vip.name,
                "influence": vip.influence,
            },
            "RiotCops": [
                {"name": cop.name}
                for cop in riot_cops
            ],
        },
    }

    # Write the state data to a YAML file
    with open(file_path, "w") as file:
        yaml.dump(state_data, file, default_flow_style=False)
    
    print(f"State data saved to {file_path}")

# Example call
generate_state()

if __name__ == "__main__":
    generate_factions()
