# simulate_day.py
import random
from location import Shop
from create_game_state import get_game_state
from ai_utility import UtilityAI
from events import Robbery

ai_system = UtilityAI()

def simulate_days(num_days=1):
    game_state = get_game_state()
    all_regions = game_state.all_regions

    for _ in range(num_days): #use generator here?
        for region in all_regions:
            for npc in region.characters_there:
                if npc.is_player:
                    continue  # Skip player; they act via menu

                # 1. Passive perception (AI motivation inputs)
                npc.observe(None, None, region, npc.location)

                #1.5 Observe() needs to go through percepts

                # 2. Decide what to do
                action = ai_system.choose_action(npc, region)

                # 3. Take that action
                if action == "Rob":
                    targets = ai_system.get_viable_robbery_targets(npc, region)
                    if targets:
                        target = random.choice(targets)
                    if target: #indentation?
                        robbery = Robbery(robber=npc, location=target)
                        robbery.execute()

        # 🔄 OPTIONAL: Add future game state updates here
        # update_world_state(game_state)
        # handle_daily_events(game_state)
            # Add more actions like "Buy", "Recruit", "Report", etc.


