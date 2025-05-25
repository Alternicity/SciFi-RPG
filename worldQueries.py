

#location searches, filtering targets, etc.

def get_viable_robbery_targets(region):
    return [
        loc for loc in region.locations
        if getattr(loc, "robbable", False)
        and getattr(loc, "is_open", False)
        and not getattr(loc, "has_security", lambda: False)()
    ]