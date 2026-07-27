#world.scenarios.setup_tc4_helpers.py
from create.create_game_state import get_game_state
from world.scenarios.scenario_helpers import reserve_test_faction, select_unused_gang
def select_tc4_gang():

    gs = get_game_state()

    # Already selected
    existing = gs.test_factions["gangs"].get("TC4")

    if existing:
        return existing

    gang = select_unused_gang(
        require_hq=True,
        require_boss=True,
        require_captains=True
    )

    reserve_test_faction(
        "gangs",
        "TC4",
        gang
    )
    return gang