#ambience.ambience_and_psy_utils.py

def compute_location_ambience(location, observer=None):
    """
    Blends ambience contributions from all objects in the location.
    Optionally filters based on observer psy.
    """
    from ambience.ambience import Ambience

    total_ambience = Ambience()

    for obj in getattr(location, "objects_present", []):
        if hasattr(obj, "modulated_ambience"):
            ambient_effect = obj.modulated_ambience()
            total_ambience.blend(Ambience(ambient_effect))

    if observer:
        return total_ambience.absorb(observer)  # Perceived ambience, filtered by psy
    return total_ambience.vibes  # Raw environmental ambience
