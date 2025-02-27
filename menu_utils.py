#menu_utils.py
from tabulate import tabulate
from display import display_world
from typing import Dict, Any


""" try:
    from main import setup_game
    print("initialize_regions successfully imported.")
except ImportError as e:
    print(f"Failed to import initialize_regions: {e}") """

    
def main_menu():
    while True:
        """Display the main menu and return the user choice. Not a gameplay menu itself"""
        print("\n=== Main Menu ===")
        print("1: Play/Test Game")
        print("2: Show world")
        print("6: Exit")

        choice = get_user_choice(6)
        if choice == 0:  # User chose "Play/Test Game"
            selected_character, region = select_character_menu()
            if selected_character:
                from game import gameplay  # Import gameplay here to avoid circular imports
                gameplay(selected_character, region)  # Start gameplay
        elif choice == 1:  # User chose "Show World"
            from create import all_regions
            display_world(all_regions)
        elif choice == 5:  # User chose "Exit"
            print("Exiting game...")
            break  # Exit the loop and end the program
        else:
            print("Invalid selection. Please try again.")

def get_menu_choice(options):
    for key, (description, _) in options.items():
        print(f"{key}: {description}")
    choice = input("Choose an option: ")
    print("\n")
    return choice if choice in options else None  # value[1] is the return value


def get_user_choice(max_choice: int) -> int:
    """Gets user input for menu selection safely."""
    try:
        choice = int(input("Enterx your choice: ")) - 1
        if 0 <= choice < max_choice:
            return choice
        print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return None

from character_creation_funcs import player_character_options, instantiate_character
from display import show_character_details

#from main import get_all_regions, get_factions
def select_character_menu():
    """Displays the character selection menu, instantiates the chosen character, and returns it."""

    # Get character options
    all_regions = get_all_regions()
    factions = get_factions()
    character_options = player_character_options(all_regions, factions)

    if not character_options:
        print("No characters available for selection.")
        return None, None

    # Display character choices
    print("\nSelect a character:")
    for idx, char_data in enumerate(character_options, start=1):
        print(f"{idx}. {char_data['name']}, {char_data['class'].__name__}")

    # Get user's choice
    while True:
        try:
            choice = int(input("Enter the number of your chosen character: ")) - 1
            if 0 <= choice < len(character_options):
                selected_data = character_options[choice]
                selected_character = instantiate_character(selected_data, all_regions, factions)
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Show selected character details
    show_character_details(selected_character)
    print("show_character_details(selected_character) has been called.")

    return selected_character, selected_character.region



#is this still used?
def display_character_summary(characters):
    """Displays all characters using the show_character_details function."""
    print("\n=== CHARACTER SUMMARY ===\n")
    from display import show_character_details, display_filtered_character_summary #either or?
    for char in characters:
        display_filtered_character_summary(char)
