# debug_utils.py
from config import (
    DEBUG_MODE,
    SHOW_TEST_NPC_LOGS,
    SHOW_TICK_LOGS,
    SHOW_NPC_THINK_LOGS,
    SHOW_NPC_ACTION_LOGS,
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
    DEBUG_LEVEL,
)

DEBUG_FLAGS = {
    "test_npc": SHOW_TEST_NPC_LOGS,
    "tick": SHOW_TICK_LOGS,
    "think": SHOW_NPC_THINK_LOGS,
    "action": SHOW_NPC_ACTION_LOGS,
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
}


def debug_print(npc=None, message="", category="general", level="DEBUG"):
    """
    Centralized debug printing system.
    - npc: optional NPC object, used to filter test NPC logs
    - category: one of DEBUG_FLAGS keys
    - level: string for severity ("DEBUG", "INFO", "WARNING", "ERROR")
    """

    if npc and not getattr(npc, "is_test_npc", False):
        return

    if not DEBUG_MODE:
        return

    # Respect category toggles
    if category in DEBUG_FLAGS and not DEBUG_FLAGS[category]:
        return

    # Filter out test NPCs if not requested
    if npc and getattr(npc, "is_test_npc", False) and not SHOW_TEST_NPC_LOGS:
        return

    npc_name = getattr(npc, "name", "System")
    print(f"[{level:<7}] [{category:<10}] {npc_name}: {message}")
