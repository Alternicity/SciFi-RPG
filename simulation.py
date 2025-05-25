#simulation.py
import time
from characters import GangMember
from character_memory import MemoryEntry

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_days

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

        print(f"[Motivations] {debug_gang_npc.name}:")
        for m in debug_gang_npc.motivation_manager.get_motivations():
            print(f" - {m.type} (urgency: {m.urgency})")

        print(f"{debug_gang_npc.name}'s episodic memory:")
        for mem in debug_gang_npc.memory.episodic:
            print(f" - {mem}")

        print(f"{debug_gang_npc.name}'s semantic memory:")
        for mem in debug_gang_npc.memory.semantic:
            print(f" - {mem}")

        """ if npc.name == debug_gang_npc.name:
            print(f"[DEBUG] {npc.name} thoughts after action: {list(npc.thoughts)}") """


        print(f"{debug_gang_npc.name}'s thoughts:")
        for thought in debug_gang_npc.thoughts:
            print(f" - {thought}")

    print(f"\nRunning simulation for {num_days} days...\n")
    simulate_days(all_characters, num_days=num_days)
    print("\nSimulation complete.")
    return debug_gang_npc  # useful for debugging
