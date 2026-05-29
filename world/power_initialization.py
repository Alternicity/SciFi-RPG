#world.power_initialization.py

#Add appropriately configured power components to locations here

from location.locations import Powerplant, Park ,VacantLot
from world.scenarios.economy.economy_logging import economy_log
from location_components.power_components import PowerComponent

def setup_normal_power(all_regions):
    """ setup_normal_power() should ONLY:
    attach components
    wire suppliers
    NOT decide operational state """

    economy_log("[POWER INIT] Setting up power components")

    for region in all_regions:

        plant = None

        # Attach components + locate plant
        for loc in region.locations:

            if loc.power_component is None:
                loc.power_component = PowerComponent()

            if isinstance(loc, Powerplant):
                plant = loc

        if not plant:
            economy_log(
                f"[POWER INIT] No powerplant in {region.name}"
            )
            continue

        # Wire consumers
        for loc in region.locations:

            power = loc.power_component

            if isinstance(loc, (Park, VacantLot)):
                power.requires_power = False
                power.power_supplier = None
                continue

            if loc is plant:
                power.generates_power = True
                power.requires_power = False
                continue

            power.requires_power = True
            power.power_supplier = plant

            """ economy_log(
                f"[POWER LINK] {loc.name} -> {plant.name}"
            ) """

