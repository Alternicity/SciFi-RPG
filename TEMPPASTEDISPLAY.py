#Temp paste of old display.py

import curses
from tabulate import tabulate
from characters import Character
import logging
import time

def display_menu(stdscr):
    """
    Main menu to manage game functionality.
    """
    stdscr.clear()
    stdscr.addstr("=== Main Menu ===\n")
    stdscr.addstr("1: Create Characters (Game Objects)\n")
    stdscr.addstr("2: Create Characters (Serialized Data)\n")
    stdscr.addstr("3: Load Serialized Characters\n")
    stdscr.addstr("4: Play/Test Game\n")
    stdscr.addstr("5: Exit\n")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        try:
            choice = int(chr(key))
            if choice == 1:
                create_characters_as_objects()
            elif choice == 2:
                create_and_serialize_characters()
            elif choice == 3:
                characters = load_serialized_characters()
                play_game_with_characters(characters)
            elif choice == 4:
                play_game_with_characters(None)  # Use in-memory characters
            elif choice == 5:
                break
            else:
                stdscr.addstr("Invalid choice. Please select a valid option.\n")
        except ValueError:
            stdscr.addstr("Invalid input. Please press a valid number.\n")
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
    """
    Main application loop using curses.
    """
    characters = []  # Initialize characters list here or load it as needed

    while True:
        display_menu(stdscr)
        key = stdscr.getch()

        if key == ord('1'):
            stdscr.clear()
            stdscr.addstr("Starting city generation...\n")
            stdscr.refresh()
            # Replace this with actual city generation logic
            # Call to generate.py here if required
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
    curses.wrapper(main)
