# gameplay.py
from region_utils import get_all_regions
#remove all object creation from this file and dont let it back in

from menu_utils import get_menu_choice, build_gameplay_menu, GameplayMenu
from characterActions import visit_location
from display import (
    show_character_details,
    display_selected_character_current_region,
    display_filtered_character_summary, display_character_Summary, display_civilians, display_corporations, display_employees, display_gangs, display_character_whereabouts, display_state
)
from motivation import MotivationManager
from character_creation_funcs import generate_faction_characters

from create_game_state import get_game_state

    
def gameplay(selected_character, region):
    from create_game_state import get_game_state
    game_state = get_game_state()  # Ensure we get the singleton game state
    all_characters = game_state.all_characters  # Access all characters
    
    # Main Gameplay Loop
    gameplay_menu = GameplayMenu()  # Create the menu object
    character =selected_character
    display_selected_character_current_region(character, region)

    # Update motivations before displaying
    character.motivation_manager.update_motivations()

    # Get the most urgent motivations
    urgent_motivations = character.motivation_manager.get_urgent_motivations()

    # Show pressing needs/motivations
    if urgent_motivations:
        motivation_list = ", ".join(urgent_motivations)
        if character.is_player:
            print(f"You feel the urge to: {motivation_list}.")
        else:
            print(f"{character.name} feels the urge to: {motivation_list}.")
    
    while True:
        print("\n=== Gameplay Menu ===")
        
        static_options = {
    1: ("Visit Location", lambda: visit_location(character, region)),
    #2: ("Move to another Region", lambda: show_region_choices(game_state.all_regions)),
    2: ("Move to another Region", lambda: move_region(character, show_region_choices(game_state.all_regions), game_state.all_regions)),

    3: ("Display Characters Summary", lambda: display_character_Summary()),
    4: ("Display Factions", lambda: display_factions()),
    5: ("Dev", lambda: dev_mode()),
    6: ("Exit Gameplay", lambda: exit_gameplay()),
}
        dynamic_options = build_gameplay_menu(selected_character.location, selected_character)

        # Merge static and dynamic menu options
        options = {**static_options, **dynamic_options}  # Ensure dictionary format
        choice = get_menu_choice(options)

        if not choice:
            continue  # Skip invalid input
        
    
def move_region(character, selected_region, all_regions):
    #all_regions is missing here, try using get_all_regions
    """Handles moving a character to another region."""

    if not selected_region:
        print("DEBUG: No region selected, returning to gameplay.")  
        return
    if selected_region == character.region:
        print(f"{character.name} is already in {selected_region.name}.")
        return  

    # Ensure selected_region is a valid instance from game_state
    
    game_state = get_game_state()

    from utils import get_region_by_name
    region_obj = get_region_by_name(selected_region.name, game_state.all_regions)
    if not region_obj:
        print(f"ERROR: Region {selected_region.name} not found in game_state! Keeping current region.")
        return

    # Debugging info before moving
    #print(f"DEBUG: BEFORE moving - character.region ID = {id(character.region)}, value = {character.region}")
    #print(f"DEBUG: Moving to region ID = {id(region_obj)}, value = {region_obj}")

    # Move character to new region
    character.region = region_obj  
    character.location = None  # Clear location since they moved

    # Debugging info after moving
    #print(f"DEBUG: AFTER moving - character.region ID = {id(character.region)}, value = {character.region}")
    #print(f"{character.name} has moved to {region_obj.name}.")


def show_region_choices(all_regions):
        #for the future
        #show regions the character can move to
        #maybe build a map. cannot move to diametrically opposed region without passing through Downtown, ie
        #she cant go directly from north to south region, OR if doing this, a message displays
        #"passing through Downtown (Central) on the way to destinationRegion" Here a Downtown percept or event might be triggered
        for i, region in enumerate(all_regions, 1):
            print(f"{i}. {region.name}")  # Assuming regions have a 'name' attribute

    # Get user choice and return the corresponding region
        choice = input("Choose a region to move to: ")
        try:
            return all_regions[int(choice) - 1]  # Return the selected Region object
        except (ValueError, IndexError):
            print("Invalid choice!")
            #move_region(character, region, game_state.all_regions)),
            return None

from menu_utils import get_menu_choice

def location_actions_options(player, location):
    """Displays available actions at a location and handles player choice."""
    while True:
        print(f"\nYou are at {location.name}: {location.description}\n")

        choice = get_menu_choice(location.get_available_actions())

        if choice is None:
            print("Invalid choice or no available actions.")
            continue

        if choice == "0": #remove
            print("You leave the location.")
            break  # Exit the function

        _, action_func = location.get_available_actions()[choice]
        action_func()  # Execute the selected action


def view_characters(all_characters, region): #this should be moved to display
    """Displays filtered character summaries."""
    print(f"DEBUG: From view_characters, type of characters = {type(all_characters)}")  # Check if it's iterable
    from display import display_filtered_character_summary
    if not isinstance(all_characters, list):
        all_characters = [all_characters]  # Wrap single object in a list
    display_filtered_character_summary(all_characters)

def display_factions():
    print(f"display_factions called")

def dev_mode():
    print(f"dev_mode called")

def exit_gameplay(character, region):
    """Exits the gameplay loop."""
    print("\nExiting gameplay.")
    exit()


