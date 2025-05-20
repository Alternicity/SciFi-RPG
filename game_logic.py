# gameplay.py
from region_utils import get_all_regions
#remove all object creation from this file and dont let it back in
import random
from menu_utils import get_menu_choice, build_gameplay_menu, GameplayMenu
from characterActions import visit_location
from display import (
    show_character_details,
    display_selected_character_current_region,
    display_filtered_character_summary, display_character_Summary, display_civilians, display_corporations, display_employees, display_gangs, display_character_whereabouts, display_state
)
from motivation import MotivationManager

from character_creation_funcs import create_faction_characters
from utils import dev_mode
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

    #tmp
    from location import Location
    if isinstance(character.region, str):
        print(f"[ERROR] {character.name} has region set as a string: {character.region}")
    if isinstance(character.location, Location) and isinstance(character.location.region, str):
        print(f"[ERROR] {character.name} has location.region set as a string: {character.location.region}")


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
    2: ("Move to another Region", lambda: move_region(character, show_region_choices(game_state.all_regions), game_state.all_regions)),
    3: ("Display Characters Summary", lambda: display_character_Summary()),
    4: ("Display Factions", lambda: display_factions()),
    5: ("Dev", lambda: dev_mode()),  # ✅ Simple call to dev_mode
    6: ("Exit Gameplay", lambda: exit_gameplay()),
}
        dynamic_options = build_gameplay_menu(selected_character.location, selected_character)

        if not isinstance(dynamic_options, dict):
            print("Error: dynamic_options is not a dictionary!", type(dynamic_options))
            dynamic_options = {}  # Prevent crashes

        # Merge static and dynamic menu options
        options = {**static_options, **dynamic_options}  # Ensure dictionary format
        choice = get_menu_choice(options)

        #print(f"Debug: static_options before merging: {static_options}")
        #print(f"Debug: dynamic_options before merging: {dynamic_options}")
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

    # Move character to new region
    character.region = region_obj  
    character.location = None  # Clear location since they moved

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

def assign_random_civilians_to_random_shops(regions, count: int = 15):
    #print("[Debug] assign_random_civilians_to_random_shops() was called.")
    from location import Shop
    from characters import Civilian
    all_civilians = []
    all_shops = []

    for region in regions:
        #print(f"[Debug] Checking region: {region.name}")
        pass
        for loc in region.locations:
            #print(f"    [Debug] Found location: {loc.name} ({type(loc).__name__})")
            pass
            if isinstance(loc, Shop):
                #print(f"        [Debug] --> This is a Shop.")
                all_shops.append(loc)
            for char in loc.characters_there:
                #print(f"        [Debug] Has character: {char.name} ({type(char).__name__})")
                if isinstance(char, Civilian):
                    #print(f"            [Debug] --> This is a Civilian.")
                    all_civilians.append((char, loc))  # track original location too
    print(f"Total Civilians found: {len(all_civilians)}")
    print(f"Total Shops found: {len(all_shops)}")

    if not all_civilians or not all_shops:
        print("No civilians or shops available to assign.")
        return

    random.shuffle(all_civilians)
    civilians_to_assign = all_civilians[:count]

    for (civilian, original_location) in civilians_to_assign:
        shop = random.choice(all_shops)

        # Remove from current location
        if civilian in original_location.characters_there:
            original_location.characters_there.remove(civilian)

        # Assign to shop
        shop.characters_there.append(civilian)
        civilian.location = shop

        #print(f"[Test] Moved {civilian.name} to shop: {shop.name}")



def display_factions():
    print(f"display_factions called")

def dev_mode():
    print(f"dev_mode called")

def exit_gameplay(character, region):
    """Exits the gameplay loop."""
    print("\nExiting gameplay.")
    exit()


