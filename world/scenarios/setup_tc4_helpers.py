#world.scenarios.setup_tc4_helpers.py
from create.create_game_state import get_game_state
from world.scenarios.scenario_helpers import reserve_test_faction, select_unused_gang
from memory.injectors.initial_gang_injectors import inject_pistol_capture_memory, inject_boss_office_memory
from thoughts.gang_thoughts.initial_thought_injector import inject_pistol_capture_thought

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

def setup_tc4_minds(gang, pistol, rival_boss, rival_gang, bosses_office):
    boss = gang.boss

    witnesses = (
        gang.captains[:1]
        + gang.members[:1]
    )

    nonwitnesses = [
        npc
        for npc in gang.captains + gang.members
        if npc not in witnesses
    ]

    for npc in witnesses:
        inject_pistol_capture_memory(
            npc,
            boss,
            pistol,
            rival_boss,
            rival_gang
        )

    for npc in nonwitnesses:
        inject_pistol_capture_thought(
            npc,
            boss,
            pistol,
            rival_boss,
            rival_gang
        )


    for npc in witnesses + nonwitnesses:
        inject_boss_office_memory(npc, boss, bosses_office)

def apply_gang_percept_overrides(npc, bloodstained=None, wounded=False, notable_features=None):
    # Wraps the instance's _postprocess_percept so scenario data rides along
    # without needing a new subclass per scenario.
    original = npc._postprocess_percept
    def _pp(data, observer):
        data = original(data, observer)
        if bloodstained is not None:
            data["bloodstained"] = bloodstained
        if wounded:
            data["is_visibly_wounded"] = True
        if notable_features:
            data["notable_features"] = list(notable_features)
        return data
    npc._postprocess_percept = _pp
    

    """
    inject_...thought(...) """

    #So should this function be calling (various memory builders and injectors?)
    
    """ Boss
    → possibly his own memory of the capture

    Witnessing gang members
        → episodic memory

    Non-witnessing gang members
        → thought / knowledge about the trophy """

