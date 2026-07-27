#world.scenarios.scenario_helpers.py
import random
from create.create_game_state import get_game_state

def reserve_test_faction(
    faction_type,
    scenario_key,
    faction
):

    gs = get_game_state()

    gs.test_factions[faction_type][scenario_key] = faction

def select_unused_gang(
    require_hq=False,
    require_boss=False,
    require_captains=False
):

    gs = get_game_state()

    reserved = set(
        gs.test_factions["gangs"].values()
    )


    candidates = []

    for gang in gs.gangs:

        if gang in reserved:
            continue

        if require_hq and gang.HQ is None:
            continue

        if require_boss and gang.boss is None:
            continue

        if require_captains and not gang.captains:
            continue

        if gang.is_street_gang:
            continue

        candidates.append(gang)


    if not candidates:
        raise RuntimeError(
            "No suitable unused gang found"
        )


    gang = random.choice(candidates)

    return gang