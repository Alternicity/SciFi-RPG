import time
import sys
import os
import logging
# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generators.generate import generate_city_data  #Import the city generation function
from generators.generateCharacters import generate_character_data
from display import show_shops_in_region, select_region_menu, show_character_details, show_shop_inventory, display_menu, select_character_menu
import json
from loader import load_region_data
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
from utils import (ensure_file_exists, load_characters_and_generate_if_empty,
                    load_characters_and_generate_if_empty, generate_and_save_characters)
from character_creation import create_characters_as_objects  # Import the function to create characters


print("Current Working Directory:", os.getcwd())
# Setup logging for debugging and tracking progress
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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

    #character_region = "North"  # This can be dynamic based on the character's current location
    # Display character details using display module
    show_character_details(current_character)

    # Display the shops in the current region
    shops = region_data.get("shops", []) #does region_data contain the shops data?
    show_shops_in_region(shops)

    # Display inventory for each shop
    for shop in shops:
        show_shop_inventory(shop)

def main():
    print("Welcome.")
    print("Gameplay selected. Initializing character selection.")

    try:
        # Get characters using the character creation function
        characters = create_characters_as_objects()  # Generate the character list
        
        # Call select_character_menu, passing the generated character data
        current_character = select_character_menu(characters)
        
        if not current_character:
            print("No character selected. Exiting the game.")
            return
        
        print(f"Selected character: {current_character.name}")
        
        # Now, select the region
        selected_region = select_region_menu()
        if not selected_region:
            print("No region selected. Exiting the game.")
            return
        
        print(f"Region '{selected_region}' selected.")

        # Load region data
        region_data = load_region_data(selected_region)
        if not region_data:
                print(f"No region data found for '{selected_region}'.")
                return
        print(f"Region data loaded successfully for '{selected_region}'.")

        # Show shops in the selected region
        show_shops_in_region(selected_region)

        # Ensure you're passing `region_data` to the `start_gameplay` function
        start_gameplay(current_character, region_data)

    except Exception as e:
        print(f"An error occurred: {e}")

    
    # You can uncomment the following line if you have the required function
    # _check_missing_keys(region_data, required_keys)  # For now, it's just a placeholder
    


if __name__ == "__main__":
    main()  # Call the main function to start the program