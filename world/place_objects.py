# world.place_objects.py

from base.location import Sublocation

def place_object(obj, destination):
    """
    Place any ObjectInWorld into either a Location or a Sublocation.
    """

    obj.region = destination.region

    if isinstance(destination, Sublocation):
        obj.location = destination.parent_location
        obj.sublocation = destination
    else:
        obj.location = destination
        obj.sublocation = None

    destination.items.objects_present.append(obj)

    return obj