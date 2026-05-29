#economy.economy_queries.economy_snapshot.py

from economy.economy_queries.location_queries import (
    get_location_economy_data
)

from create.create_game_state import get_game_state
from world.scenarios.economy.economy_logging import economy_log


def economy_snapshot_tick_1():

    game_state = get_game_state()

    important_types = (
        "Factory",
        "Powerplant",
        "Shop",
        "Cafe",
    )

    economy_log("")
    economy_log("=== ECONOMY SNAPSHOT ===")

    for location in game_state.all_locations:

        data = get_location_economy_data(location)

        if data["location_type"] not in important_types:
            continue

        if data["is_generator"]:

            if (
                data["employees"] == 0
                and not data["generating"]
            ):
                continue

        else:

            if (
                data["employees"] == 0
                and not data["resources"]
                and not data["requires_power"]
            ):
                continue

        economy_log(
            f"[LOCATION] "
            f"{location.region.name}:"
            f"{location.name}"
        )

        economy_log(
            f"  Type: {data['location_type']}"
        )

        economy_log(
            f"  Owner: {data['owner']}"
        )

        if data["is_generator"]:

            economy_log(
                f"  Generating: {data['generating']}"
            )

            economy_log(
                f"  Consumers: {len(data['consumers'])}"
            )

        else:

            economy_log(
                f"  Powered: {data['powered']}"
            )

            economy_log(
                f"  Supplier: {data['supplier']}"
            )

        economy_log(
            f"  Employees: {data['employees']}"
        )

        economy_log(
            f"  Resources: {data['resources']}"
        )