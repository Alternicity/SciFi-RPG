import json
import yaml
import random
from InWorldObjects import Pistol, Weapon, RangedWeapon, Medkit
from characters import Character
from inventory import Inventory
from loader import load_data
from generators.generateStore import generate_stores
from store import Store, Vendor, CorporateDepot, Stash, Dealer
from morale import adjust_morale
import sys
print(sys.path)

# Load the city data
city_data = {}

try:
    with open('data/Locations/test_city.json', 'r') as f:
        test_city_data = json.load(f)  # Should this utilize load_data?
        city_data.update(test_city_data)

    with open('data/Locations/Southville.json', 'r') as f:
        southville_data = json.load(f)
        city_data.update(southville_data)
except FileNotFoundError as e:
    print(f"Error loading city data: {e}")


def display_status():
    print("City Status:")
    for region, data in city_data.get("regions", {}).items():
        print(f"\nRegion: {region}")
        for faction in data.get("factions", []):
            print(f"  Faction: {faction}")
        for character in data.get("characters", []):
            print(f"    {character['name']} - Loyalty: {character['loyalties'].get(faction, 0)}")


def main():
    # Placeholder for loading or generating characters
    # This will be implemented in generateCharacters.py
    # For now, we use manual test cases for characters

    # Test character setup (to be replaced later)
    john = Character(name="John", char_role="Employee", entity_id=1, wallet=500)
    jane = Character(name="Jane", char_role="Employee", entity_id=2, wallet=10)

    # Placeholder for store generation (to be replaced by generate_stores)
    pistol = Pistol()
    medkit = Medkit()

    # Test buying items
    john.buy(pistol)  # Should work, as the wallet is sufficient
    john.buy(medkit)  # Should work, as the wallet still has money

    jane.buy(pistol)  # Should fail, not enough money

    # Display city status for debugging
    display_status()

if __name__ == "__main__":
    main()
