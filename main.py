import time
import sys
import os
import logging
# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generators.generate import generate_city_data  #Import the city generation function
from generators.generateCharacters import generate_character_data
import curses
from characters import Character
import json
from characters import Boss, Captain, Employee, VIP, RiotCop


print("Current Working Directory:", os.getcwd())
# Setup logging for debugging and tracking progress
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_file_exists(file_path, default_data=None):
    """
    Ensure the specified file exists. If it doesn't, create it with the provided default data.
    Args:
        file_path (str): The path of the file to check.
        default_data (dict or list): The default data to write if the file doesn't exist.
    """
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directories exist
        with open(file_path, 'w') as f:
            json.dump(default_data or [], f, indent=4)  # Write valid JSON default data
        print(f"Created new file at: {file_path}")

def load_characters_from_file(file_path):
    """
    Load character data from a JSON file.
    Args:
        file_path (str): The path to the character JSON file.
    Returns:
        list: A list of character data.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)  # Attempt to parse JSON
            if not isinstance(data, list):
                raise ValueError("Invalid data structure: Expected a list of characters.")
            logging.debug(f"Loaded character data: {data}")
            return data
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in {file_path}. Resetting to default.")
        ensure_file_exists(file_path, default_data=[])  # Reset file with default content
        return []  # Return an empty list
    except Exception as e:
        logging.error(f"Failed to load characters: {e}")
        #here call generate_and_save_characters()
        return []  # Return an empty list if an unexpected error occurs

def generate_and_save_characters(file_path, num_characters=5):
    """
    Generate characters and save them to the specified file.
    Args:
        file_path (str): The path to the character JSON file.
        num_characters (int): Number of characters to generate.
    """
    # Generate a list of Character objects
    try:
        characters = [
            Boss(name="Big Boss", faction="Blue Gang"),
            Captain(name="Blue Captain", faction="Blue Gang"),
            Employee(name="Corporate Employee", faction="Blue Corporation"),
            VIP(name="VIP", faction="Elite Corporation"),
            RiotCop(name="Cop One"),
        ]
    except Exception as e:
        logging.error(f"Error while generating characters: {e}")
    #logging.debug(f"Serializing character: {character.name}, {type(character).__name__}")
    

def load_characters_and_generate_if_empty(file_path):
    """
    Load characters from the JSON file. If empty, generate and save new characters.
    Args:
        file_path (str): Path to the character JSON file.
    Returns:
        list: List of characters.
    """
    characters = load_characters_from_file(file_path)
    if not characters:
        logging.info("No characters found. Generating new characters...")
        generate_and_save_characters(file_path)
        characters = load_characters_from_file(file_path)  # Reload after generation
    return characters

def display_menu(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the RPG Generator!\n")
    stdscr.addstr("1: Generate City\n")
    stdscr.addstr("2: Choose Character\n")
    stdscr.addstr("3: Exit\n")
    stdscr.refresh()

def choose_character_menu(stdscr, characters):
    """
    Display a menu for selecting a character.
    Args:
        stdscr: Curses screen object.
        characters (list): List of character data.
    Returns:
        Character: The selected Character object.
    """
    stdscr.clear()
    if not characters:
        stdscr.addstr("No characters available. Generating new characters... (chooseCharacter menu)\n")
        stdscr.refresh()
        time.sleep(2)  # Simulate loading delay
        return None

    stdscr.addstr("=== Choose a Character ===\n")
    for index, character in enumerate(characters, start=1):
        stdscr.addstr(f"{index}: {character['name']} - Role: {character['char_role']}\n")

    stdscr.addstr("\nEnter the number of the character you want to select: ")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        try:
            choice = int(chr(key))
            if 1 <= choice <= len(characters):
                selected_character_data = characters[choice - 1]
                logging.debug(f"Selected character data: {selected_character_data}")
                
                selected_character = Character(**selected_character_data)
                logging.debug(f"Selected character data: {selected_character_data}")
                print(f"Character object created: {selected_character.name} (Role: {selected_character.char_role})")
                return selected_character
            else:
                stdscr.addstr("Invalid selection. Please choose a valid number.\n")
        except (ValueError, IndexError):
            stdscr.addstr("Invalid input. Please press a valid number.\n")
        stdscr.refresh()

def main(stdscr):
    

    characters_file_path = r"data\Test City\Characters\characters.json"
    
    # Ensure the file exists before attempting to load it
    ensure_file_exists(characters_file_path, default_data=[])  # Default to an empty list for characters

    # Load characters from the file
    #characters = load_characters_from_file(characters_file_path)

    # Load characters, generating them if the file is empty
    characters = load_characters_and_generate_if_empty(characters_file_path)
    logging.debug(f"Loaded characters: {characters}")
    current_character = None


    while True:
        display_menu(stdscr)
        key = stdscr.getch()

        if key == ord('1'):
            stdscr.clear()
            stdscr.addstr("Starting city generation...\n")
            stdscr.refresh()
            # Replace this with actual city generation logic
            #a call to generate.py here?
            stdscr.addstr("City generation complete.\n")
            stdscr.refresh()
            time.sleep(1)
        elif key == ord('2'):
            current_character = choose_character_menu(stdscr, characters)
            if current_character:
                stdscr.clear()
                stdscr.addstr(f"You are now controlling: {current_character.name}\n")
                stdscr.refresh()
                stdscr.getch()

        elif key == ord('3'):
            stdscr.clear()
            stdscr.addstr("Exiting...\n")
            stdscr.refresh()
            break
        else:
            stdscr.clear()
            stdscr.addstr("Invalid option. Please press 1, 2, or 3.\n")
            stdscr.refresh()
            time.sleep(1)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)