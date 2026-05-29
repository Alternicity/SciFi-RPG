# main.py

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from menu_utils import main_menu
from game import game
from create.create_game_state import get_game_state
from augment.augmentLocations import reassign_shop_names_after_character_creation
from Family import link_family_shops
# Only define these globals once
game_state = None
all_regions = None
factions = None

def setup_game():
    global game_state, factions, all_regions

    game_state = get_game_state()  # Singleton pattern
    from create.create import create_regions, create_factions
    from create.createLocations import create_locations
    from base.location import Location
    from display.display import compare_locations, debug_display_all_shops
    from augment.augment_state import augment_municipal_buildings
    
    all_regions, all_locations = create_regions()
    game_state.all_regions = all_regions

    if not all_regions:
        print("ERROR: No regions were created!")
        return
    
    game_state.all_locations = all_locations

    compare_locations(all_locations, all_regions)
    
    factions, all_characters = create_factions(all_regions, all_locations)
    game_state.factions = factions
    game_state.all_characters = all_characters
    #maybe augment_municipal_buildings call should go here?

    reassign_shop_names_after_character_creation()
    link_family_shops(game_state)
    augment_municipal_buildings()
    debug_display_all_shops(all_regions)
    
    #tmp
    """ from debug_utils import debug_location_init
    for loc in game_state.all_locations:

        if hasattr(loc, "employees_there") or hasattr(loc, "power_component"):
            debug_location_init(loc) """


    print(f"Game setup complete. Total characters: {len(game_state.all_characters)}")

    return all_regions, factions, all_characters, all_locations

def main():
    all_regions, factions, all_characters, all_locations = setup_game()
    from world.scenarios.apply_scenarios import apply_scenarios

    apply_scenarios(all_characters)
    from augment.augment_factions import augment_factions

    augment_factions(factions)#the factions i was suspicious of. Is setup_game returning it? 
    #maybe we should try populating it again from game_state here just to see what happens?
    main_menu(all_locations, all_characters)
    #game()

def get_all_regions():
    global all_regions
    return all_regions

def get_factions():
    global factions
    return factions

if __name__ == "__main__":
    main()

#Linux sometimes strips executable state after edits.