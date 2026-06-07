#GUI.inspectors.percepts.percept_grouping.py
from base.location import Sublocation
from objects.furniture import CafeTable, CafeChair

def build_percept_sections(npc):
    regular_rows = []
    sublocation_rows = []

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
    }