#world.scenarios.setup_tc2.py
from create.create_game_state import get_game_state
game_state = get_game_state()
from employment.roles import CAFE_MANAGER, WAITRESS
from characters import Civilian
from memory.injectors.initial_memory_injectors import inject_initial_region_knowledge, inject_food_location_knowledge, inject_initial_shop_knowledge, inject_fun_prefs
from simulation_utils import pick_civilian, assign_fallback_location
import random
from employment.employee import EmployeeProfile
from debug_utils import debug_print
from world.placement import place_character
from base.posture import Posture
from objects.food.drinks import Coffee
from objects.food.cutlery_crockery import Cup
from location.locations import Cafe
from objects.furniture import CafeTable, CafeChair
from character_components.npc_effects import MorningSettlingEffect
from world.scenarios.economy.setup_normal_economy import register_employee


def setup_tc2_world(all_characters):
    civilians = [c for c in all_characters if isinstance(c, Civilian)]
    debug_civilian_worker = pick_civilian(civilians)
    debug_civilian_liberty = pick_civilian(
        civilians,
        exclude={debug_civilian_worker}
    )

    debug_civilian_waitress = pick_civilian(
        civilians,
        sex="female",
        exclude={debug_civilian_worker, debug_civilian_liberty}
    )

    downtown_region = next(
        (
            r for r in game_state.all_regions
            if r.name == "downtown"
        ),
        None
    )
    if debug_civilian_worker:
        debug_civilian_worker.debug_role = "civilian_worker"
        debug_civilian_worker.is_scenario_npc = True

    if debug_civilian_liberty:
        debug_civilian_liberty.debug_role = "civilian_liberty"
        debug_civilian_liberty.is_scenario_npc = True

    if debug_civilian_waitress:
        debug_civilian_waitress.debug_role = "civilian_waitress"
        debug_civilian_waitress.is_scenario_npc = True

    #tmp
    """ print(
        "[TC2 LIBERTY, from setup_tc2_world]",
        debug_civilian_liberty.name,
        debug_civilian_liberty.is_employee,
        debug_civilian_liberty.is_scenario_npc
    ) """

    debug_civilian_passive = pick_civilian(
            civilians,
            exclude={debug_civilian_worker, debug_civilian_liberty, debug_civilian_waitress}
        )
    if debug_civilian_passive:
        game_state.debug_npcs["civilian_passive"] = debug_civilian_passive
        debug_civilian_passive.debug_role = "civilian_passive"
        debug_civilian_passive.is_scenario_npc = True

        from character_think_utils import build_colony_doubt_thought
        debug_civilian_passive.mind.thoughts.append(
            build_colony_doubt_thought(debug_civilian_passive)
        )
        place_tc2_passive_npc(debug_civilian_passive, downtown_region)
        
    if debug_civilian_worker:
        game_state.debug_npcs["civilian_worker"] = debug_civilian_worker
    if debug_civilian_liberty:
        game_state.debug_npcs["civilian_liberty"] = debug_civilian_liberty
    if debug_civilian_waitress:
        game_state.debug_npcs["civilian_waitress"] = debug_civilian_waitress


    downtown_region = next((r for r in game_state.all_regions if r.name == "downtown"), None)
    debug_civilian_worker.region = downtown_region
    debug_civilian_liberty.region = downtown_region

    downtown_region.add_character(debug_civilian_worker)
    downtown_region.add_character(debug_civilian_liberty)
    downtown_region.add_character(debug_civilian_waitress)

    if debug_civilian_worker:
        setup_tc2_worker(debug_civilian_worker, downtown_region, role=CAFE_MANAGER)
        ## setup_tc2_worker now handles home and location
        debug_civilian_worker.motivation_manager.update_motivations("work", urgency=8)
        debug_civilian_worker.motivation_manager.update_motivations("eat", urgency=6)
        debug_civilian_worker.motivation_manager.update_motivations("have_fun", urgency=5)
        
        debug_civilian_worker.placement_locked = True
        
        inject_initial_region_knowledge(debug_civilian_worker)
        inject_food_location_knowledge(debug_civilian_worker)
        inject_initial_shop_knowledge(debug_civilian_worker)

    if debug_civilian_waitress:
        if debug_civilian_waitress is debug_civilian_worker:
            raise RuntimeError("Waitress and worker resolved to the same NPC")
        setup_tc2_worker(debug_civilian_waitress, downtown_region, role=WAITRESS)
        ## setup_tc2_worker now handles home and location

        debug_civilian_waitress.motivation_manager.update_motivations("work", urgency=8)
        debug_civilian_waitress.motivation_manager.update_motivations("eat", urgency=6)
        debug_civilian_waitress.motivation_manager.update_motivations("have_fun", urgency=5)

        debug_civilian_waitress.placement_locked = True
        
        inject_food_location_knowledge(debug_civilian_waitress)
        inject_initial_shop_knowledge(debug_civilian_waitress)
        inject_initial_region_knowledge(debug_civilian_waitress)

    else:
        print(
            f"[PLACEMENT ERROR] Waitress {debug_civilian_waitress.name} "
            f"is NOT in region.characters_there"
        )

    if debug_civilian_liberty:
        debug_civilian_liberty.is_employee = False

        #tmp
        #print(debug_civilian_liberty)
        print(debug_civilian_liberty.employment)
        print(type(debug_civilian_liberty.employment))
        print(debug_civilian_liberty.__class__.__name__)


        if debug_civilian_liberty.employment is None:
            debug_civilian_liberty.employment = EmployeeProfile()

        debug_civilian_liberty.employment.workplace = None
        debug_civilian_liberty.employment.role = None


        debug_civilian_liberty.motivation_manager.update_motivations("eat", urgency=8)
        debug_civilian_liberty.motivation_manager.update_motivations("find_partner", urgency=3)#but npc might automatically already have one
        debug_civilian_liberty.motivation_manager.update_motivations("have_fun", urgency=5)

        setup_tc2_civilian_liberty(debug_civilian_liberty, region=downtown_region)
        debug_civilian_liberty.placement_locked = True

        inject_initial_region_knowledge(debug_civilian_liberty)
        inject_food_location_knowledge(debug_civilian_liberty)
        inject_initial_shop_knowledge(debug_civilian_liberty)
        inject_fun_prefs(debug_civilian_liberty)

    #handle homeless NOTE this might affect the TC1 GangMember npcs also
    for npc in all_characters:
        if not isinstance(npc, Civilian):#or not
            continue

        if npc.placement_locked:
            continue

        if npc.location is None and npc.is_homeless:
            assign_fallback_location(
                npc,
                npc.region or npc.home_region or downtown_region#downtown implies tc2
            )

        if npc.location:
            npc.region = npc.location.region


def get_tc2_cafe(region):#not used for civilian_liberty setup
    cafe = next(
        (loc for loc in region.locations if loc.__class__.__name__ == "Cafe"),
        None
    )
    if not cafe:
        raise RuntimeError("TC2 requires a Cafe in region")
    return cafe

def setup_tc2_civilian_liberty(npc, region):
    npc.region = region
    npc.home_region = region
    npc.hunger = 5
    npc.effects.append(MorningSettlingEffect())
    npc.effects[-1].on_start(npc)

    # Force home to be in the correct region
    home_candidates = [
        loc for loc in region.locations
        if loc.__class__.__name__ in ("House", "ApartmentBlock")
    ]
    if home_candidates:
        chosen_home = random.choice(home_candidates)
        npc.residences = [chosen_home]      # sets npc.home via property
        npc.location = chosen_home
        if npc not in chosen_home.characters_there:
            chosen_home.characters_there.append(npc)
        gs = get_game_state()
        gs.reserved_homes[npc.id] = chosen_home

def setup_tc2_worker(worker, region, *, role):#civilian_manager, and civilian_waitress
    
    cafe = get_tc2_cafe(region)

    worker.is_employee = True

    # Create employment profile
    worker.employment = EmployeeProfile(
        workplace=cafe,
        role=role,
        role_type=role.role_type,
        shift="day",
        shift_start=1,
        shift_end=4
    )
    register_employee(worker)
    # Register as employee (NOT arrival)
    if hasattr(cafe, "employees"):
        cafe.employees.append(worker)

    # Force home to correct region
    home_candidates = [
        loc for loc in region.locations
        if loc.__class__.__name__ in ("House", "ApartmentBlock")
    ]
    if home_candidates:
        chosen_home = random.choice(home_candidates)
        if chosen_home not in worker.residences:
            worker.residences = [chosen_home]  # set as primary residence
        worker.location = chosen_home
        if worker not in chosen_home.characters_there:
            chosen_home.characters_there.append(worker)

        gs = get_game_state()
        gs.reserved_homes[worker.id] = chosen_home

    # Attach to worker/manager to counter
    if isinstance(worker.location, Cafe) and worker.employment.role == CAFE_MANAGER:
        counter = getattr(worker.location, "counter", None)
        if counter:
            counter.seat(worker)
            worker.posture = Posture.STANDING  # behind counter
            worker.current_counter = counter

#Call after all characters are created
def seed_tc2_presets(waitress, manager):
    social = waitress.mind.memory.semantic.get("social")
    rel = social.get_relation(manager)
    rel.current_type = "co_worker"
    rel.trust = 2

def place_tc2_passive_npc(npc, region):
    from location.locations import Nightclub
    
    region = random.choice(game_state.all_regions)

    nightclubs = [
        loc for loc in region.locations
        if isinstance(loc, Nightclub)
    ]

    nightclub = random.choice(nightclubs)
    nightclub.is_tc2_nightclub = True
    #print(f"[TC2] Selected nightclub: {nightclub.name}")
    
    if not nightclub:
        raise RuntimeError("No Nightclub found in region for passive NPC placement.")

    # Assign region + location
    npc.region = region
    npc.location = nightclub
    npc.seated_at = None
    
    nightclub.characters_there.append(npc)

    # Lock down behaviour
    npc.debug_role = "civilian_passive"
    npc.placement_locked = True#starting to look deprecated

    # Find a table
    table = next(
        (o for o in nightclub.items.objects_present
        if isinstance(o, CafeTable) and not o.occupants),
        None
    )

    if table:
        from actions.npc_bodily_actions import sit_auto #actions.npc_bodily_actions marked Import cannot be resolved
        sit_auto(npc, table=table)

    # Create drink
    cup = Cup()
    coffee = Coffee()
    cup.add(coffee)

    # Put cup on table if seated
    if table:
        nightclub.items.objects_present.append(cup)
    else:
        nightclub.items.objects_present.append(cup)

    return npc

def place_tc2_npc(npc, region):
    npc.region = region

    # 🔥 Ensure valid starting location in region
    if not npc.location or npc.location.region != region:
        candidates = [
            loc for loc in region.locations
            if loc.__class__.__name__ in ("House", "ApartmentBlock")
        ]

        if candidates:
            location = random.choice(candidates)
            place_character(npc, location)
        else:
            # fallback but STILL in region
            fallback = random.choice(region.locations)
            place_character(npc, fallback)

def assign_tc2_staging_location(npc, region):

    candidates = [
        loc for loc in region.locations
        if "restaurant" not in loc.tags
        and "cafe" not in loc.tags
        and "park" not in loc.tags
        and "vacant" not in loc.tags
    ]

    if not candidates:
        return False

    loc = random.choice(candidates)

    npc.location = loc
    npc.region = region
    loc.characters_there.append(npc)

    return True
