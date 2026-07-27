#world.scenarios.setup_tcX_helpers.py

from create.create_game_state import get_game_state
gs = get_game_state()

def register_scenario_npc(npc, role,):

    npc.is_scenario_npc = True
    npc.debug_role = role

    key = role

    counter = 2

    while key in gs.debug_npcs:
        key = f"{role} {counter}"
        counter += 1

    gs.debug_npcs[key] = npc

def available_for_scenario(npc):

    return not getattr(
        npc,
        "is_scenario_npc",
        False
    )
