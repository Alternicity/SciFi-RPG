#simulation.py
import random
from characters import GangMember, Civilian
from ai.ai_utils import encode_weapon_shop_memory
from debug_utils import debug_print
from create.create_game_state import get_game_state, game_state#is game_state needed here?
from display import display_all_debug_npcs
game_state = get_game_state()

from augment.augmentLocations import reassign_shop_names_after_character_creation
""" from memory.memory_builders.food_sources_builder import build_food_sources
from memory.memory_builders.shop_knowledge_builder import build_shop_knowledge
from memory.memory_builders.region_knowledge_builder import build_region_knowledge """
from memory.injectors.initial_memory_injectors import inject_initial_region_knowledge, inject_food_location_knowledge, inject_initial_shop_knowledge
from population.population import summarize_civilians

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_days
    
    from location.locations import Shop

    debug_npcs = []#not accessed
    debug_print(None, "Debug system initialised successfully.", category="simulation")
    debug_print(None, f"\nRunning simulation for {num_days} days...\n", category="simulation")

    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)
    debug_gang_npc2 = next((c for c in all_characters
                            if isinstance(c, GangMember) and c is not debug_gang_npc), None)
    debug_civilian_npc = next((c for c in all_characters if isinstance(c, Civilian)), None)


    #debug_gang_npc is only used in this file, after, in test case 1 logic,  we always used test_npc for this GangMember
    debug_gang_npc.is_test_npc = True
    #what do do here?
    #set debug_civilian_npc to have is_test_npc = True as well?
    #will it matter?

    # Set NPCs to Regions
    #When next scaling up use pick_random_npc()
    easternhole_region = next((r for r in game_state.all_regions if r.name == "easternhole"), None)
    debug_gang_npc.region = easternhole_region
    easternhole_region.add_character(debug_gang_npc)

    northville_region = next((b for b in game_state.all_regions if b.name == "northville"), None)
    debug_gang_npc2.region = northville_region
    northville_region.add_character(debug_gang_npc2)

    downtown_region = next((r for r in game_state.all_regions if r.name == "downtown"), None)
    debug_civilian_npc.region = downtown_region
    downtown_region.add_character(debug_civilian_npc)

    #For debug_print filtering
    debug_gang_npc.debug_role = "primary"
    debug_gang_npc2.debug_role = "secondary"
    debug_civilian_npc.debug_role = "civilian_test"

    #We should add these npcs to their region objects, and game_state

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

    
    

    if debug_gang_npc:
        debug_print(None, f"[Simulation] Selected DEBUG NPC: {debug_gang_npc.name}, {debug_gang_npc.race}", category="simulation")
        debug_print(None, f"[INIT] Placed debug gang NPC at {start_location.name}", category="simulation")
        #First parameter is None. We cant ues npc here like with most debug_prints - can we use debug_gang_npc?
        #will debug_print accept it? Could these two prints be consolidate into one?

        debug_gang_npc.debug = True  # Does this attribute even exist?

        debug_gang_npc.motivation_manager.update_motivations("rob", urgency=8)
        debug_gang_npc.motivation_manager.update_motivations("obtain_ranged_weapon", urgency=6)
        debug_gang_npc.motivation_manager.update_motivations("earn_money", urgency=5)

        inject_initial_region_knowledge(debug_gang_npc)
        inject_food_location_knowledge(debug_gang_npc)
        inject_initial_shop_knowledge(debug_gang_npc)

    if debug_gang_npc2:
        #debug_gang_npc2.is_test_npc = True
        #we need to decide if we are setting several npcs to is_test_npc = True or use something different
        debug_gang_npc2.motivation_manager.update_motivations("shakedown", urgency=8)
        debug_gang_npc2.motivation_manager.update_motivations("eat", urgency=6)
        debug_gang_npc2.motivation_manager.update_motivations("have_fun", urgency=5)


        # Gang NPC 2
        locs_g2 = non_shop_or_cafe_locations(northville_region)
        if locs_g2:
            debug_gang_npc2.location = random.choice(locs_g2)
        else:
            print("[WARNING] No valid locations in northville for gang npc 2.")

        inject_initial_region_knowledge(debug_gang_npc2)
        inject_food_location_knowledge(debug_gang_npc2)
        inject_initial_shop_knowledge(debug_gang_npc2)

    if debug_civilian_npc:

        debug_civilian_npc.motivation_manager.update_motivations("work", urgency=8)
        debug_civilian_npc.motivation_manager.update_motivations("eat", urgency=6)
        debug_civilian_npc.motivation_manager.update_motivations("have_fun", urgency=5)

        locs_civ = non_shop_or_cafe_locations(downtown_region)
        if locs_civ:
            debug_civilian_npc.location = random.choice(locs_civ)
        else:
            print("[WARNING] No valid locations in downtown for civilian npc.")
        inject_initial_region_knowledge(debug_civilian_npc)
        inject_food_location_knowledge(debug_civilian_npc)
        inject_initial_shop_knowledge(debug_civilian_npc)

        print(f"[Motivations] {debug_gang_npc.name}:")
        for m in debug_gang_npc.motivation_manager.get_motivations():
            print(f" - {m.type} (urgency: {m.urgency})")

    debug_civilian_npc.is_test_npc = True
    debug_gang_npc.is_test_npc = True
    debug_gang_npc2.is_test_npc = True


    #Claude line
    setup_debug_npcs_in_game_state(debug_gang_npc, debug_gang_npc2, debug_civilian_npc)
    display_all_debug_npcs()

    from create.create_game_state import get_game_state
    from display import debug_list_gang_hqs
    
    debug_list_gang_hqs(game_state)#odd that game_state is used as a parameter, it is designed to route around parameter passing

    civilians = game_state.civilians 
    all_regions = game_state.all_regions

    summarize_civilians(civilians, all_regions)

    simulate_days(all_characters, num_days=num_days, debug_character=debug_gang_npc)
    print("\nSimulation complete.")

def pick_random_npc(characters, cls, exclude=None):
    return next((c for c in characters
                 if isinstance(c, cls) and c is not exclude),
                None)


def setup_debug_npcs_in_game_state(debug_gang_npc, debug_gang_npc2, debug_civilian_npc):
    """
    Call this in simulation.py to register debug NPCs for easy access.
    
    Usage in simulation.py:
        setup_debug_npcs_in_game_state(debug_gang_npc, debug_gang_npc2, debug_civilian_npc)
    """
    game_state = get_game_state()
    
    game_state.debug_npcs = {
        'primary': debug_gang_npc,
        'secondary': debug_gang_npc2,
        'civilian_test': debug_civilian_npc
    }
    
    print(f"[DEBUG] Registered {len(game_state.debug_npcs)} debug NPCs")

def non_shop_or_cafe_locations(region):
    from location.locations import Shop, Cafe, CorporateStore, Restaurant

    excluded_types = (Shop, Cafe, CorporateStore, Restaurant)

    return [
        loc for loc in region.locations 
        if not isinstance(loc, excluded_types)
    ]


        #We should probably make some display.py function to list all three new testing npcs, with bools in config.py to 
        #indicate which ones get output prints actually printing.We dont really need to see the original test_npc in
        #output for a while (the GangMember from test case 1)
