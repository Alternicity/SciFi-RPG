#main.py
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from menu_utils import main_menu
from display import show_locations_in_region, show_character_details, show_shop_inventory
from game import game
from create_game_state import get_game_state

game_state = None
def setup_game():
    global game_state, factions, all_regions
    #The global declaration in setup_game() only affects the function where it is declared.

    #print("DEBUG: setup_game() is running!")
    #print(f"📌📌📌 DEBUG: from setup_game all_regions = {all_regions}")
    
    game_state = get_game_state()  # Assign the result to game_state
    #print(f"DEBUG: game_state AFTER  get_game_state() = {game_state}")

    from create import create_regions, create_factions
    from createLocations import create_locations

    all_regions = create_regions()
    #print(f"📌 DEBUG: After create_regions(), game_state.all_regions = {game_state.all_regions}")  
    
    # Set up the game_state variables
    game_state.all_regions = all_regions
    #print(f"DEBUG: After create_regions(), game_state.all_regions = {[r.name for r in game_state.all_regions]}")

    if not all_regions:  # Check if no regions were created
        print("ERROR: No regions were created!")
        return
    
    from base_classes import Location
    all_locations = [loc for region in all_regions for loc in region.locations if isinstance(loc, Location)]
    #print(f"🟢 DEBUG: First item in all_locations after flattening: {all_locations[0]} (Type: {type(all_locations[0])})")

    game_state.all_locations = all_locations
    #print(f"📌 DEBUG: game_state.all_locations = {game_state.all_locations}") #verbose

    from display import compare_locations
    compare_locations(all_locations, all_regions)


    factions, all_characters = create_factions(all_regions, all_locations)
    game_state.factions = factions
    game_state.all_characters = all_characters
    
    print(f"Game setup complete. Total characters: {len(game_state.all_characters)}")
    # Verify that game_state is still set after modifying it  
    #1print(f"🛠️ DEBUG: 🔴🔵From setup_game final game_state check before main_menu() = {game_state}")

    #print(f"✅ DEBUG: game_state after setup = {game_state}")
    #print(f"✅ DEBUG: game_state.all_characters = {getattr(game_state, 'all_characters', 'MISSING')}")

    return all_regions, factions, all_characters, all_locations

def main(all_locations):
    setup_game()
    main_menu(all_locations)
    game()

def get_all_regions():
    global all_regions
    return all_regions

def get_factions():
    global factions
    return factions


if __name__ == "__main__":
    all_locations = setup_game()
    main(all_locations)