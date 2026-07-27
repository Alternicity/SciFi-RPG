#GUI.helpers.formatting.py

def is_highlighted_percept(origin, npc):

    if origin is npc:
        #return True
        return "self"

    if origin is getattr(npc, "sublocation", None):
        return "location"

    if getattr(npc, "current_interaction_target", None) is origin:
        return "interaction"

    #return False
    return None