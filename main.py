# main.py

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from menu_utils import main_menu
from game import game
from create_game_state import get_game_state

# Only define these globals once
game_state = None
all_regions = None
factions = None

def setup_game():
    global game_state, factions, all_regions

    game_state = get_game_state()  # Singleton pattern
    from create import create_regions, create_factions
    from createLocations import create_locations
    from base_classes import Location
    from display import compare_locations

    all_regions = create_regions()
    game_state.all_regions = all_regions

    if not all_regions:
        print("ERROR: No regions were created!")
        return

    all_locations = [loc for region in all_regions for loc in region.locations if isinstance(loc, Location)]
    game_state.all_locations = all_locations

    compare_locations(all_locations, all_regions)

    factions, all_characters = create_factions(all_regions, all_locations)
    game_state.factions = factions
    game_state.all_characters = all_characters

    print(f"Game setup complete. Total characters: {len(game_state.all_characters)}")


    return all_regions, factions, all_characters, all_locations

def main():
    all_regions, factions, all_characters, all_locations = setup_game()
    main_menu(all_locations, all_characters)
    game()

def get_all_regions():
    global all_regions
    return all_regions

def get_factions():
    global factions
    return factions

if __name__ == "__main__":
    main()
