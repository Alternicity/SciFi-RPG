
import sys
import os
import logging
from common import get_project_root
#ALL files use this to get the project root

# Debug: Print current directory and sys.path
#print(f"Running main.py from: {os.getcwd()}")
#print(f"sys.path: {sys.path}")

# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

""" try:
    from generators.generate import generate_city_data
    print("Imported generate_city_data successfully!")
except ImportError as e:
    print(f"ImportError: {e}") """

from generators.generate import generate_city_data
from generators.generateCharacters import generate_character_data
from display import show_locations_in_region, select_region_menu, show_character_details, show_shop_inventory, display_menu, select_character_menu
from loader import load_region_data
from characters import (Boss, Captain, Employee, VIP, RiotCop, CorporateAssasin, Employee, GangMember,
                        CEO, Manager, CorporateSecurity, Civilian)
from utils import (ensure_file_exists, load_characters_and_generate_if_empty, generate_and_save_characters)
from character_creation import create_characters_as_objects  # Import character creation function
from city_utils import regenerate_city_data  # Import from the new module
import gameplay
# main.py can now use regenerate_city_data without redefining it

# Debug: Print current directory and sys.path
#print(f"Running main.py from: {os.getcwd()}")
#print(f"sys.path: {sys.path}")


def load_serialized_characters():
    """Load character data from serialized JSON."""
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

def start_gameplay(current_character, region_data):
    """Manage gameplay flow with character interaction and region data."""
    print("\n=== Gameplay Start ===\n")
    show_character_details(current_character)
    shops = region_data.get("shops", [])
    show_locations_in_region(shops)
    for shop in shops:
        show_shop_inventory(shop)


def main():
    """Main game loop."""
    while True:
        selected_character, region = display_menu()
        if selected_character and region:
            print(f"Starting game with {selected_character.name} in {region}.")
            gameplay.gameplay(selected_character, region)  # Pass control to gameplay()
            break
        else:
            print("Failed to start game. Returning to main menu.")

if __name__ == "__main__":
    main()  # Start the game
