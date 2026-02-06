#world.placement.py
#no imports currently
def place_character(npc, location):
    # Set location
    
    npc.location = location
    npc.region = location.region

    # Location membership
    if npc not in location.characters_there:
        location.characters_there.append(npc)#already there

    # Region membership
    if npc not in location.region.characters_there:
        location.region.characters_there.append(npc)


