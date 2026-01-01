#simulation_utils.py
from create.create_game_state import get_game_state
gamestate = get_game_state()
from debug_utils import debug_print

def setup_debug_npcs_in_game_state(
    debug_gang_npc,
    debug_gang_npc2,
    debug_civilian_worker,
    debug_civilian_liberty
):

    game_state = get_game_state()
    
    game_state.debug_npcs = {
        "primary": debug_gang_npc,
        "secondary": debug_gang_npc2,
        "civilian_worker": debug_civilian_worker,
        "civilian_liberty": debug_civilian_liberty,
    }
    
    print(f"[DEBUG] Registered {len(game_state.debug_npcs)} debug NPCs")

def non_shop_or_cafe_locations(region):
    from location.locations import Shop, Cafe, CorporateStore, Restaurant

    excluded_types = (Shop, Cafe, CorporateStore, Restaurant)

    return [
        loc for loc in region.locations 
        if not isinstance(loc, excluded_types)
    ]

def setup_tc2_debug_npcs(
    civilian_worker,
    civilian_liberty
):
    game_state = get_game_state()

    game_state.debug_npcs = {
        "civilian_worker": civilian_worker,
        "civilian_liberty": civilian_liberty,
    }

    game_state.show_background_debug = False

    print("[DEBUG] TC2 debug NPCs registered (2 civilians only)")
