#economy.economy_queries.workforce_queries.py
def get_active_workers(entity):

    active = []

    owned_locations = getattr(
        entity,
        "owned_locations",
        []
    )

    for location in owned_locations:

        workers = getattr(
            location,
            "employees_there",
            []
        )

        active.extend(workers)

    return active
