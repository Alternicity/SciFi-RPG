# config.py
# Global game settings and constants

DEBUG_MODE = True  # Master switch for all debug printing
DEBUG_TC1 = False         # legacy TC1 narration
DEBUG_TC2 = True          # current focus
#ATTN are these used?

""" ENABLED_DEBUG_CATEGORIES = {"think", "salience", "memory", "action", "motivation", 
                            "rkprint", "decision", "anchor", "tick", "insight"} """

ENABLED_DEBUG_CATEGORIES = {"test_npc"}  # Only logs for test NPCs

# Individual subsystem toggles
SHOW_TICK_LOGS = True



# Test NPC visibility
SHOW_TEST_NPC_LOGS = True   # keep this True so test NPCs still show
# ^ only relevant when npc.is_test_npc == True

SHOW_CREATE_LOGS = True
SHOW_FUN_LOGS = True
SHOW_EAT_LOGS = True
SHOW_FACTION_LOGS = True
SHOW_ROLE_FLAGS = True
SHOW_PRIMARY_LOGS = True
SHOW_SECONDARY_LOGS = True
SHOW_ATTRIBUTE_TEST_LOGS = True
SHOW_NPC_THINK_LOGS = True
SHOW_ACTION_LOGS = True
SHOW_MEMORY_LOGS = True
SHOW_SALIENCE_LOGS = True
SHOW_SIMULATION_LOGS = True
SHOW_GAMEPLAY_LOGS = True
SHOW_ANCHOR_LOGS = True
SHOW_RK_LOGS = True
SHOW_DECISION_LOGS = True
SHOW_INSIGHT_LOGS = True
SHOW_PERCEPT_LOGS = True
SHOW_EFFECT_LOGS = True
SHOW_BUY_LOGS = True
SHOW_TC2_LOGS =True
SHOW_INTERACTION_LOGS = True
SHOW_INVENTORY_LOGS = True
SHOW_OBSERVATION_LOGS =True
SHOW_THOUGHT_LOGS = True
SHOW_VISIT_LOGS = True
SHOW_FOCUS_LOGS = True
SHOW_MOTIVE_LOGS = True
SHOW_ERROR_LOGS = True
SHOW_WEAPON_LOGS =True
SHOW_ACTION_LOGS = True
SHOW_EVENT_LOGS = True
SHOW_FAMILY_LOGS = False
SHOW_PLACEMENT_LOGS = True
SHOW_VERIFY_LOGS = True
SHOW_ECONOMY_LOGS = True
SHOW_EMPLOYMENT_LOGS = True
SHOW_POPULATION_LOGS = True
SHOW_GAMESTATE_LOGS = True
SHOW_CHOICE_LOGS = True
""" In the long term:
SHOW_SALIENCE_LOGS → replace with "salience" in ENABLED_DEBUG_CATEGORIES
SHOW_NPC_ACTION_LOGS → replace with "action" in ENABLED_DEBUG_CATEGORIES """

# Optional: verbosity levels (for later)
DEBUG_LEVEL = "DEBUG"  # could be "INFO", "DEBUG", "ERROR"
