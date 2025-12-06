# debug_utils.py
from config import (
    DEBUG_MODE,
    SHOW_FUN_LOGS,
    SHOW_EAT_LOGS,
    SHOW_FACTION_LOGS,
    SHOW_PRIMARY_LOGS,
    SHOW_SECONDARY_LOGS,
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
    
# A second parallel dict for role filtering:
ROLE_FILTERS = {
    "primary": True,
    "secondary": True,
    "civilian_test": True,
    "test_npc": False,
}

#categories act like tags.
#ALL categories in the print must be enabled.
def debug_print(npc=None, message="", category="general", level="DEBUG"):
    if not DEBUG_MODE:
        return

    # ----- Resolve categories -----
    if isinstance(category, str):
        categories = [category]
    else:
        categories = list(category)

    # ----- Category filtering -----
    for cat in categories:
        if cat in DEBUG_FLAGS and not DEBUG_FLAGS[cat]:
            return

    # 1 — NPC filter
    if npc is not None:
        role = getattr(npc, "debug_role", None)
        if role is not None:
            if not ROLE_FILTERS.get(role, False):
                return  # suppressed because of NPC’s role

    # 2 — category filter
    """ if category in DEBUG_FLAGS and not DEBUG_FLAGS[category]:
        return """
    #delete if multi category prints work

    # ----- Message formatting -----
    npc_name = getattr(npc, "name", "System")
    print(f"[{','.join(categories)}] {npc_name}: {message}")


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

#marked for deletion, not currently called
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

