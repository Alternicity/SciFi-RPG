#simulation.py
import random
from characters import GangMember, Civilian
from debug_utils import debug_print
from display import display_top_motivations
from simulation_utils import setup_debug_npcs_in_game_state, non_shop_or_cafe_locations, setup_tc2_debug_npcs
from create.create_game_state import get_game_state
game_state = get_game_state()
from world.TC2_presets import setup_tc2_worker

from augment.augmentLocations import reassign_shop_names_after_character_creation

""" from memory.memory_builders.food_sources_builder import build_food_sources
from memory.memory_builders.shop_knowledge_builder import build_shop_knowledge
from memory.memory_builders.region_knowledge_builder import build_region_knowledge """
from memory.injectors.initial_memory_injectors import inject_initial_region_knowledge, inject_food_location_knowledge, inject_initial_shop_knowledge
from population.population import summarize_civilians

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_hours
    from location.locations import Shop

    debug_npcs = []#not yet accessed
    debug_print(None, "Debug system initialised successfully.", category="simulation")
    debug_print(None, f"\nRunning simulation for {num_days} days...\n", category="simulation")

    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)

    debug_gang_npc2 = next((c for c in all_characters if isinstance(c, GangMember) and c is not debug_gang_npc), None)

    civilians = [c for c in all_characters if isinstance(c, Civilian)]

    debug_civilian_worker = civilians[0] if len(civilians) > 0 else None
    debug_civilian_liberty = civilians[1] if len(civilians) > 1 else None


    # tag them for other code that checks flags
    if debug_gang_npc:
        debug_gang_npc.debug_role = "primary"
        debug_gang_npc.debug = True

    if debug_gang_npc2:
        debug_gang_npc2.debug_role = "secondary"

    if debug_civilian_worker:

        debug_civilian_worker.debug_role = "civilian_worker"

    if debug_civilian_liberty:

        debug_civilian_liberty.debug_role = "civilian_liberty"

    game_state.debug_npcs["civilian_worker"] = debug_civilian_worker
    game_state.debug_npcs["civilian_liberty"] = debug_civilian_liberty

    # register in game_state.debug_npcs
    #setup_debug_npcs_in_game_state(debug_gang_npc, debug_gang_npc2, debug_civilian_worker, debug_civilian_liberty)
    setup_tc2_debug_npcs(debug_civilian_worker, debug_civilian_liberty)


    characters = [
        c for c in (
            debug_gang_npc,
            debug_gang_npc2,
            debug_civilian_worker,
            debug_civilian_liberty
        )
        if c is not None
    ]

    #list_characters(characters)
    #Nice table print, lists all characters, not test case aware

    easternhole_region = next((r for r in game_state.all_regions if r.name == "easternhole"), None)
    debug_gang_npc.region = easternhole_region
    easternhole_region.add_character(debug_gang_npc)

    northville_region = next((b for b in game_state.all_regions if b.name == "northville"), None)
    debug_gang_npc2.region = northville_region
    northville_region.add_character(debug_gang_npc2)

    downtown_region = next((r for r in game_state.all_regions if r.name == "downtown"), None)
    debug_civilian_worker.region = downtown_region
    debug_civilian_liberty.region = downtown_region

    downtown_region.add_character(debug_civilian_worker)
    downtown_region.add_character(debug_civilian_liberty)
    #We should add these npcs to game_state variables

    # Choose a non-shop location in easternhole to place the test NPC (refers to the original test npc, the GangMember that robs the shop)
    non_shop_locations = [loc for loc in easternhole_region.locations if not isinstance(loc, Shop)]

    if non_shop_locations:
        start_location = random.choice(non_shop_locations)
        debug_gang_npc.location = start_location
    else:
        print("[WARNING] No valid non-shop locations found in easternhole for debug NPC.")
    
    start_locs = non_shop_or_cafe_locations(easternhole_region)
    debug_gang_npc2.location = random.choice(start_locs)

    #start_loc_g1 = random.choice(start_locs)
    start_loc_g2 = random.choice(start_locs)#start_loc_g2 not accessed
    start_loc_civ = random.choice(start_locs)#start_loc_civ not accessed

    # Gang NPC 1 - Test Case 1
    if debug_gang_npc:
        #TC1 prints:
        """ debug_print(None, f"[Simulation] Selected DEBUG NPC: {debug_gang_npc.name}, {debug_gang_npc.race}", category="simulation")
        debug_print(None, f"[INIT] Placed debug gang NPC at {start_location.name}", category="simulation") """
        debug_gang_npc.debug = True

        debug_gang_npc.motivation_manager.update_motivations("rob", urgency=8)
        debug_gang_npc.motivation_manager.update_motivations("obtain_ranged_weapon", urgency=6)
        debug_gang_npc.motivation_manager.update_motivations("earn_money", urgency=5)

        inject_initial_region_knowledge(debug_gang_npc)
        inject_food_location_knowledge(debug_gang_npc)
        inject_initial_shop_knowledge(debug_gang_npc)

    # Gang NPC 2
    if debug_gang_npc2: #aka secondary 

        debug_gang_npc2.motivation_manager.update_motivations("shakedown", urgency=4)
        debug_gang_npc2.motivation_manager.update_motivations("eat", urgency=7)
        debug_gang_npc2.motivation_manager.update_motivations("have_fun", urgency=5)

        locs_g2 = non_shop_or_cafe_locations(northville_region)
        if locs_g2:
            debug_gang_npc2.location = random.choice(locs_g2)
        else:
            print("[WARNING] No valid locations in northville for gang npc 2.")

        inject_initial_region_knowledge(debug_gang_npc2)
        inject_food_location_knowledge(debug_gang_npc2)
        inject_initial_shop_knowledge(debug_gang_npc2)


    if debug_civilian_worker:
        setup_tc2_worker(debug_civilian_worker, downtown_region)
        debug_civilian_worker.motivation_manager.update_motivations("work", urgency=8)
        debug_civilian_worker.motivation_manager.update_motivations("eat", urgency=6)
        debug_civilian_worker.motivation_manager.update_motivations("have_fun", urgency=5)

        if debug_civilian_worker and debug_civilian_worker.family:
            debug_civilian_worker.location = debug_civilian_worker.family.home

        inject_initial_region_knowledge(debug_civilian_worker)
        inject_food_location_knowledge(debug_civilian_worker)
        inject_initial_shop_knowledge(debug_civilian_worker)

        display_top_motivations(debug_civilian_worker)
 
    if debug_civilian_liberty:
        debug_civilian_liberty.is_employee = False
        debug_civilian_liberty.employment.workplace = None
        debug_civilian_liberty.employment.role = None
        debug_civilian_liberty.motivation_manager.update_motivations("eat", urgency=8)
        debug_civilian_liberty.motivation_manager.update_motivations("find_partner", urgency=3)#but npc might automatically already have one
        debug_civilian_liberty.motivation_manager.update_motivations("have_fun", urgency=5)

        if debug_civilian_liberty and debug_civilian_liberty.family:
            debug_civilian_liberty.location = debug_civilian_liberty.family.home
            
        inject_initial_region_knowledge(debug_civilian_liberty)
        inject_food_location_knowledge(debug_civilian_liberty)
        inject_initial_shop_knowledge(debug_civilian_liberty)
        #add some more money to their wallet here, and a temporary print
        display_top_motivations(debug_civilian_liberty)

                #this npc might automaically have a partner when that is assigned. We can leave this for now.


    """ debug_npcs = [
        c for c in all_characters
        if getattr(c, "debug_role", None) in ("civilian_worker", "civilian_liberty")
    ]
    display_debug_npcs(debug_npcs) """

    from display import debug_list_gang_hqs
    #debug_list_gang_hqs()
    #nice print

    civilians = game_state.civilians 
    all_regions = game_state.all_regions

    summarize_civilians(civilians, all_regions)

    simulate_hours(all_characters, num_days=num_days, debug_character=debug_gang_npc)
    print("\nSimulation complete.")


def pick_random_npc(characters, cls, exclude=None):
    return next((c for c in characters
                 if isinstance(c, cls) and c is not exclude),
                None)







        #We should probably make some display.py function to list all three new testing npcs, with bools in config.py to 
        #indicate which ones get output prints actually printing.We dont really need to see the original test_npc in
        #output for a while (the GangMember from test case 1)