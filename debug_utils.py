# debug_utils.py
from config import (
    DEBUG_MODE,
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
    DEBUG_LEVEL,
)

DEBUG_FLAGS = {
    "create": SHOW_CREATE_LOGS,
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
}


def debug_print(npc=None, message="", category="general", level="DEBUG"):
    if not DEBUG_MODE:
        return

    # Allow system logs before NPCs exist
    if npc is None:
        npc_name = "System"
    else:
        # Filter out non-test NPCs
        if not getattr(npc, "is_test_npc", False):
            return
        npc_name = getattr(npc, "name", "Unknown")

    # Category filtering
    if category in DEBUG_FLAGS and not DEBUG_FLAGS[category]:
        return

    print(f"[{category:<7}] {npc_name}: {message}")

