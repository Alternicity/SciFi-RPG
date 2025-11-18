#simulation.py
import random
from characters import GangMember, Civilian
from ai_utils import encode_weapon_shop_memory
from debug_utils import debug_print

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_days
    from create_game_state import get_game_state, game_state
    from location import Shop

    debug_npcs = []
    debug_print(None, "Debug system initialised successfully.", category="simulation")
    debug_print(None, f"\nRunning simulation for {num_days} days...\n", category="simulation")
    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)
    debug_civilian_npc =next((a for a in all_characters if isinstance(a, Civilian)), None)

    #how will this scale when there are 30 GangMembers?
    debug_gang_npc2 = next(
    (d for d in all_characters 
     if isinstance(d, GangMember) and d is not debug_gang_npc),
    None
)

    #debug_gang_npc is only used in this file, after we always used test_npc for the test GangMember
    #mark test npc
    debug_gang_npc.is_test_npc = True
    #what do do here?
    #set debug_civilian_npc to have is_test_npc = True as well?
    #or use a new test_civilian in later files?

    # Set NPCs to Regions
    #When next scaling up use pick_random_npc()
    easternhole_region = next((r for r in game_state.all_regions if r.name == "Easternhole"), None)
    debug_gang_npc.region = easternhole_region
    easternhole_region.add_character(debug_gang_npc)

    northVille_region = next((b for b in game_state.all_regions if b.name == "NorthVille"), None)
    debug_gang_npc2.region = northVille_region
    northVille_region.add_character(debug_gang_npc2)

    downtown_region = next((r for r in game_state.all_regions if r.name == "Downtown"), None)
    debug_civilian_npc.region = downtown_region
    downtown_region.add_character(debug_civilian_npc)

    
    #For debug_print filtering
    debug_gang_npc.debug_role = "primary"
    debug_gang_npc2.debug_role = "secondary"
    debug_civilian_npc.debug_role = "civilian_test"

    #We should add these npcs to their region objects, and game_state

    # Choose a non-shop location in Easternhole to place the test NPC
    non_shop_locations = [loc for loc in easternhole_region.locations if not isinstance(loc, Shop)]

    if non_shop_locations:
        start_location = random.choice(non_shop_locations)
        debug_gang_npc.location = start_location
    else:
        print("[WARNING] No valid non-shop locations found in Easternhole for debug NPC.")
    
    start_locs = non_shop_or_cafe_locations(easternhole_region)
    debug_gang_npc2.location = random.choice(start_locs)

    #start_loc_g1 = random.choice(start_locs)
    start_loc_g2 = random.choice(start_locs)
    start_loc_civ = random.choice(start_locs)

    from create_game_state import get_game_state
    from region_knowledge_builder import build_region_knowledge

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

    if debug_gang_npc2:
        #debug_gang_npc2.is_test_npc = True
        #we need to decide if we are setting several npcs to is_test_npc = True or use something different
        debug_gang_npc2.motivation_manager.update_motivations("shakedown", urgency=8)
        debug_gang_npc2.motivation_manager.update_motivations("eat", urgency=6)
        debug_gang_npc2.motivation_manager.update_motivations("have_fun", urgency=5)
        start_location = start_location = random.choice(non_shop_or_cafe_locations)
        debug_gang_npc2.location = start_location
        inject_initial_region_knowledge(debug_gang_npc2)

    if debug_civilian_npc:
        #debug_civilian_npc.is_test_npc = True 
        #we need to decide if we are setting several npcs to is_test_npc = True or use something different
        debug_civilian_npc.motivation_manager.update_motivations("work", urgency=8)
        debug_civilian_npc.motivation_manager.update_motivations("eat", urgency=6)
        debug_civilian_npc.motivation_manager.update_motivations("have_fun", urgency=5)
        start_location = start_location = start_location = random.choice(non_shop_or_cafe_locations)
        debug_civilian_npc.location = start_location
        inject_initial_region_knowledge(debug_civilian_npc)
        
        

        def inject_initial_region_knowledge(npc, game_state):
            for region in game_state.all_regions:
                rk = build_region_knowledge(region, npc)
                npc.mind.memory.semantic["region_knowledge"].append(rk)  

        #and placeholder code put here for a more general shop knowledge, not weapon centric
        #When shops are more specialized, npcs will need to know which shop sells what.
        #I will have to build also an encode_XYZ_shop_memory()

        def inject_initial_shop_knowledge(npc, game_state):
            for region in game_state.all_regions:
                for shop in getattr(region, "shops", []):
                    mem = encode_weapon_shop_memory(npc, shop)#FIX
                    npc.mind.memory.add_semantic_unique(
                        "shop_knowledge", mem, dedupe_key="details"
                    )


        def inject_food_location_knowledge(npc, game_state):
            food_locs = []
            for region in game_state.all_regions:
                for loc in region.locations:
                    if hasattr(loc, "is_food_source") and loc.is_food_source:
                        food_locs.append(loc)

            for loc in food_locs:
                mem = {
                    "type": "food_location",
                    "details": loc.name,
                    "region": loc.region.name,
                }
                npc.mind.memory.semantic["food_locations"].append(mem)


        def non_shop_or_cafe_locations(region):
            from location import Shop, Cafe
            return [loc for loc in region.locations if not isinstance(loc, (Shop, Cafe))]



            
        #We should probably make some display.py function to list all three npcs, with bools in config.py to 
        #indicate which ones get output prints actually printing.We dont really need to see test_npc in
        #output for a while
        print(f"[Motivations] {debug_gang_npc.name}:")
        for m in debug_gang_npc.motivation_manager.get_motivations():
            print(f" - {m.type} (urgency: {m.urgency})")
        

        """ print(f"{debug_gang_npc.name}'s episodic memory:")
        for mem in debug_gang_npc.mind.memory.episodic:
            print(f" - {mem}") """

        """ print(f"{debug_gang_npc.name}'s semantic memory:")
        for mem in debug_gang_npc.mind.memory.semantic:
            print(f" - {mem}") """

        """ print(f"{debug_gang_npc.name}'s thoughts, from simulation.py:")
        for thought in debug_gang_npc.mind.get_all():  # safer if you have get_all() 
            print(f" - {thought}") """

    from create_game_state import get_game_state
    from display import debug_list_gang_hqs
    game_state = get_game_state()
    debug_list_gang_hqs(game_state)
    #call other display.py functions listing important info for the new npcs


    simulate_days(all_characters, num_days=num_days, debug_character=debug_gang_npc)
    print("\nSimulation complete.")

def pick_random_npc(characters, cls, exclude=None):
    return next((c for c in characters 
                 if isinstance(c, cls) and c is not exclude),
                None)