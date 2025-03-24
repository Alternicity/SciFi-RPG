def get_visitable_locations(region):
    from characterActions import visit_location
    """Returns a dictionary of visitable locations in a region."""
    if not region.locations:
        print("No visitable locations in this region.")
        return {}  # Return empty dict if there are no locations

    return {
        idx + 1: (location.name, lambda: location)
        for idx, location in enumerate(region.locations)
    } #Does this return "locations"
