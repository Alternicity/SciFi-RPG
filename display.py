from tabulate import tabulate
from characters import Character
import logging
import time
from utils import create_characters_as_objects


def display_menu(characters):
    """
    Main menu to manage game functionality using print and input.
    """
    while True:
        print("=== Main Menu ===")
        print("1: Create Characters (Game Objects)")
        print("2: Create Characters (Serialized Data)")
        print("3: Load Serialized Characters")
        print("4: Play/Test Game")
        print("5: Exit")

        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
            if choice == 1:
                create_characters_as_objects()
            elif choice == 2:
                print("Feature to create and serialize characters is under development.")
            elif choice == 3:
                print("Feature to load serialized characters is under development.")
            elif choice == 4:
                print("Feature to play/test game is under development.")
            elif choice == 5:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            stdscr.clear()
            stdscr.addstr("Invalid option. Please press 1, 2, or 3.\n")
            stdscr.refresh()
            time.sleep(1)

def list_characters(characters):
    """
    Display a list of existing characters in a table format.
    """
    print("Listing Characters, list_characters().")

    if not characters:
        print("No existing characters.")
        return

    # Prepare the character data for tabulation
    character_data = [
        [character.name, character.faction]
        for character in characters
    ]

    # Create a table with headers
    headers = ["Name", "Faction"]
    table = tabulate(character_data, headers, tablefmt="grid")

    # Print the table
    print(table)

if __name__ == "__main__":
    characters = []  # Initialize characters list
    display_menu(characters)
