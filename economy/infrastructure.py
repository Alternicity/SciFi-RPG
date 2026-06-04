#economy.infrastructure.py
from world.scenarios.economy.economy_logging import economy_log
from location.locations import Powerplant
from create.create_game_state import get_game_state
game_state = get_game_state()

def update_infrastructure():

    update_power_grid()


def update_power_grid():

    for plant in game_state.all_powerplants:

        print(
            plant.name,
            len(plant.employees_there),
            plant.power_component.is_generating
        )

        plant.power_component.is_generating = (
            len(plant.employees_there) >= 2
        )

        #verbose
        """ print(
            "AFTER:",
            plant.name,
            plant.power_component.is_generating
        ) """

        """ economy_log(
            f"[POWERPLANT] "
            f"{plant.region.name}:{plant.name} "
            f"generating={plant.power_component.is_generating}"
        ) """

    for location in game_state.all_locations:

        power = getattr(location, "power_component", None)

        if not power:
            continue

        if not power.requires_power:
            continue

        supplier = power.power_supplier

        if supplier is None:

            power.has_power = False

            economy_log(
                f"[UNPOWERED] "
                f"{location.region.name}:{location.name}"
            )

            continue

        supplier_power = getattr(
            supplier,
            "power_component",
            None
        )

        power.has_power = (
            supplier_power is not None
            and supplier_power.is_generating
        )

        """ economy_log(
            f"[POWER LINK] "
            f"{location.region.name}:{location.name} "
            f"-> "
            f"{supplier.name}"
        ) """

        """ economy_log(
            f"[POWER STATUS] "
            f"{location.name} powered={location.is_powered}"
        ) """