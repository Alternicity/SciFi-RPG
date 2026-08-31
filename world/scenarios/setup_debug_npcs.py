#world.scenarios.setup_debug_npcs.py
from world.scenarios.setup_tcX_helpers import register_scenario_npc
from simulation_utils import pick_civilian
from location.locations import Nightclub
from utils import get_all_civilians
from create.create_game_state import get_game_state
gs = get_game_state()

def setup_debug_npcs(all_characters):
    #TC1

    #TC2

    #TC3

    #TC4

    #Passive npcs
    civilians = get_all_civilians()
    coffee_npc = pick_civilian(civilians)
    register_scenario_npc(coffee_npc, "coffee_drinker")

    book_npc = pick_civilian(civilians, exclude={coffee_npc})
    register_scenario_npc(book_npc, "book_reader")