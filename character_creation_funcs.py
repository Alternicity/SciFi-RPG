#character_creation_funcs.py
import logging
import random
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, GangMember, Child, Influencer,
                           Babe, Detective, Accountant, Taxman)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from utils import get_faction_by_name, get_location_by_name, get_region_by_name
from createGangCharacters import create_gang_characters
from createCorporateCharacters import create_corporation_characters
from create_TheState_characters import create_TheState_characters


def create_faction_characters(faction, all_regions, factions=None):
    # Choose a dominant race for the faction
    from faction import Gang, Corporation, State
    if isinstance(faction, Gang):
        return create_gang_characters(faction)
    elif isinstance(faction, Corporation):
        return create_corporation_characters(faction, factions)
    elif isinstance(faction, State):
        return create_TheState_characters(faction)
    else:
        raise ValueError(f"Unknown faction type: {faction}")

def create_all_characters(factions, all_locations, all_regions):
    # TODO: Update NPC instantiation to support Wallet and Inventory objects
    print("\n" * 3)  # Line breaks for clarity
    print("create_all_characters() is about to run")

    import inspect
    print(f"create_all_characters() called from: {inspect.stack()[1].function}")

    all_characters = []
   
    for faction in factions:
        faction_characters = create_faction_characters(faction, all_regions, factions)
        all_characters.extend(faction_characters)

    from createCivilians import create_civilian_population, assign_workplaces

    civilians = create_civilian_population(all_locations, all_regions)
    assign_workplaces(civilians, all_locations)
    all_characters.extend(civilians)

    return all_characters

#marked for deletion
""" def player_character_options(all_regions, factions) -> list:
    #duplicate to either delete or rename. Is this code used?
    print("Checking available regions and factions...")
    # Ensure we get a valid Corporation
    from faction import Corporation, Gang

    available_corporations = [faction for faction in factions if isinstance(faction, Corporation)]
    if not available_corporations:
        raise ValueError("No corporation factions available!")

    available_gangs = [faction for faction in factions if isinstance(faction, Gang)]
    if not available_gangs:
        raise ValueError("No corporation factions available!")
    
    selected_faction = random.choice(available_corporations)  # Pick one at random """

from base_classes import Character
def select_character_menu():
    """Displays character selection and returns the selected character and their region."""
    from character_creation_funcs import player_character_options
    from display import show_character_details
    from create import all_regions, factions
    from base_classes import Character
    character_options = player_character_options(all_regions, factions)

    if not character_options:
        print("No characters available for selection.")
        return None, None

    # Display character choices
    print("\nSelect a character:")
    for idx, char_data in enumerate(character_options, start=1):
        print(f"{idx}. {char_data['name']} {char_data['Class'].name}")

    # Player selects a character
    while True:
        try:
            choice = int(input("Enter the number of your chosen character: ")) - 1
            if 0 <= choice < len(character_options):
                char_data = character_options[choice]
                selected_character = Character(
                    name=char_data["name"],
                    #their class name
                )
                selected_character.is_player = True
                global current_character  # Declare global to use it in other modules
                current_character = selected_character

                #I had to add this line to make it be defined:
                character = selected_character
                print(f"🔴🔴DEBUG: {character.name} location.name = {character.location.name}")
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Show character details
    show_character_details(selected_character)

    return selected_character, selected_character.region


def player_character_options(all_regions, factions):
    """Return a list of dictionaries with character DATA instead of full objects."""
    # Define character options as data dictionaries
    from InWorldObjects import Wallet
    character_data = [
    {
        "class": Manager,
        "name": "Karen",
        "faction_name": "Hannival",
        "region_name": "Downtown",
        "location_name": "Corporate HQ",
        "wallet": Wallet(bankCardCash=500),
        "preferred_actions": {}
    },
    {
        "class": GangMember,
        "name": "Swiz",
        "faction_name": "The Black Fangs",
        "region_name": "Easternhole",
        "location_name": "Stash",
        "wallet": Wallet(bankCardCash=50),
        "preferred_actions": {"Rob": 1, "Steal": 2}
    }
]

    return character_data
    
def instantiate_character(char_data, all_regions, factions):
    from utils import get_faction_by_name, get_region_by_name, get_location_by_name
    from create_game_state import get_game_state
    from InWorldObjects import Wallet

    game_state = get_game_state()    
    if game_state is None:
        print("ERROR: game_state is not initialized!")

    # Extract names from data
    faction_name = char_data.get("faction_name")
    region_name = char_data.get("region_name")
    location_name = char_data.get("location_name")

    # Lookups
    faction = get_faction_by_name(faction_name, factions)
    region = get_region_by_name(region_name, all_regions)
    location = get_location_by_name(location_name, all_regions)
    wallet = char_data.get("wallet", Wallet())

    if faction is None:
        print(f"❌ ERROR: No faction found with name '{faction_name}'")
    if region is None:
        print(f"❌ ERROR: No region found with name '{region_name}'")
    """ if location is None:
        print(f"⚠️ Warning: Could not find location '{location_name}' for {char_data['name']}. Defaulting to region center.")
        location = region.locations[0] if region and region.locations else None """
        #this Warning shows up in program output.
        #return to examine this, is it still coming from get_location_by_name, and thus game_state?


    # Create character
    character = char_data["class"](
        name=char_data["name"],
        faction=faction,
        region=region,
        location=location,
        wallet=wallet,
        fun=1,
        hunger=3,
        preferred_actions=char_data.get("preferred_actions", {})
    )

    game_state.player_character = character
    return character


    