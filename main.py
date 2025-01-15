import time
import sys
import os
import logging
# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generators.generate import generate_city_data  #Import the city generation function
from generators.generateCharacters import generate_character_data
import display
import json
from loader import load_region_data
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
from utils import (ensure_file_exists, load_characters_and_generate_if_empty,
                    load_characters_and_generate_if_empty, generate_and_save_characters)
from character_creation import create_characters_as_objects  # Import the function to create characters

import display
print("Current Working Directory:", os.getcwd())
# Setup logging for debugging and tracking progress
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define a mapping from user-friendly names to the actual filenames
# Define the directory where the region JSON files are stored

# Test file access
test_region = "NorthVille"
try:
    test_data = load_region_data(test_region)
    print(f"Successfully loaded test data for region '{test_region}': {test_data}")
except Exception as e:
    print(f"Error during test: {e}")



def load_serialized_characters():
    try:
        with open("characters.json", "r") as f:
            data = json.load(f)
        characters = [Character(**char_data) for char_data in data]
        logging.info(f"Loaded characters: {characters}")
        return characters
    except FileNotFoundError:
        logging.error("No serialized character data found.")
        return []
    except Exception as e:
        logging.error(f"Error loading serialized characters: {e}")
        return []

def start_gameplay(current_character, region_data):
    """
    Manages the gameplay flow by coordinating character interaction with region data.
    
    Args:
        current_character (dict): The selected character's data.
        region_data (dict): Data for the selected region.
    """
    print("\n=== Gameplay Start ===\n")

    # Display character details using display module
    display.show_character_details(current_character)

    # Show available shops using display module
    shops = region_data.get("shops", [])
    display.show_shops_in_region(shops)

    # Display inventory for each shop
    for shop in shops:
        display.show_shop_inventory(shop)

def main():
    print("Welcome.")
    print("Gameplay selected. Initializing character selection.")

    try:
        # Get characters using the character creation function
        characters = create_characters_as_objects()  # Generate the character list
        
        # Call select_character_menu, passing the generated character data
        current_character = display.select_character_menu(characters)
        
        if current_character:
            print(f"Selected character: {current_character.name}")
        else:
            print("No character selected. Exiting the game.")
            return

        # Select region
        selected_region = display.select_region_menu()
        if not selected_region:
            print("No region selected. Exiting the game.")
            return

        print(f"Region '{selected_region}' selected.")

        # Load region data using loader.py
        try:
            region_data = load_region_data(selected_region)
            print(f"Region data loaded successfully for '{selected_region}'.")
            start_gameplay(current_character, region_data)
        except Exception as e:
            print(f"Failed to load region data: {e}")

    except Exception as e:
        print(f"Error: {e}")

    
    # You can uncomment the following line if you have the required function
    # _check_missing_keys(region_data, required_keys)  # For now, it's just a placeholder
    


if __name__ == "__main__":
    main()  # Call the main function to start the program