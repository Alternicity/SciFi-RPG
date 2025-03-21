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
                gameplay(selected_character, region)  # Start gameplay

        elif choice == 1:  # User chose "Show World"
            from create import all_regions
            display_world(all_regions)
        elif choice == 5:  # User chose "Exit"
            print("Exiting game...")
            break  # Exit the loop and end the program
        else:
            print("Invalid selection. Please try again.")

from characterActions import talk_to_character, steal, rob, buy
from location import Shop
from display import display_employees
from typing import List

class GameplayMenu:
    def __init__(self):
        self.menu_options: List[str] = [
            "Visit Location",
            "Move to another Region",
            "Display Characters Summary",
            "Display Factions",  # New consolidated option
            "Dev",
            "Exit Gameplay",  # Always last
        ]

    def get_options(self):
        """Convert menu_options to the format required"""
        return self.menu_options


def get_available_options(location, character):
    """Determine available menu options based on character and location."""
    available_options = []

    if location is None:
        print(f"In transit; {character.name} is in {character.region} but no specific location")
        return {}  # Return empty dict instead of list

    # Location-based actions
    if hasattr(location, "employees_there") and location.employees_there:
        available_options.append(("Display Employees", lambda: display_employees(location)))

    if location.characters_there:
        available_options.append(("Talk to a Character", lambda: talk_to_character(location, character)))
    #Character based actions
    if "Steal" in character.get_preferred_actions() and location.has_stealable_items():
        available_options.append(("Steal an Item", lambda: steal(character, location, location.get_random_stealable_item())))

    if "Rob" in character.get_preferred_actions() and location.robbable():
        available_options.append(("Rob the Place", lambda: rob(character, location)))

    if "Buy" in character.get_preferred_actions() and isinstance(location, Shop):
        available_options.append(("Buy an Item", lambda: character.buy(select_item_for_purchase(location))))

    return dict(enumerate(available_options, start=1))

def build_gameplay_menu(location, character):
    """Combines location-based options with general gameplay menu."""
    options = get_available_options(location, character)

    # Get general gameplay menu options
    gameplay_options = options.copy()  # Make a copy instead of calling function again 
    #both options and gameplay_options are needed

    for idx, option in enumerate(gameplay_options, start=len(options) + 1):
        options[idx] = (option, None)  # No function mapping for now
        
    return options 


def get_menu_choice(options, filter_func=None):
    """Displays a menu and returns the chosen option, filtering actions if needed."""
    if filter_func:
        options = {k: v for k, v in options.items() if filter_func(v)}

    if not options:
        print("No available options.")
        return None

    print("\nAvailable actions:")
    for key, (desc, action) in options.items(): #line 109
        print(f"{key}: {desc}")

    while True:
        choice = input("Choose an option: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if choice in options:
                desc, action = options[choice]
                print(f"You selected: {desc}")
                if action:
                    action()  # Call the associated function
                return desc
            else:
                print("Invalid choice. Try again.")
        else:
            print("Please enter a number.")


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

def location_menu(character, location):
    """Menu for interacting with a location dynamically."""
    while True:
        available_options = get_available_options(character, location)
        
        if not available_options:
            print("No actions available here.")
            return
        
        # Show menu dynamically
        print("\nAvailable actions:")
        for index, (desc, _) in enumerate(available_options, start=1):
            print(f"{index}: {desc}")

        choice = input("Choose an option: ").strip()
        
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(available_options):
                _, action_func = available_options[choice_index]
                action_func()
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

        if location.is_workplace:  # Example condition to exit after an action
            break


def display_menu(options):
    """Displays a dynamic menu and returns the chosen action."""
    for key, (desc, _) in options.items():
        print(f"{key}: {desc}")
    
    choice = input("> ")
    return choice if choice in options else None

def select_item_for_purchase(shop):
    """Let the player choose an item to buy."""
    if not shop.inventory:
        print("The shop is empty.")
        return None

    print("Available items:")
    item_options = {str(i+1): item for i, item in enumerate(shop.inventory)}

    choice = get_menu_choice(item_options)
    return item_options.get(choice)
