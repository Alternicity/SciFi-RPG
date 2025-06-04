# npc_actions.py
def visit_location_auto(character, location):
    if location is None:
        return False

    print(f"[AUTO VISIT] {character.name} is going to {location.name}")
    character.location = location
    location.enter(character) #enter does not exist, this may be cruft

    return True

def steal_auto():
    print (f"npc steal called")

def rob_auto(npc, region=None, location=None, **kwargs):
    pass
    #print (f"npc rob called")

def exit_location_auto():
    print (f"npc exit location called")

def eat_auto():
    pass
    print (f"npc eat called")

def idle_auto(npc, region=None, **kwargs):
    pass
    #print (f"npc idle called")