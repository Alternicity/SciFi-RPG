#display.aggregate_display_buckets.py

from objects.furniture import CafeTable, CafeChair

def collect_display_buckets(npc):
    """
    Collects and aggregates percept objects into
    structured display buckets.

    Returns:
        {
            "normal_rows": [],
            "occupied_tables": [],
            "empty_tables": [],
            # future: gangs, food stacks, weapons, etc.
        }
    """

    buckets = {
        "normal_rows": [],
        "occupied_tables": [],
        "empty_tables": [],
    }

    for key, v in npc.percepts.items():

        data = v.get("data", {})
        origin = v.get("origin") or data.get("origin")

        if origin is None:
            continue

        # Suppress chairs entirely
        if isinstance(origin, CafeChair):
            continue

        # Tables get bucketed
        if isinstance(origin, CafeTable):
            if origin.occupants:
                buckets["occupied_tables"].append(origin)
            else:
                buckets["empty_tables"].append(origin)
            continue

        # Everything else passes through untouched
        buckets["normal_rows"].append((origin, data, v))

    return buckets
