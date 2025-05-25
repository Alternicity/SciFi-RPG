
from characters import GangMember

def run_simulation(all_characters, num_days=10):
    from simulate_day import simulate_days

    debug_gang_npc = next((c for c in all_characters if isinstance(c, GangMember)), None)
    if debug_gang_npc:
        DEBUG_NPC_NAME = debug_gang_npc.name
        print(f"DEBUG_NPC_NAME set to: {DEBUG_NPC_NAME}")
        debug_gang_npc.add_motivation("earn_money")
        debug_gang_npc.add_motivation("obtain_ranged_weapon")
        debug_gang_npc.add_motivation("rob")  # Assuming these work

    print(f"\nRunning simulation for {num_days} days...\n")
    simulate_days(num_days=num_days)
    print("\nSimulation complete.")