#world.scenarios.economy.setup_normal_economy.py
from location.locations import Powerplant, Factory, Cafe, Shop, Park
from characters import Civilian
from world.scenarios.economy.economy_logging import economy_log
from world.power_initialization import setup_normal_power
import random
from economy.economy_helpers import get_region_powerplant, get_region_factories
from world.scenarios.economy.assign_corporate_workers import assign_corporate_workers
from world.scenarios.economy.assign_corporation_ownership import assign_corporation_ownership
from create.create_game_state import get_game_state
game_state = get_game_state()

def setup_normal_economy(all_characters):
    from augment.augmentLocations import rename_factories, rename_powerplants, rename_nightclubs
    from economy.economy_helpers import seed_corporation_workers, seed_nightclub_workers
    from economy.economy_queries.economy_snapshot import economy_snapshot_tick_1
    from economy.infrastructure import update_infrastructure
    from world.scenarios.economy.assign_nightclub_ownership import assign_nightclub_ownership
    from augment.augmentLocations import seed_nightclub_furniture, augment_nightclubs



    assign_power_infrastructure()

    assign_corporation_ownership()
    assign_nightclub_ownership()


    rename_factories()
    rename_powerplants()
    rename_nightclubs()
    seed_nightclub_workers()

    seed_factory_resources()

    seed_corporation_workers()

    game_state = get_game_state()

    for corp in game_state.corporations:
        assign_corporate_workers(corp)

    all_regions = game_state.all_regions
    all_locations = game_state.all_locations

    augment_nightclubs()#Ths could actually call seed_nightclub_sublocations, seed_nightclub_furniture
    seed_nightclub_furniture(all_locations)



    setup_normal_power(all_regions)
    update_infrastructure()#added

    log_economy_summary()
    economy_snapshot_tick_1()

def assign_power_infrastructure():

    for region in game_state.all_regions:

        powerplant = get_region_powerplant(region)

        if not powerplant:
            continue

        for location in region.locations:

            if isinstance(location, Park):#no need for power, VacantLot and Stash could be added here
                continue

            if isinstance(location, (Factory, Shop, Cafe)):#maybe out of date
                pass
                

            #economy_log(f"[POWER LINK] {location} -> {powerplant}")

def seed_factory_resources():

    for location in game_state.all_locations:#culprit.Factories can start with 50, Mines can start with, idk, 100000
        """ economy_log(
            f"[DEBUG TYPE] {location.name} -> {type(location)}"
        ) """
        
        if isinstance(location, Factory):

            location.resources = {
                "ore": 50
            }
            economy_log(f"[SEED] Factory {location.name} ore=50")#verbosity culprit
            """ economy_log(
                f"[DEBUG TYPE] "
                f"{location.name} "
                f"type={type(location)} "
                f"mro={type(location).mro()}"
            ) """

def log_economy_summary():

    economy_log("=== ECONOMY SUMMARY ===")

    for plant in game_state.all_powerplants:

        economy_log(
            f"POWERPLANT: {plant.name}"
        )

        economy_log(
            f"  Workers: {len(plant.employees_there)}"
        )

    for location in game_state.all_locations:

        if isinstance(location, Factory):

            economy_log(
                f"FACTORY: {location.name}"
            )

            supplier = None

            power_component = getattr(
                location,
                "power_component",
                None
            )

            supplier = (
                power_component.power_supplier
                if power_component
                else None
            )

            supplier_name = getattr(
                supplier,
                "name",
                "None"
            )



            economy_log(
                f"  Supplier: {supplier_name}"
            )

            economy_log(
                f"  Requires Power: {power_component.requires_power}"
            )

            economy_log(
                f"  Resources: "
                f"{getattr(location, 'resources', {})}"
            )

def register_employee(npc):
    """ This is now becoming semi-obsolete:
    game_state.employed_npcs
    because employment truth is migrating into:
    npc.employment
    which is better ECS-style design. """

    game_state = get_game_state()

    if not hasattr(game_state, "employed_npcs"):
        game_state.employed_npcs = set()

    game_state.employed_npcs.add(npc)



#todo
#Ensure some corporations own Powerplants and factories
#get some civilians who work for the right Corporation and spawn them at Powerplant in their region
