#world.scenarios.setup_tc1.py
import random
from create.create_game_state import get_game_state
from simulation_utils import non_shop_or_cafe_locations
from characters import GangMember
from location.locations import Shop
game_state = get_game_state()
from memory.injectors.initial_memory_injectors import (
    inject_initial_region_knowledge,
    inject_food_location_knowledge,
    inject_initial_shop_knowledge
)

def setup_tc1_world(all_characters):
    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)#all_characters, the early flow
    #variable. We might be able to pass it in to a function here, if not there should be a game_state
    #equivalent
    debug_gang_npc2 = next((c for c in all_characters if isinstance(c, GangMember) and c is not debug_gang_npc), None)
    #The Gangmembers are currently unused and ignored in TC2


    # tag them for other code that checks flags
    if debug_gang_npc:
        debug_gang_npc.debug_role = "primary"
        debug_gang_npc.debug = True
    if debug_gang_npc2:
        debug_gang_npc2.debug_role = "secondary"

    easternhole_region = next((r for r in game_state.all_regions if r.name == "easternhole"), None)
    debug_gang_npc.region = easternhole_region
    easternhole_region.add_character(debug_gang_npc)

    northville_region = next((b for b in game_state.all_regions if b.name == "northville"), None)
    debug_gang_npc2.region = northville_region
    northville_region.add_character(debug_gang_npc2)

    # Choose a non-shop location in easternhole to place the test NPC (refers to the original test npc, the GangMember that robs the shop)
    non_shop_locations = [loc for loc in easternhole_region.locations if not isinstance(loc, Shop)]

    if non_shop_locations:
        start_location = random.choice(non_shop_locations)
        debug_gang_npc.location = start_location
    else:
        print("[WARNING] No valid non-shop locations found in easternhole for debug NPC.")

    start_locs = non_shop_or_cafe_locations(easternhole_region)
    debug_gang_npc2.location = random.choice(start_locs)

    # Gang NPC 1 - Test Case 1
    if debug_gang_npc:
        #TC1 prints:
        
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