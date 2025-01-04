import json
import random
from .generateCorps import generate_corporations
from .generateGangs import generate_gangs

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

if __name__ == "__main__":
    generate_factions()
