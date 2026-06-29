#GUI.helpers.formatting.py

def is_highlighted_percept(origin, npc):

    if origin is npc:
        print("HIGHLIGHT: ME", origin.name)
        #return True
        return "self"

    if origin is getattr(npc, "sublocation", None):
        print("HIGHLIGHT: CURRENT ROOM", origin.name)#not showing up, see SUBLOCATION TAG print
        return "location"

    if getattr(npc, "current_interaction_target", None) is origin:
        print("HIGHLIGHT: TALKING TO", origin.name)
        return "interaction"

    #return False
    return None