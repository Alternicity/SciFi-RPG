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
from motivation_presets import MotivationPresets
from status import FactionStatus, StatusLevel, CharacterStatus
from base_classes import Character

def create_faction_characters(faction, all_regions, factions=None):
    from faction import Gang, Corporation, State
    if isinstance(faction, Gang):
        return create_gang_characters(faction)
    elif isinstance(faction, Corporation):
        return create_corporation_characters(faction, factions)
    elif isinstance(faction, State):
        return create_TheState_characters(faction)
    elif faction.name == "Factionless":
        # Skip creating characters for factionless, its just to make code run for independent characters
        return []
    else:
        raise ValueError(f"Unknown faction type: {faction}")

def create_all_characters(factions, all_locations, all_regions):
    # TODO: Update NPC instantiation to support Inventory objects
    print("\n" * 3)  # Line breaks for clarity
    print("Creating characters for factions...")
    print(f"Received {len(factions)} factions")

    all_characters = []
   
    for faction in factions:
        faction_characters = create_faction_characters(faction, all_regions, factions)
        all_characters.extend(faction_characters)

    from createCivilians import create_civilian_population, assign_workplaces

    civilians = create_civilian_population(all_locations, all_regions)
    assign_workplaces(civilians, all_locations)
    all_characters.extend(civilians)
    
    from game_logic import assign_random_civilians_to_random_shops
    assign_random_civilians_to_random_shops(all_regions)  # Now regions are ready
    
    print(f"Total characters created: {len(all_characters)}")
    return all_characters

def player_character_options(all_regions, factions):
    """Return a list of dictionaries with character DATA instead of full objects."""
    # Define character options as data dictionaries
    from InWorldObjects import Wallet
    from weapons import Knife
    from inventory import Inventory
    from base_classes import Factionless #foes this need adding to factions and game_state
    
    character_data = [
    {
        "class": Manager,
        "name": "Karen",
        "sex": "female",
        "race": "Terran",
        "faction_name": "Hannival",
        "region_name": "Downtown",
        "location_name": "Hannival HQ",
        "wallet": Wallet(bankCardCash=500),
        "preferred_actions": {},
        "initial_motivations": MotivationPresets.for_class("Manager"),  # new
        "status_data": {
            "corporate": {"level": StatusLevel.MID, "title": "Manager"},
            "public": {"level": StatusLevel.LOW, "title": "Suit"}
    },
    },

    {
        "class": GangMember,
        "name": "Swiz",
        "sex": "male",
        "race": "French",
        "faction_name": "Factionless",
        "region_name": "Easternhole",
        "location_name": "None",
        "inventory": Inventory([Knife(owner_name="Swiz")]),
        "wallet": Wallet(bankCardCash=50),
        "preferred_actions": {"Rob": 1, "Steal": 2},
        "initial_motivations": MotivationPresets.for_class("GangMember"),
        "custom_skills": {"stealth": 12, "observation": 6},
        "primary_status_domain": "criminal",
        "status_data": {
            "public": {"level": StatusLevel.LOW, "title": "Unknown"},
            "criminal": {"level": StatusLevel.LOW, "title": "Alone"}
    },
},
]   

    return character_data
    
def instantiate_character(char_data, all_regions, factions):
    from utils import get_faction_by_name, get_region_by_name, get_location_by_name
    from create_game_state import get_game_state
    from InWorldObjects import Wallet
    from weapons import Weapon

    print(f"\n[DEBUG] Instantiating character: {char_data.get('name')}")

    game_state = get_game_state()    
    if game_state is None:
        print("❌ ERROR: game_state is not initialized!")
        return None

    # Extract names from data
    faction_name = char_data.get("faction_name")
    region_name = char_data.get("region_name")
    location_name = char_data.get("location_name")

    print(f"[DEBUG] faction_name: {faction_name}, region_name: {region_name}, location_name: {location_name}")

    # Lookups
    if faction_name is None or faction_name == "Factionless":
        # Find the Factionless instance by name
        faction = next((f for f in factions if f.name == "Factionless"), None)
    else:
        faction = get_faction_by_name(faction_name, factions)

        if faction is None and faction_name != "Factionless":
            print(f"[Warning] No faction found with name: {faction_name}")
            return None

        if faction is None:
            print(f"❌ ERROR: Faction '{faction_name}' not found in factions list!")
        else:
            print(f"[DEBUG] Faction found: {faction.name}")

    region = get_region_by_name(region_name, all_regions)
    #tmp block below
    if region is None:
        print(f"❌ ERROR: Region '{region_name}' not found!")
    else:
        print(f"[DEBUG] Region found: {region.name}")


    location = get_location_by_name(location_name, all_regions)
    #tmp block below
    if location is None:
        print(f"❌ ERROR: Location '{location_name}' not found!")
    else:
        print(f"[DEBUG] Location found: {location.name}")


    wallet = char_data.get("wallet", Wallet())
    race = char_data["race"]
    sex = char_data["sex"]

    if region is None:
        print(f"❌ ERROR: No region found with name '{region_name}'")

    motivation_objects = char_data.get("initial_motivations", [])

    # Build status if data is provided
    status = None
    if "status_data" in char_data:
        status = CharacterStatus()
        for domain, status_info in char_data["status_data"].items():
            status.set_status(
                domain,
                FactionStatus(level=status_info["level"], title=status_info["title"])
            )

    # Create character
    character = char_data["class"](
    name=char_data["name"],
    race=race,
    sex=sex,
    faction=faction,
    region=region,
    location=location,
    wallet=wallet,
    fun=1,
    hunger=3,
    preferred_actions=char_data.get("preferred_actions", {}),
    initial_motivations=motivation_objects,  # pass weighted tuples
    custom_skills=char_data.get("custom_skills"),
    status=status
)

    # ✅ Set primary status domain
    character.primary_status_domain = char_data.get("primary_status_domain", "public")
    #maybe move the above block up into instantiator above it.


# Assign inventory if provided
    if "inventory" in char_data:
        character.inventory = char_data["inventory"]
        character.inventory.owner = character  # Set the owner reference

        # Update each item to be aware of its new owner
        for item in character.inventory.items.values():
            item.owner_name = character.name
            if isinstance(item, Weapon):
                character.weapons.append(item)

        character.inventory.update_primary_weapon()
        #print(f"Post-instantiation inventory for {character.name}:")
        for item in character.inventory.items.values():
            print(f"  - {item.name} x{getattr(item, 'quantity', 1)}")

        print(f"{character.name} starts with motivations: {', '.join([m.type for m in character.motivation_manager.motivations])}")

        game_state.player_character = character
        print(f"[SUCCESS] Character '{character.name}' instantiated successfully.")
    return character

    