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

def place_character_in_sublocation(
    npc,
    parent_location,
    sublocation
):

    npc.location = parent_location
    npc.sublocation = sublocation
    npc.region = parent_location.region

    print(
        npc.name,
        npc.__class__.__name__,
        getattr(npc, "debug_role", None),
        sublocation.accessible_roles
    )

    if npc not in sublocation.characters_there:
        sublocation.characters_there.append(npc)

    if npc not in parent_location.characters_there:
        parent_location.characters_there.append(npc)

    if npc not in npc.region.characters_there:
        npc.region.characters_there.append(npc)
