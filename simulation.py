#simulation.py
import time
from characters import GangMember
from character_memory import MemoryEntry

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_days
    print(f"\nRunning simulation for {num_days} days...\n")
    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)
    if debug_gang_npc:
        print(f"[Simulation] Selected DEBUG NPC: {debug_gang_npc.name}")
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

        region = debug_gang_npc.region
        if region:
            debug_gang_npc.ai.think(region)
        else:
            print(f"[Warning] {debug_gang_npc.name} has no assigned region.")
                  

        print(f"[Motivations] {debug_gang_npc.name}:")
        for m in debug_gang_npc.motivation_manager.get_motivations():
            print(f" - {m.type} (urgency: {m.urgency})")

        print(f"{debug_gang_npc.name}'s episodic memory:")
        for mem in debug_gang_npc.memory.episodic:
            print(f" - {mem}")

        print(f"{debug_gang_npc.name}'s semantic memory:")
        for mem in debug_gang_npc.memory.semantic:
            print(f" - {mem}")

        print(f"{debug_gang_npc.name}'s thoughts, from simulation.py:")
        for thought in debug_gang_npc.mind.get_all():  # safer if you have get_all() 
            print(f" - {thought}")

    simulate_days(all_characters, num_days=num_days, debug_character=debug_gang_npc)
    print("\nSimulation complete.")
    return debug_gang_npc  # useful for debugging
