#character_creation_funcs.py
import logging
import random
from characters import (Boss, Captain, Employee, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, Child, Influencer,
                           Babe, Detective, Accountant, Taxman, Adepta)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from utils import get_faction_by_name, get_location_by_name, get_region_by_name
from create.createGangCharacters import create_gang_characters
from create.createCorporateCharacters import create_corporation_characters
from create.create_TheState_characters import create_TheState_characters
from motivation.motivation import MotivationManager, VALID_MOTIVATIONS
from motivation.motivation_presets import MotivationPresets
from motivation.motivation_init import initialize_motivations
from status import FactionStatus, StatusLevel, CharacterStatus
from base.character import Character
from Family import assign_families_and_homes, link_family_shops
from create.create_game_state import get_game_state
from debug_utils import debug_print
from character_components.observation_component import ObservationComponent
from character_components.inventory_component import InventoryComponent
from character_components.self_awareness_component import SelfAwarenessComponent
from character_components.wallet_component import WalletComponent
from character_mind import Mind, Curiosity
from tasks.tasks import TaskManager
from employment.employee import EmployeeProfile
from weapons import Knife
game_state = get_game_state()

def create_faction_characters(faction, all_regions, factions=None):
    from faction import Gang, Corporation, State
    if isinstance(faction, Gang):
        return create_gang_characters(faction, all_regions)
    elif isinstance(faction, Corporation):
        #return create_corporation_characters(faction, factions)
        #uncomment to create corp characters
        
        return []  # corporations intentionally have no characters (yet)
    
    elif isinstance(faction, State):
        return create_TheState_characters(faction)
    elif faction.name == "Factionless":
        # Skip creating characters for factionless
        return []

    # Final fallback catch
    print(f"[WARN] Unknown faction type for: {faction.name} ({type(faction)}) — returning empty list.")
    return []

def create_all_characters(factions, all_locations, all_regions):

    #print("\n" * 3)  # Line breaks for clarity
    print("Creating characters for factions...")
    print(f"Received {len(factions)} factions")
        # Extract all shops from the location list
    from location.locations import Shop
    shops = [loc for loc in all_locations if isinstance(loc, Shop)]

    all_characters = []
   
    for faction in factions:
        faction_characters = create_faction_characters(faction, all_regions, factions)
        if faction_characters:
            all_characters.extend(faction_characters)
        else:
            pass
            #print(f"[ERROR] create_faction_characters() returned None for faction: {faction.name}")
            #uncomment this when populating corporation factions fully

    from create.createCivilians import create_civilian_population, place_civilians_in_homes

    factionless = next(f for f in factions if f.name == "Factionless")
    civilians = create_civilian_population(all_locations, all_regions, factionless)
    
    all_characters.extend(civilians)


    # After all civilians and locations exist:
    families = assign_families_and_homes(game_state)
    shops = [loc for loc in all_locations if getattr(loc, "is_shop", False)]
    place_civilians_in_homes(civilians, families, all_locations, shops, populate_shops_after_worldgen=True)

    # --- DIAGNOSTIC CHECK: After homes + shop patron placement ---
    #debug_print(None, "[DIAG] Checking all major faction HQs just after shop population...", "placement")

    for faction in factions:
        hq = getattr(faction, "hq", None)
        if hq:
            occupants = [c.name for c in getattr(hq, "characters_there", [])]
            debug_print(None, f"[DIAG] HQ {hq.name} occupants: {occupants}", "placement")

    debug_print(None, "[DIAG] Checking shop occupants after shop population...", "placement")
    for shop in shops:
        occupants = [c.name for c in shop.characters_there]
        #debug_print(None, f"[DIAG] SHOP (Currently) {shop.name} occupants: {occupants}",category=["placement", "economy"])

    
    
    """from game_logic import assign_random_civilians_to_random_shops
    assign_random_civilians_to_random_shops(all_regions, all_characters, count=3) """

    print(f"Total characters created: {len(all_characters)}")
    return all_characters

def player_character_options(all_regions, factions):
    """Return a list of dictionaries with character DATA instead of full objects."""
    # Define character options as data dictionaries
    #from objects.InWorldObjects import Wallet
    
    from inventory import Inventory
    from base.faction import Factionless
    
    character_data = [
    {
        "class": Manager,
        "name": "Karen Andersen",
        "first_name": "Karen",
        "family_name": "Andersen",
        "sex": "female",
        "is_player": True,
        "race": "Terran",
        "faction_name": "Hannival",
        "region_name": "downtown",
        "location_name": "Hannival HQ",
        #"wallet": Wallet(bankCardCash=500),
        "wallet": {"bankCardCash": 500, "cash": 0},
        "preferred_actions": {},
        "motivations": [
            {"type": "buy_object", "urgency": 9, "target": "SmartPhone"},
            {"type": "work", "urgency": 5},
            {"type": "earn_money", "urgency": 8},
            {"type": "virtue_signal", "urgency": 6},
            {"type": "increase_status", "urgency": 8, "status_type": "corporate"},
            {"type": "unwind", "urgency": 5},
            {"type": "have_fun", "urgency": 5}
        ],
        "primary_status_domain": "corporate",
        "status_data": {
            "corporate": {"level": StatusLevel.MID, "title": "Manager"},
            "public": {"level": StatusLevel.LOW, "title": "Suit"}
            },
        "self_awareness": {
                "override_level": None,     # Or SelfAwarenessLevel.PERSONAL
                "override_score": None
            }
    },

    {
        "class": GangMember,
        "name": "Swiz",
        "first_name": "Swiz",
        "family_name": "Novak",
        "sex": "male",
        "is_player": True,
        "race": "Terran",
        "faction_name": "Factionless",
        "region_name": "easternhole",
        "location_name": "None",
        "inventory": Inventory([Knife(owner="Swiz")]),
        #"wallet": Wallet(bankCardCash=50),
        "wallet": {"bankCardCash": 50, "cash": 0},
        "preferred_actions": {"Rob": 1, "Steal": 2},
        "motivations": [
            {"type": "join_gang", "urgency": 6},
            {"type": "obtain_ranged_weapon", "urgency": 5},
            {"type": "increase_status", "urgency": 4},
            {"type": "steal_money", "urgency": 4},
            {"type": "rob", "urgency": 4}
        ],
        "custom_skills": {"stealth": 12, "observation": 6},
        "primary_status_domain": "criminal",
        "status_data": {
            "public": {"level": StatusLevel.LOW, "title": "Unknown"},
            "criminal": {"level": StatusLevel.LOW, "title": "Alone"}
        },
        "self_awareness": {
            "override_level": None,
            "override_score": None
        }

    },
         
{
        "class": Adepta,
        "name": "Ava Kelly",
        "first_name": "Ava",
        "family_name": "Kelly",
        "sex": "female",
        "is_player": True,
        "race": "Irish",
        "faction_name": "Factionless",
        "region_name": "northville",
        "location_name": "Park",        #ATTN npcs are placed with add_character() now

        #"wallet": Wallet(bankCardCash=500),
        "wallet": {"bankCardCash": 50, "cash": 0},
        "preferred_actions": {"charm", "heal", "flirt"},
        "motivations": [
            {"type": "earn_money", "urgency": 3},
            {"type": "have_fun", "urgency": 6, "status_type": "civilian"},
            {"type": "increase_status", "urgency": 2}
        ],
        "primary_status_domain": "civilian",
        "status_data": {
            "public": {"level": StatusLevel.LOW, "title": "Woman"}
        },
        "self_awareness": {
            "override_level": None,
            "override_score": None
        }
    },

]   

    return character_data
    
def instantiate_character(char_data, all_regions, factions):
    from utils import get_faction_by_name, get_region_by_name, get_location_by_name
    from create.create_game_state import get_game_state
    from objects.InWorldObjects import Wallet
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

    #ATTN npcs are placed with add_character() now
    #not sure if that is relevant here, look at it"
    location = get_location_by_name(location_name, all_regions)
    #tmp block below
    if location is None:
        print(f"❌ ERROR: Location '{location_name}' not found!")
    else:
        print(f"[DEBUG] Location found: {location.name}")


    wallet_data = char_data.get("wallet", {})
    race = char_data["race"]
    sex = char_data["sex"]

    if region is None:
        print(f"❌ ERROR: No region found with name '{region_name}'")

    motivation_objects = char_data.get("motivations", [])

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
    fun=1,
    hunger=3,
    preferred_actions=char_data.get("preferred_actions", {}),

    custom_skills=char_data.get("custom_skills"),
    status=status
)
    character.mind = Mind(owner=character, capacity=character.intelligence)
    character.curiosity = Curiosity(base_score=character.intelligence // 2)
    character.task_manager = TaskManager(character)
    character.employment = EmployeeProfile()
    character.motivation_manager = MotivationManager(character)
    character.inventory_component = InventoryComponent(owner=character)

    knife = Knife()
    character.inventory.add_item(knife)

    character.primary_status_domain = char_data.get("primary_status_domain", "public")
    character.observation_component = ObservationComponent(owner=character)
    character.self_awareness = SelfAwarenessComponent(owner=character)
    character.is_player = char_data.get("is_player", False)
    family_name = character.family_name
    if family_name not in game_state.extant_family_names:
        game_state.extant_family_names.append(family_name)

    character.wallet = WalletComponent(
        owner=character,
        bankCardCash=wallet_data.get("bankCardCash", 0),
        cash=wallet_data.get("cash", 0)
    )


    # Populate motivations
    for m in motivation_objects:
        if isinstance(m, tuple):
            mtype, urgency = m
            character.motivation_manager.create_initial(mtype, urgency)

        elif isinstance(m, dict):
            character.motivation_manager.create_initial(
                m["type"], 
                m.get("urgency", 1),
                target=m.get("target"),
                source=m.get("source", "initial"),
                status_type=m.get("status_type")
            )


    if "inventory" in char_data:
        initial_items = char_data["inventory"]
        for item in initial_items:
            character.inventory.add_item(item)

        character.inventory.update_primary_weapon()


    if character.is_player:
        game_state.player_character = character

    return character

    