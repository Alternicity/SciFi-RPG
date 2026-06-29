#GUI.inspectors.percepts.percept_grouping.py
from base.location import Sublocation
from objects.furniture import CafeTable, CafeChair

def build_percept_sections(npc):
    regular_rows = []
    sublocation_rows = []
    parent_location_rows = []

    current_sublocation = getattr(
        npc,
        "sublocation",
        None
    )

    parent_location = getattr(
        current_sublocation,
        "parent_location",
        None
    )

    

    for key, v in npc.percepts.items():

        origin = v.get("origin")
        data = v.get("data", {})


        if origin is None:
            continue

        if isinstance(origin, CafeChair):
            continue

        if isinstance(origin, CafeTable):
            continue

        if isinstance(origin, Sublocation):

            sublocation_rows.append(
                (origin, data, v)
            )

        elif belongs_to_sublocation(
            origin,
            current_sublocation
        ):

            regular_rows.append(
                (origin, data, v)
            )

        #new
        elif origin is parent_location:

            parent_location_rows.append(
                (origin, data, v)
            )

        elif belongs_to_location(
            origin,
            parent_location
        ):

            parent_location_rows.append(
                (origin, data, v)
            )

        else:

            regular_rows.append(
                (origin, data, v)
            )

    print(
        "From build_percept_sections SUBLOCATION COUNT:",
        len(sublocation_rows)
    )

    print(
        "from build_percept_sections SUBLOCATIONS:",
        [
            getattr(origin, "name", str(origin))
            for origin, data, v in sublocation_rows
        ]
    )




    return {
        "regular": regular_rows,
        "sublocations": sublocation_rows,
        "parent_location": parent_location_rows,#updated
    }

#utility functions
def belongs_to_sublocation(obj, sublocation):

    if sublocation is None:
        return False

    if obj in sublocation.objects_present:
        return True

    if obj in getattr(
        sublocation,
        "characters_there",
        []
    ):
        return True

    return False

def belongs_to_location(obj, location):

    if location is None:
        return False

    if obj in location.objects_present:
        return True

    if obj in getattr(
        location,
        "characters_there",
        []
    ):
        return True

    return False