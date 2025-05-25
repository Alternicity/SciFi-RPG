# simulate_day.py
import random
from location import Shop
from create_game_state import get_game_state
from ai_utility import UtilityAI
from events import Robbery
from characterActions import execute_action
DEBUG_NPC_NAME = "None"

def simulate_days(num_days=1):
    game_state = get_game_state()
    all_regions = game_state.all_regions

    for _ in range(num_days):
        for region in all_regions:
            for npc in region.characters_there:
                if npc.is_player:
                    continue

                npc.observe(None, None, region, npc.location)

                action = npc.ai.choose_action(npc, region)
                if action:
                    execute_action(npc, action, region)


        # 🔄 OPTIONAL: Add future game state updates here
        # update_world_state(game_state)
        # handle_daily_events(game_state)
            # Add more actions like "Buy", "Recruit", "Report", etc.


