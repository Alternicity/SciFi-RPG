#simulation.py
import random
from characters import GangMember
from character_memory import MemoryEntry

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_days
    from create_game_state import get_game_state, game_state
    from location import Shop

    print(f"\nRunning simulation for {num_days} days...\n")
    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)

    #mark test npc
    debug_gang_npc.is_test_npc = True

    # Set test NPC to Easternhole if needed
    easternhole_region = next((r for r in game_state.all_regions if r.name == "Easternhole"), None)
    debug_gang_npc.region = easternhole_region

    # Choose a non-shop location in Easternhole to place the test NPC
    non_shop_locations = [loc for loc in easternhole_region.locations if not isinstance(loc, Shop)]

    if non_shop_locations:
        start_location = random.choice(non_shop_locations)
        debug_gang_npc.location = start_location
        start_location.characters_there.append(debug_gang_npc)
        
    else:
        print("[WARNING] No valid non-shop locations found in Easternhole for debug NPC.")
    
    from weapons import Pistol
    from InWorldObjects import CashWad

    # Add perceptible objects to that location for testing perception
    # if hasattr(test_location, "objects_present"):
    #     pistol = Pistol()
    #     cash = CashWad(amount=60)
    #     if hasattr(test_location, "objects_present"):
    #         test_location.objects_present.extend([pistol, cash])
    #         print(f"[Simulation] Placed Pistol and CashWad at {test_location.name}")
    #     else:
    #         print(f"[Simulation] ERROR: {test_location.name} has no 'objects_present' list.")


    if debug_gang_npc:
        print(f"[Simulation] Selected DEBUG NPC: {debug_gang_npc.name}, {debug_gang_npc.race}")
        print(f"[INIT] Placed debug gang NPC at {start_location.name}")
        #print(f"[Simulation] Their location: {debug_gang_npc.location}")

        #print(f"[Simulation] Their region: {debug_gang_npc.region}")

        #print(f"[Simulation] Their region: {getattr(debug_gang_npc.location, 'region', 'Unknown')}")

        debug_gang_npc.is_test_npc = True
        debug_gang_npc.debug = True  # Optional: add a `.debug` flag for visibility

        debug_gang_npc.motivation_manager.update_motivations("rob", urgency=8)
        debug_gang_npc.motivation_manager.update_motivations("obtain_ranged_weapon", urgency=6)
        debug_gang_npc.motivation_manager.update_motivations("earn_money", urgency=5)

        from create_game_state import get_game_state
        from region_knowledge_builder import build_region_knowledge

        for region in game_state.all_regions:
            region_knowledge = build_region_knowledge(region, debug_gang_npc)
            debug_gang_npc.mind.memory.semantic["region_knowledge"].append(region_knowledge)

        #note this is a debug_npc injection, not a general one for all_characters
        if region.shops:
            shop = region.shops[0]
        entry = MemoryEntry(
            subject="Shop",
            object_="ranged_weapon",
            details="This shop sells ranged weapons",
            importance=3,
            tags=["shop", "weapons"],
            target=shop,
            type="injection",
            initial_memory_type="semantic"
        )
        debug_gang_npc.mind.memory.add_semantic(entry)  

        region = debug_gang_npc.region
        if region:
            debug_gang_npc.location.region #line 82 ATTN
        else:
            print(f"[Warning] {debug_gang_npc.name} has no assigned region.")
                  

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

    simulate_days(all_characters, num_days=num_days, debug_character=debug_gang_npc)
    print("\nSimulation complete.")
    return debug_gang_npc  # useful for debugging
