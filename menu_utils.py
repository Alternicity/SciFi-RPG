#menu_utils.py
from tabulate import tabulate
from display import display_world
from typing import Dict, Any


try:
    from create import initialize_regions
    print("initialize_regions successfully imported.")
except ImportError as e:
    print(f"Failed to import initialize_regions: {e}")

    
def main_menu():
    """Display the main menu and return the user choice. Not a gameplay menu itself"""
    print("\n=== Main Menu ===")
    print("1: Play/Test Game")
    print("2: Show world")
    print("6: Exit")

    choice = get_user_choice(1)
    select_character_menu()

    choice = get_user_choice(2)
    from menu_utils import all_regions
    display_world(all_regions)

    choice = get_user_choice(6)
    return choice

def get_menu_choice(options: Dict[str, Any]) -> Any:
    """Generic function to handle menu selection."""
    for key, value in options.items():
        print(f"{key}. {value[0]}")  # value[0] is the display name
    
    choice = input("> ")
    return options.get(choice, [None])[1]  # value[1] is the return value


def get_user_choice(max_choice: int) -> int:
    """Gets user input for menu selection safely."""
    try:
        choice = int(input("Enter your choice: ")) - 1
        if 0 <= choice < max_choice:
            return choice
        print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return None

def select_character_menu():
    """Displays character selection and returns the selected character."""
    from character_creation_funcs import player_character_options
    from display import show_character_details
    from create import all_regions, factions
    
  
    playable_characters = player_character_options(all_regions, factions)  # Get list of playable characters
    

    if not playable_characters:
        print("No characters available for selection.")
        return None

    # Display available characters
    print("\nSelect a character:")
    for idx, character in enumerate(playable_characters, start=1):
        print(f"{idx}. {character.name} {character.faction.name} {character.faction.type.capitalize()}")


    # Get player's choice
    while True:
        try:
            choice = int(input("Enter the number of your chosen character: ")) - 1
            if 0 <= choice < len(playable_characters):
                selected_character = playable_characters[choice]
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

        #all_characters.append(selected_character) add the plazers character to the list of all characters?
        #Decide whether all_characters should store the player character.

    # Show character details
    show_character_details(selected_character)
    return selected_character

#is this still used?
def display_character_summary(characters):
    """Displays all characters using the show_character_details function."""
    print("\n=== CHARACTER SUMMARY ===\n")
    from display import show_character_details, display_filtered_character_summary #either or?
    for char in characters:
        display_filtered_character_summary(char)
