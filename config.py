# config.py
# Global game settings and constants

DEBUG_MODE = True  # Master switch for all debug printing


""" ENABLED_DEBUG_CATEGORIES = {"think", "salience", "memory", "action", "motivation", 
                            "rkprint", "decision", "anchor", "tick", "insight"} """

ENABLED_DEBUG_CATEGORIES = {"test_npc"}  # Only logs for test NPCs

# Individual subsystem toggles
SHOW_TICK_LOGS = True

# Test NPC visibility
SHOW_TEST_NPC_LOGS = True   # keep this True so test NPCs still show
# ^ only relevant when npc.is_test_npc == True

SHOW_NPC_THINK_LOGS = False
SHOW_NPC_ACTION_LOGS = False
SHOW_MEMORY_LOGS = False
SHOW_SALIENCE_LOGS = False
SHOW_SIMULATION_LOGS = False
SHOW_GAMEPLAY_LOGS = False
SHOW_ANCHOR_LOGS = False
SHOW_RK_LOGS = False
SHOW_DECISION_LOGS = False
SHOW_INSIGHT_LOGS = False
SHOW_PERCEPT_LOGS = False
SHOW_INVENTORY_LOGS = True
SHOW_INVENTORY_LOGS = True
SHOW_VISIT_LOGS = True
SHOW_FOCUS_LOGS = True
SHOW_MOTIVE_LOGS = True
""" In the long term:
SHOW_SALIENCE_LOGS → replace with "salience" in ENABLED_DEBUG_CATEGORIES
SHOW_NPC_ACTION_LOGS → replace with "action" in ENABLED_DEBUG_CATEGORIES """

# Optional: verbosity levels (for later)
DEBUG_LEVEL = "DEBUG"  # could be "INFO", "DEBUG", "ERROR"
