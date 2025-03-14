#menu_utils.py
from tabulate import tabulate
from display import display_world
from typing import Dict, Any
from create_game_state import get_game_state

# Ensure game_state is initialized correctly before use
game_state = get_game_state()
    

def main_menu(all_locations):
    global game_state
    game_state = get_game_state()

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
                print(f"DEBUG: in menu_utils line 27 character.region type = {type(region)}, value = {region}")
                gameplay(selected_character, region, game_state.all_characters, game_state.all_regions, all_locations)  # Start gameplay

        elif choice == 1:  # User chose "Show World"
            from create import all_regions
            display_world(all_regions)
        elif choice == 5:  # User chose "Exit"
            print("Exiting game...")
            break  # Exit the loop and end the program
        else:
            print("Invalid selection. Please try again.")

def get_menu_choice(options, filter_func=None):
    """Displays a menu and returns the chosen option, filtering actions if needed."""
    if filter_func:
        options = {k: v for k, v in options.items() if filter_func(v)}

    if not options:
        print("No available actions.")
        return None

    for key, (desc, _) in options.items():
        print(f"{key}: {desc}")

    choice = input("Choose an option: ")
    return choice if choice in options else None

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
    from create_game_state import game_state

    all_regions = game_state.all_regions
    factions = game_state.factions
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
    #print("show_character_details(selected_character) has been called.")

    return selected_character, selected_character.region

def location_menu(character, region, location):
    """Menu for interacting with a location."""
    from characterActions import talk_to_character, exit_location
    from display import show_shop_inventory, display_employees

    while True:
        options = {
            "1": ("Talk to Character", talk_to_character),
            "2": ("View Shop Inventory", show_shop_inventory),
            "3": ("View Employees", display_employees),
            "4": ("Leave Location", exit_location)
        }

        choice = get_menu_choice(options)

        if choice:
            action_name, action_function = options[choice]
            
            if action_name == "Leave Location":
                print(f"{character.name} leaves {location.name}.")
                #update character.location AND game_state
                break  # Exits the loop, returning to region

            if action_function:
                action_function(location)

            

