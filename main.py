
import sys
import os
import logging
from common import get_project_root, BASE_REGION_DIR
#ALL files use this to get the project root
from loader import load_region_data
from display import main_menu
from gameplay import gameplay

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from generators.generate import generate_city_data
from generators.generateCharacters import generate_character_data
from display import show_locations_in_region, select_region_menu, show_character_details, show_shop_inventory, main_menu, select_character_menu
from loader import load_region_data
from characters import (Boss, Captain, Employee, VIP, RiotCop, CorporateAssasin, Employee, GangMember,
                        CEO, Manager, CorporateSecurity, Civilian)
from utils import (ensure_file_exists, load_characters_and_generate_if_empty, generate_and_save_characters)
from character_creation import create_characters_as_objects  
from city_utils import regenerate_city_data  
import gameplay


def load_serialized_characters():
    try:
        with open("characters.json", "r") as f:
            data = json.load(f)
        characters = [Character(**char_data) for char_data in data]
        #logging.info(f"Loaded characters: {characters}")
        return characters
    except FileNotFoundError:
        #logging.error("No serialized character data found.")
        return []
    except Exception as e:
        logging.error(f"Error loading serialized characters: {e}")
        return []

def main():
    """Main game loop."""
    while True:
        selected_character, region = main_menu()
        if selected_character and region:
            # Set the character's initial location
            selected_character.update_location(region, None)
            print(f"Starting game with {selected_character.name} in {region.nameForUser}.")
            gameplay.gameplay(selected_character, region)  # Pass control to gameplay()
        else:
            print("Failed to start game. Returning to main menu.")

def start_gameplay(current_character, region_data): #Is this still used?
    """Manage gameplay flow with character interaction and region data."""
    print("\n=== Gameplay Start ===\n")

    show_character_details(current_character)
    print(f"Current character: {current_character}")

    shops = region_data.get("shops", [])
    print(f"Region data type: {type(region_data)}")
    #is it an Object? Does this reflect the charcater's current_location var?

    show_locations_in_region(shops) 
    for shop in shops:
        show_shop_inventory(shop)


if __name__ == "__main__":
    main()