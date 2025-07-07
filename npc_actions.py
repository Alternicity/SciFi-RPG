# npc_actions.py
def visit_location_auto(character, region, location):
    if location is None:
        return False
    print(f"[AUTO VISIT] {character.name} is going to {location.name}")
    character.location = location
    return True

def steal_auto(character, region):
    print(f"[STEAL] {character.name} tries to steal something at {character.location.name}")
    # Logic for: success chance, item taken, consequences


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

#explore
    """ if not percepts and not promoted_actions:
            unexplored = [l for l in region.locations if l.name != self.npc.location.name]
            if unexplored:
                next_loc = random.choice(unexplored)
                print(f"[EXPLORE] {self.npc.name} wandering to {next_loc.name}")
                return {
                    "name": "visit_location",
                    "params": {"location": next_loc}
                } """
    

