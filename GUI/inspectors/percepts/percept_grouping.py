#GUI.inspectors.percepts.percept_grouping.py
from base.location import Sublocation
from base.location import Location
#utility functions
def build_percept_sections(npc):
    regular_rows = []
    sublocation_rows = []
    parent_location_rows = []#ie Nightclub is the parent location of VIP Lounge, Gang HQ is the parent location of Boss Office
    location_rows = []

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

    for key, v in npc.percepts.items():#key is not accessed

        origin = v.get("origin")
        data = v.get("data", {})

        if origin is None:
            continue

        if isinstance(origin, Sublocation):

            sublocation_rows.append(
                (origin, data, v)
            )

        elif (
                isinstance(origin, Location)
                and not isinstance(origin, Sublocation)
            ):
                location_rows.append((origin, data, v))

        elif getattr(origin, "sublocation", None) is current_sublocation:

            regular_rows.append(
                (origin, data, v)
            )

        elif origin is parent_location:

            parent_location_rows.append(
                (origin, data, v)
            )

        elif getattr(origin, "location", None) is parent_location:

            parent_location_rows.append(
                (origin, data, v)
            )

        else:

            regular_rows.append(
                (origin, data, v)
            )

    return {
        "location": location_rows,
        "regular": regular_rows,
        "sublocations": sublocation_rows,
        "parent_location": parent_location_rows,
    }



