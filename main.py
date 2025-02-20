#main.py
import logging
#ALL files use this to get the project root

from gameplay import gameplay
from create import create_regions, create_factions, create_characters, create_locations, all_regions
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from menu_utils import main_menu
from display import show_locations_in_region, select_region_menu, show_character_details, show_shop_inventory
from loader import load_region_data
from characters import (Boss, Captain, Employee, VIP, RiotCop, CorporateAssasin, Employee, GangMember,
                        CEO, Manager, CorporateSecurity, Civilian)

from character_creation_funcs import player_character_options

def setup_game():
    """Initialize game world with existing regions, then create factions and characters."""
    all_locations = [create_locations(region.name, region.wealth) for region in all_regions]
    factions, all_characters = create_factions(all_locations)  # Pass locations correctly

    return all_regions, factions, all_characters

def main():

    main_menu()
    
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