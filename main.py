#main.py
import logging
#ALL files use this to get the project root

from game_logic import gameplay
from create import create_regions, create_factions, create_characters
from createLocations import create_locations
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from menu_utils import main_menu
from display import show_locations_in_region, select_region_menu, show_character_details, show_shop_inventory
from loader import load_region_data
from characters import (Boss, Captain, Employee, VIP, RiotCop, CorporateAssasin, Employee, GangMember,
                        CEO, Manager, CorporateSecurity, Civilian)
from game import game
from city_vars import game_state
from character_creation_funcs import player_character_options


import os

def setup_game():
    global factions, all_regions
    """Initialize game world with existing regions, then create factions and characters."""
    print("DEBUG: setup_game() is running!")
    all_regions = create_regions() 
    all_locations = [loc for region in all_regions for loc in create_locations(region.name, region.wealth)]
    print("From setup, after all_locations initialiyed, All Regions:", [region.name for region in all_regions])
    factions, all_characters = create_factions(all_regions, all_locations)
    print(f"DEBUG from setup: game_state.all_locations = {[loc.name for loc in game_state.all_locations]}")

    # Set up the game_state variables
    game_state.all_regions = all_regions
    game_state.all_locations = all_locations
    game_state.factions = factions
    game_state.all_characters = all_characters
    #at one point AI said to call setup_game from main
    return all_regions, factions, all_characters

def main():
    setup_game()
    main_menu()
    game()

def get_all_regions():
    global all_regions
    return all_regions

def get_factions():
    global factions
    return factions

def start_gameplay(current_character, region_data): #Is this still used?
    """Manage gameplay flow with character interaction and region data."""
    print("\n=== Gameplay Start ===\n")

    show_character_details(current_character)
    print(f"Current character: {current_character}")

    shops = region_data.get("shops", [])
    #print(f"Region data type: {type(region_data)}")
    #is it an Object? Does this reflect the charcater's current_location var?

    show_locations_in_region(shops) 
    for shop in shops:
        show_shop_inventory(shop)


if __name__ == "__main__":
    main()