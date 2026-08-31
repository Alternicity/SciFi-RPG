# world.place_objects.py

from base.location import Sublocation
from objects.furniture import Furniture

def place_object(obj, destination):
    if obj is None:
        raise ValueError("place_object(): obj is None")
    if destination is None:
        raise ValueError("place_object(): destination is None")

    if isinstance(destination, Furniture):

        obj.region = destination.region
        obj.location = destination.location
        obj.sublocation = destination.sublocation

        destination.add_to_surface(obj)

        return obj

    elif isinstance(destination, Sublocation):

        obj.region = destination.region
        obj.location = destination.parent_location
        obj.sublocation = destination

        destination.items.objects_present.append(obj)

        return obj

    else:   # Location

        obj.region = destination.region
        obj.location = destination
        obj.sublocation = None

        destination.items.objects_present.append(obj)

        return obj