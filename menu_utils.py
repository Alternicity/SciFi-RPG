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
    def __init__(self):# the static  menu options
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
    available_options = {}

    if location is None:
        print(f"In transit; {character.name} is in {character.region} but no specific location")
        return available_options  # Return empty dict instead of list

    option_list = []  # Collect options before converting to dict

    print(f"Debug: Checking available options for {location.name}.")

    # Location-based actions
    if hasattr(location, "employees_there"):
        print(f"Debug: {location.name} has employees_there: {location.employees_there}")
    if hasattr(location, "characters_there"):
        print(f"Debug: {location.name} has characters_there: {location.characters_there}")

    if hasattr(location, "employees_there") and location.employees_there:
        option_list.append(("Display Employees", lambda: display_employees(location)))
        print(f"Debug: Employees present at {location.name}, adding 'Display Employees' option.")

    if hasattr(location, "characters_there") and location.characters_there:
        option_list.append(("Talk to a Character", lambda: talk_to_character(location, character)))
        print(f"Debug: Characters present at {location.name}, adding 'Talk to a Character' option.")


    # Character-based actions
    print(f"Debug: {character.name} preferred actions: {character.get_preferred_actions()}")

    if hasattr(location, "has_stealable_items") and location.has_stealable_items():
        option_list.append(("Steal an Item", lambda: steal(character, location, location.get_random_stealable_item())))
        print(f"Debug: {character.name} can steal at {location.name}, adding 'Steal' option.")

    if hasattr(location, "robbable") and location.robbable():
        option_list.append(("Rob the Place", lambda: rob(character, location)))
        print(f"Debug: {character.name} can rob {location.name}, adding 'Rob' option.")

    if hasattr(location, "menu_options"):
        print(f"Debug: {location.name} has menu_options: {location.menu_options}")

    # Include predefined `menu_options` in `Shop`
    if hasattr(location, "menu_options") and isinstance(location.menu_options, list):
        for action_name in location.menu_options:
            option_list.append((action_name, lambda: print(f"Selected action: {action_name}")))
            print(f"Debug: Added '{action_name}' from menu_options.")

    # Convert the list to a dictionary
    available_options = {idx + 1: (desc, func) for idx, (desc, func) in enumerate(option_list)}

    print(f"Debug: Final available options for {location.name}: {available_options}")

    return available_options  # Now always a dictionary

def build_gameplay_menu(location, character):
    """Combines location-based options with general gameplay menu."""
    location = character.location  # Get location from character
    region = character.region
    
    options = get_available_options(location, character)

    if not isinstance(options, dict):
        print(f"Error: get_available_options did not return a dictionary! Type: {type(options)}")
    options = {}  # Ensure it doesn't crash

    # Ensure options is in the correct format
    options = {idx: (desc, func) for idx, (desc, func) in options.items()} 
    

    print(f"Debug: In build_gameplay_menu: Options type before returning: {type(options)}, value: {options}")

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


        if not choice:  # Handle empty input
            print("Error: No input detected! Please enter a number.from get_menu_choice")
            continue

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
    """Gets user input for main menu selection safely."""
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



def location_menu(character, location):#deprecated?
    """Menu for interacting with a location dynamically."""
    while True:
        available_options = get_available_options(character, location)
        print(f"Debug: location_menu() - get_available_options() returned {type(available_options)}, {available_options}")
        
        #here associate the menu_options from the location with appropriate functions
        
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


def display_menu(options: dict):
    """Displays a dynamic menu and returns the chosen action."""
    if not options:
        print("No available options.")
        return None
    
    while True:
        print("\nAvailable options:")
        for key, (desc, _) in options.items():
            print(f"{key}: {desc}")
    
    
        choice = input("Choose an option: ").strip()
        print(f"Debug: User entered {repr(choice)}")  # Debugging line

        if choice.isdigit():
            choice = int(choice)
            if choice in options:
                return choice  # Return valid selection

        print("Invalid choice. Try again.")
        


        return choice  # Ensure input is returned

def select_item_for_purchase(shop):
    """Let the player choose an item to buy."""
    if not shop.inventory.items:  # Ensure inventory exists and has items
        print("The shop is empty.")
        return None

    shop.show_inventory()  # This should print the inventory

    # Allow player to select an item
    item_name = input("Enter the name of the item you want to buy: ").strip()
    return item_name if item_name else None  # Return the item name if provided

    print("Available items:")
    item_options = {str(i+1): item for i, item in enumerate(shop.inventory)}

    choice = get_menu_choice(item_options)
    return item_options.get(choice)
