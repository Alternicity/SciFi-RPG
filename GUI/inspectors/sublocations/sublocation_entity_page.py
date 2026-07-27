#GUI.inspectors.sublocations.sublocation_entity_page.py
from GUI.inspectors.npc.sublocation_inspector import build_sublocation_inspector

def build_sublocation_entity_page(gui, parent, observer, sublocation):

    return build_sublocation_inspector(
        gui,
        parent,
        observer,
        sublocation
    )#Behaviour unchanged. Later move the code.
