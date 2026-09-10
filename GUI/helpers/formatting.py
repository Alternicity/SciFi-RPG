#GUI.helpers.formatting.py

def is_highlighted_percept(origin, npc):
    # Return a display tag for percepts with special relevance to the observer.
    if origin is npc:
    # "self" identifies the observer's own percept.    
        return "self"

    if origin is getattr(npc, "sublocation", None):
        return "location"

    if getattr(npc, "current_interaction_target", None) is origin:
        return "interaction"


    return None