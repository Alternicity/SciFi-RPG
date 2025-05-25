# simulate_day.py
import random
from location import Shop
from create_game_state import get_game_state
from ai_utility import UtilityAI
from events import Robbery
from characterActions import execute_action
DEBUG_NPC_NAME = "None"

def simulate_days(all_characters, num_days=1):
    game_state = get_game_state()
    all_regions = game_state.all_regions

    for _ in range(num_days):
        for region in all_regions:
            for npc in region.characters_there:
                if npc.is_player:
                    continue

                npc.observe(None, None, region, npc.location)

                action = npc.ai.choose_action(region)
                if action:
                    npc.ai.execute_action(action, region)


    print("[OUTPUT FILTER] Showing only criminal-motivated actions")

    #tmp
    for c in all_characters:
            if not hasattr(c, "motivation_manager"):
                print(f"[ERROR] Non-character in all_characters: {type(c)} -> {c}")

    for character in all_characters:
        motivations = character.motivation_manager.get_motivations()
        criminal_motivated = any(m.type in {"rob", "steal", "obtain_ranged_weapon"} for m in motivations)

        """if criminal_motivated:
            print(f"[Action] {character.name} is criminally motivated:")
             for m in motivations:
                if m.type in {"rob", "steal", "obtain_ranged_weapon"}:
                    print(f" - {m.type} (urgency: {m.urgency})") """

        # 🔄 OPTIONAL: Add future game state updates here
        # update_world_state(game_state)
        # handle_daily_events(game_state)
            # Add more actions like "Buy", "Recruit", "Report", etc.


