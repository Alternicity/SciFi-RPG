# gameplay.py
from region_utils import get_all_regions
#remove all object creation from this file and dont let it back in
from menu_utils import get_menu_choice
from characterActions import visit_location
from display import (
    show_character_details,
    display_selected_character_current_region,
    display_filtered_character_summary,
    display_civilians, display_corporations, display_employees, display_gangs, display_character_whereabouts, display_state
)
from motivation import MotivationManager
from character_creation_funcs import generate_faction_characters

from create_game_state import get_game_state

def gameplay(character, region, characters, all_regions, all_locations):
    game_state = get_game_state()  # Ensure single instance of game_state
    
    
    
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

    

    # Main Gameplay Loop
    while True:
        print("\n=== Gameplay Menu ===")
        #print("DEBUG: All locations after setup, in gameplay:", game_state.all_locations)

        #from display import display_character_whereabouts
        display_character_whereabouts(character)  # Ensure proper whereabouts are shown
        from display import display_state, display_gangs, display_employees
        from create_game_state import game_state
        options = {
        "1": ("Visit Location", visit_location),
        "2": ("Move to another Region", move_region),
        "3": ("Display Characters Summary", view_characters),
        "4": ("Exit Gameplay", exit_gameplay),
        "5": ("View Characters Summarized", display_civilians),
        "6": ("Display Employees", display_employees),
        "8": ("Display Corporations", display_corporations),
        "9": ("Display Gangs", display_gangs),
        "10": ("Display State", display_state),
    }

        # Get user choice
        choice = get_menu_choice(options)

        if choice:  # If the choice is valid
            action_name, action_function = options[choice]  # Unpack the tuple
            if action_name == "Visit Location":
                # Convert list of locations to a dictionary for menu selection
                location_options = {str(i+1): (loc.name, loc) for i, loc in enumerate(region.locations)}

                # Ask player to select a location
                location_choice = get_menu_choice(location_options)

                if location_choice in location_options:
                    location = location_options[location_choice][1]
                    action_function(character, region, location)
                else:
                    print("Invalid location choice.")
            elif action_name == "Display State":
                if game_state.state:
                    display_state(game_state.state)
                else:
                    print("State data is not yet initialized.")

            elif action_name == "Display Gangs":
                display_gangs(game_state)

            
            elif action_name == "View Characters Summarized":
                pass
                #display_civilians(civilians)
                #might need to split civilian and emplozee creation for this.


            elif action_name == "Display Employees":  # Use action_name instead of choice
                print("DEBUG: Entering display_employees()")
                display_employees(character.location, all_locations)

            elif action_name == "Display Character Summary":
                view_characters(game_state.all_characters, region)
                
                
            elif action_name == "Move to another Region":
                from display import select_region_menu  # Ensure we have the menu function

                selected_region = select_region_menu(all_regions)  # Let the player choose
                if selected_region:
                    move_region(character, selected_region, all_regions)

            

            gameplay(character, character.region, game_state.all_characters, all_locations, all_regions)  # Ensure we return here

def move_region(character, selected_region, all_regions):
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
    print(f"DEBUG: BEFORE moving - character.region ID = {id(character.region)}, value = {character.region}")
    print(f"DEBUG: Moving to region ID = {id(region_obj)}, value = {region_obj}")

    # Move character to new region
    character.region = region_obj  
    character.location = None  # Clear location since they moved

    # Debugging info after moving
    print(f"DEBUG: AFTER moving - character.region ID = {id(character.region)}, value = {character.region}")

    print(f"{character.name} has moved to {region_obj.name}.")


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


def view_characters(all_characters, region):
    """Displays filtered character summaries."""
    print(f"DEBUG: From view_characters, type of characters = {type(all_characters)}")  # Check if it's iterable
    from display import display_filtered_character_summary
    if not isinstance(all_characters, list):
        all_characters = [all_characters]  # Wrap single object in a list
    display_filtered_character_summary(all_characters)


def exit_gameplay(character, region):
    """Exits the gameplay loop."""
    print("\nExiting gameplay.")
    exit()


