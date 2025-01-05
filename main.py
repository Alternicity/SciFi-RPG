import time
import sys
import os
import logging
# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generators.generate import generate_city_data  #Import the city generation function
import curses
from characters import Character

print("Current Working Directory:", os.getcwd())
# Setup logging for debugging and tracking progress
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_characters_from_file(file_path):
    logging.debug(f"Attempting to load characters from {file_path}")
    if not os.path.exists(file_path):
        logging.warning(f"Character file {file_path} not found.")
        return []

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            logging.debug(f"Loaded data: {data}")
            return [Character(**char_data) for char_data in data.get("characters", [])]
    except Exception as e:
        logging.error(f"Failed to load characters: {e}")
        return []


def display_menu(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the RPG Generator!\n")
    stdscr.addstr("1: Generate City\n")
    stdscr.addstr("2: Choose Character\n")
    stdscr.addstr("3: Exit\n")
    stdscr.refresh()

def choose_character_menu(stdscr, characters):
    stdscr.clear()

    if not characters:
        stdscr.addstr("No characters available to choose from.\n")
        stdscr.addstr("Press any key to return to the main menu.\n")
        stdscr.refresh()
        stdscr.getch()
        return None

    stdscr.addstr("=== Choose a Character ===\n")
    for index, character in enumerate(characters, start=1):
        stdscr.addstr(f"{index}: {character.name} - Role: {character.char_role}\n")

    stdscr.addstr("\nEnter the number of the character you want to select: ")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        try:
            choice = int(chr(key))
            if 1 <= choice <= len(characters):
                selected_character = characters[choice - 1]
                stdscr.clear()
                stdscr.addstr(f"You selected: {selected_character.name} (Role: {selected_character.char_role})\n")
                stdscr.addstr("Press any key to return to the main menu.\n")
                stdscr.refresh()
                stdscr.getch()
                return selected_character
            else:
                stdscr.addstr("Invalid selection. Please choose a valid number.\n")
        except (ValueError, IndexError):
            stdscr.addstr("Invalid input. Please press a valid number.\n")
        stdscr.refresh()

def main(stdscr):
    characters_file_path = "data/Test City/test_city.json"
    characters = load_characters_from_file(characters_file_path)

    while True:
        display_menu(stdscr)
        key = stdscr.getch()

        if key == ord('1'):
            stdscr.clear()
            stdscr.addstr("Starting city generation...\n")
            stdscr.refresh()
            # Replace this with actual city generation logic
            stdscr.addstr("City generation complete.\n")
            stdscr.refresh()
            time.sleep(1)
        elif key == ord('2'):
            choose_character_menu(stdscr, characters)
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