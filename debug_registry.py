
# debug_registry.py
# Holds which NPC instance should be printed.

DEBUG_NPC_ONLY = None

def set_debug_npc(npc):
    global DEBUG_NPC_ONLY
    DEBUG_NPC_ONLY = npc

def get_debug_npc():
    return DEBUG_NPC_ONLY