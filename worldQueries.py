#worldQueries.py

#location searches, filtering targets, etc.

def get_viable_robbery_targets(region):
    return [
        loc for loc in region.locations
        if getattr(loc, "robbable", False)
        and getattr(loc, "is_open", False)
        and not getattr(loc, "has_security", lambda: False)()
    ]

def get_nearby_objects(npc, region=None, location=None):
    nearby = []

    if location:
        # All characters at same location, except self
        nearby.extend([c for c in location.characters_there if c is not npc])

        # Objects at location
        if hasattr(location, "inventory"):
            nearby.extend(location.inventory.items)

        # Static structures like cash register, shop structure
        if hasattr(location, "cash_register"):
            nearby.append(location.cash_register)

        # Add location itself if needed (e.g. a perceptible building)
        nearby.append(location)

    return nearby