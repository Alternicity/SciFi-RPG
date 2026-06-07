#create.create_babes.py
from characters import Babe
from create.create_game_state import get_game_state
game_state = get_game_state()
import random
from get_valid_races import get_valid_races
from create.create_character_names import create_name
from status import StatusLevel, CharacterStatus, FactionStatus
from utils import normalize_location_regions, get_region_for_location, find_location_by_type
from objects.InWorldObjects import Wallet
from character_mind import Mind, Curiosity
from tasks.tasks import TaskManager
from employment.employee import EmployeeProfile
from character_components.observation_component import ObservationComponent
from augment.augment_character import augment_character
from create.create_fun_prefs import create_fun_prefs
from create.create_personality import create_personality
from objects.InWorldObjects import Wallet
from motivation.motivation import MotivationManager
from motivation.motivation_init import initialize_motivations
from character_components.inventory_component import InventoryComponent

def create_babes(all_regions, factionless, babes_per_region=2):
    all_locations = game_state.all_locations

    babes = []

    for region in all_regions:

        race = random.choice(get_valid_races())

        first_name, family_name, full_name = create_name(
            race,
            sex="female"
        )
        random_cash = random.randint(5, 500)

        homes = [loc for loc in all_locations if "residential" in getattr(loc, "categories", [])]
        public_spaces = [loc for loc in all_locations if "public" in getattr(loc, "categories", [])]#public_spaces not yet accessed

        if not homes:
            raise ValueError("❌ No residential locations found for civilian placement.")

        # Assign home
        home = random.choice(homes)
        region_for_home = get_region_for_location(home, all_regions)
        if not region_for_home:
            print(f"⚠️ Skipping {full_name}: home {home.name} has no region.")
            continue

        babe = Babe(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            sex="female",
            race=race,
            faction=factionless,
            location=None,
            region=None,
            wallet=None,
            status=CharacterStatus()
        )

        babe.wallet=Wallet(bankCardCash=random_cash)
        babe.status.set_status("general_population", FactionStatus(StatusLevel.LOW, "Normie"))
        babe.region = region_for_home
        babe.personality = create_personality(babe)
        babe.fun_prefs = create_fun_prefs(babe)
        babe.mind = Mind(owner=babe, capacity=babe.intelligence)

        augment_character(babe)

        babe.curiosity = Curiosity(base_score=babe.intelligence // 2)
        babe.task_manager = TaskManager(babe)

        #civilian.employment = EmployeeProfile(shift_start=9, shift_end = 5)
        #paused for now
        
        babe.faction = factionless
        babe.motivation_manager = MotivationManager(babe)

        initialize_motivations(babe, passed_motivations=[("idle", 1)])

        babe.inventory_component = InventoryComponent(babe)
        babe.observation_component = ObservationComponent(owner=babe)

        game_state.all_babes.append(babe)
        babes.append(babe)

        game_state.all_characters.append(babe)

    return babes