# debug_utils.py
from create.create_game_state import get_game_state
game_state = get_game_state()

from config import (
    DEBUG_MODE,
    SHOW_FUN_LOGS,
    SHOW_EAT_LOGS,
    SHOW_FACTION_LOGS,
    SHOW_PRIMARY_LOGS,
    SHOW_SECONDARY_LOGS,
    SHOW_ATTRIBUTE_TEST_LOGS,
    SHOW_CREATE_LOGS,
    SHOW_TEST_NPC_LOGS,
    SHOW_TICK_LOGS,
    SHOW_NPC_THINK_LOGS,
    SHOW_ACTION_LOGS,
    SHOW_MEMORY_LOGS,
    SHOW_SALIENCE_LOGS,
    SHOW_SIMULATION_LOGS,
    SHOW_GAMEPLAY_LOGS,
    SHOW_ANCHOR_LOGS,
    SHOW_RK_LOGS,
    SHOW_DECISION_LOGS,
    SHOW_INSIGHT_LOGS,
    SHOW_PERCEPT_LOGS,
    SHOW_INVENTORY_LOGS,
    SHOW_VISIT_LOGS,
    SHOW_FOCUS_LOGS,
    SHOW_MOTIVE_LOGS,
    SHOW_OBSERVATION_LOGS,
    SHOW_THOUGHT_LOGS,
    SHOW_ERROR_LOGS,
    SHOW_WEAPON_LOGS,
    SHOW_EVENT_LOGS,
    SHOW_CHOICE_LOGS,
    SHOW_FAMILY_LOGS,
    SHOW_PLACEMENT_LOGS,
    SHOW_VERIFY_LOGS,
    SHOW_ECONOMY_LOGS,
    SHOW_EMPLOYMENT_LOGS,
    SHOW_POPULATION_LOGS,
    SHOW_GAMESTATE_LOGS,
    SHOW_ROLE_FLAGS,
    DEBUG_LEVEL,

)

DEBUG_FLAGS = {
    "fun": SHOW_FUN_LOGS,
    "eat": SHOW_EAT_LOGS,
    "create": SHOW_CREATE_LOGS,
    "primary": SHOW_PRIMARY_LOGS,
    "secondary": SHOW_SECONDARY_LOGS,
    "faction": SHOW_FACTION_LOGS,
    "placement": SHOW_PLACEMENT_LOGS,
    "test_npc": SHOW_TEST_NPC_LOGS,
    "tick": SHOW_TICK_LOGS,
    "attribute": SHOW_ATTRIBUTE_TEST_LOGS,
    "think": SHOW_NPC_THINK_LOGS,
    "action": SHOW_ACTION_LOGS,
    "memory": SHOW_MEMORY_LOGS,
    "salience": SHOW_SALIENCE_LOGS,
    "simulation": SHOW_SIMULATION_LOGS,
    "gameplay": SHOW_GAMEPLAY_LOGS,
    "anchor": SHOW_ANCHOR_LOGS,
    "rkprint": SHOW_RK_LOGS,
    "decision": SHOW_DECISION_LOGS,
    "insight": SHOW_INSIGHT_LOGS,
    "percept": SHOW_PERCEPT_LOGS,
    "inventory": SHOW_INVENTORY_LOGS,
    "visit": SHOW_VISIT_LOGS,
    "focus": SHOW_FOCUS_LOGS,
    "motive": SHOW_MOTIVE_LOGS,
    "observation": SHOW_OBSERVATION_LOGS,
    "thought": SHOW_THOUGHT_LOGS,
    "error": SHOW_ERROR_LOGS,
    "weapon": SHOW_WEAPON_LOGS,
    "event": SHOW_EVENT_LOGS,
    "choice": SHOW_CHOICE_LOGS,
    "family": SHOW_FAMILY_LOGS,
    "verify": SHOW_VERIFY_LOGS,
    "economy": SHOW_ECONOMY_LOGS,
    "gamestate": SHOW_GAMESTATE_LOGS,
    "population": SHOW_POPULATION_LOGS,
    "employment": SHOW_EMPLOYMENT_LOGS,
    # NEW — role filtering is a **parallel system**, not inside DEBUG_FLAGS
}
    
# A second parallel dict for role filtering OUTPUT
ROLE_FILTERS = {
    "primary": False,#set to False for test case 2
    "secondary": False,
    "civilian_worker": True,
    "civilian_liberty": True,
    
}

""" Why move ROLE_FILTERS into config (per test case)?
Debug policy becomes hot-swappable

Later, you can do things like:

game_state.load_debug_profile("tc2_civilians")

Which swaps:
ROLE_FILTERS
category flags
maybe even display verbosity
That is impossible if filters are hard-coded. """

#categories act like tags.
#ALL categories in the print must be enabled.
# NOTE: is_test_npc is deprecated.
# Do not use for debug filtering; use debug_role + ROLE_FILTERS instead.
def debug_print(npc=None, message="", category="general", level="DEBUG"):
    if not DEBUG_MODE:
        return
    if not message:
        return
    gs = get_game_state()

    # ---- System-level message ----
    if npc is None or not hasattr(npc, "id"):
        categories = [category] if isinstance(category, str) else list(category)
        for cat in categories:
            if cat in DEBUG_FLAGS and not DEBUG_FLAGS[cat]:
                return
        print(f"[{','.join(categories)}] System: {message}")
        return

    # ---- NPC-gated message ----
    if gs and not gs.should_display_npc(npc):
        return

    categories = [category] if isinstance(category, str) else list(category)
    for cat in categories:
        if cat in DEBUG_FLAGS and not DEBUG_FLAGS[cat]:
            return

    role = getattr(npc, "debug_role", None)
    if role is not None and not ROLE_FILTERS.get(role, False):
        return

    print(f"[{','.join(categories)}] {npc.name}: {message}")



def add_character(location, char):
    #Add a debug print to every place characters are added to a location, the ONLY legal way to add a character to characters_there.
    location.characters_there.append(char)
    """ debug_print(char,
            f"PLACED at {location.name} from debug_utils add_character",
            category=("placement", "population")) """
    #double category
    

    """ Correct Safe Ordering (prevents ghost placement):
    1. Set new location on the character
    2. Call add_character() """

#marked for deletion
def diagnose_civilian_location_integrity(region_civilians, all_civilians):#region_civilians is not accessed
    """
    Checks for duplicates and mismatched location references across civilians.
    """
    from collections import defaultdict
    location_map = defaultdict(list)

    for civ in all_civilians:
        loc_name = getattr(getattr(civ, "location", None), "name", None)
        if loc_name:
            location_map[civ.name].append(loc_name)

    duplicates = [(n, locs) for n, locs in location_map.items() if len(set(locs)) > 1]
    mismatches = []

    for civ in all_civilians:
        loc = getattr(civ, "location", None)
        if loc and civ not in getattr(loc, "characters_there", []):
            mismatches.append((civ.name, getattr(loc, "name", "?"), "not listed in location.characters_there"))

    if duplicates:
        print(f"[WARNING] Civilians appear in multiple locations: {duplicates}")
    if mismatches:
        print(f"[WARNING] Civilians with mismatched location references: {mismatches}")

_DEBUG_ONCE_KEYS = set()

def debug_once(key, npc, message, category="debug"):
    if key in _DEBUG_ONCE_KEYS:
        return
    _DEBUG_ONCE_KEYS.add(key)
    debug_print(npc, message, category=category)

def can_narrate(npc):#older, now deprecated?
    return getattr(npc, "debug_role", None) == "primary"

from config import DEBUG_MODE, DEBUG_TC1

def narration_enabled(entity=None, *, tc1=False):
    """
    Central gate for narration/debug output.
    """
    if not DEBUG_MODE:
        return False

    if tc1 and not DEBUG_TC1:
        return False

    if entity is None:
        return True

    return getattr(entity, "debug_role", None) == "primary"
