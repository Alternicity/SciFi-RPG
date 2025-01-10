import time
import sys
import os
import logging
# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generators.generate import generate_city_data  #Import the city generation function
from generators.generateCharacters import generate_character_data
from display import display_menu
import json
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
from utils import (ensure_file_exists, load_characters_and_generate_if_empty,
                    load_characters_and_generate_if_empty, generate_and_save_characters)
#from create import create_characters_as_objects, create_and_serialize_characters
import display
print("Current Working Directory:", os.getcwd())
# Setup logging for debugging and tracking progress
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



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

def play_game_with_characters(characters):
    if characters is None:
        logging.info("Playing game with in-memory characters...")
    else:
        logging.info("Playing game with loaded characters...")
    # Placeholder for actual game logic
    pass

def main():
    
    characters_file_path = r"data\Test City\Characters\characters.json"
    
    # Ensure the file exists before attempting to load it
    ensure_file_exists(characters_file_path, default_data=[])  # Default to an empty list for characters

    # Load characters from the file
    #characters = load_characters_from_file(characters_file_path)

    # Load characters, generating them if the file is empty
    characters = load_characters_and_generate_if_empty(characters_file_path)
    logging.debug(f"Loaded characters: {characters}")
    #current_character = None

    display_menu(characters)

if __name__ == "__main__":
    main()  # Call the main function to start the program