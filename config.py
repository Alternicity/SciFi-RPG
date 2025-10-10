# config.py
# Global game settings and constants

DEBUG_MODE = True  # Master switch for all debug printing

#do this line and the following lines functinoally overlap?
ENABLED_DEBUG_CATEGORIES = {"think", "salience", "memory", "action", "motivation", 
                            "rkprint", "decision", "anchor", "tick", "insight"}

# Individual subsystem toggles
SHOW_TICK_LOGS = True
SHOW_TEST_NPC_LOGS = True
SHOW_NPC_THINK_LOGS = True
SHOW_NPC_ACTION_LOGS = True
SHOW_MEMORY_LOGS = True
SHOW_SALIENCE_LOGS = False
SHOW_SIMULATION_LOGS = True
SHOW_GAMEPLAY_LOGS = True
SHOW_ANCHOR_LOGS = True
SHOW_RK_LOGS = False
SHOW_DECISION_LOGS = True
SHOW_INSIGHT_LOGS = True
""" In the long term:
SHOW_SALIENCE_LOGS → replace with "salience" in ENABLED_DEBUG_CATEGORIES
SHOW_NPC_ACTION_LOGS → replace with "action" in ENABLED_DEBUG_CATEGORIES """

# Optional: verbosity levels (for later)
DEBUG_LEVEL = "DEBUG"  # could be "INFO", "DEBUG", "ERROR"
