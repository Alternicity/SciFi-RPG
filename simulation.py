#simulation.py
import time
from characters import GangMember
from character_memory import MemoryEntry

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_days
    from create_game_state import get_game_state, game_state

    print(f"\nRunning simulation for {num_days} days...\n")
    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)


    # Set test NPC to Easternhole if needed
    easternhole_region = next((r for r in game_state.all_regions if r.name == "Easternhole"), None)
    debug_gang_npc.region = easternhole_region

    #no locationn is being set here

    """ if easternhole_region:
        # Use a first location in Easternhole
        test_location = easternhole_region.locations[4]
        debug_gang_npc.location = test_location
        test_location.characters_there.append(debug_gang_npc)
        print(f"[Simulation] Moved {debug_gang_npc.name} to {test_location}")
    else:
        print("[Simulation] WARNING: Easternhole region not found.") """

    # the above block comment needs to change to put the test_npc in Easternhole, but not set a location.


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
        print(f"[Simulation] Selected DEBUG NPC: {debug_gang_npc.name}")
        print(f"[Simulation] Their location: {debug_gang_npc.location}")

        print(f"[Simulation] Their region: {debug_gang_npc.region}")

        #print(f"[Simulation] Their region: {getattr(debug_gang_npc.location, 'region', 'Unknown')}")

        debug_gang_npc.is_test_npc = True
        debug_gang_npc.debug = True  # Optional: add a `.debug` flag for visibility

        debug_gang_npc.motivation_manager.update_motivations("rob", urgency=8)
        debug_gang_npc.motivation_manager.update_motivations("obtain_ranged_weapon", urgency=6)
        debug_gang_npc.motivation_manager.update_motivations("earn_money", urgency=5)

        entry = MemoryEntry(
            subject="Shop",
            details="This shop sells ranged weapons",
            importance=3,
            tags=["shop", "weapons"]
        )
        debug_gang_npc.memory.add_entry(entry)  # Adds to episodic by default
        #If this memory is later proven useful:
        #debug_gang_npc.memory.promote_to_semantic(entry)

        #Inject a semanitc memory here, test_npc should remember that region Easternhole has a shop location
        #class shop has
        """ class Region:
            name: str
            id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
            shops: List[str] = field(default_factory=list)
            locations: List[Location] = field(default_factory=list) """
        
        #so they could access their self.region.shops maybe, and write teh memory



        region = debug_gang_npc.region
        if region:
            debug_gang_npc.ai.think(region)
        else:
            print(f"[Warning] {debug_gang_npc.name} has no assigned region.")
                  

        print(f"[Motivations] {debug_gang_npc.name}:")
        for m in debug_gang_npc.motivation_manager.get_motivations():
            print(f" - {m.type} (urgency: {m.urgency})")

        """ print(f"{debug_gang_npc.name}'s episodic memory:")
        for mem in debug_gang_npc.memory.episodic:
            print(f" - {mem}") """

        """ print(f"{debug_gang_npc.name}'s semantic memory:")
        for mem in debug_gang_npc.memory.semantic:
            print(f" - {mem}") """

        """ print(f"{debug_gang_npc.name}'s thoughts, from simulation.py:")
        for thought in debug_gang_npc.mind.get_all():  # safer if you have get_all() 
            print(f" - {thought}") """

    simulate_days(all_characters, num_days=num_days, debug_character=debug_gang_npc)
    print("\nSimulation complete.")
    return debug_gang_npc  # useful for debugging
