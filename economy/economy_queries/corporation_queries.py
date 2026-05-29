#economy.economy_queries.corporation_queries.py

from location.locations import Factory, Powerplant

def get_corporation_economy_data(corp):

    owned = getattr(corp, "owned_locations", [])

    factories = [
        loc for loc in owned
        if isinstance(loc, Factory)
    ]

    powerplants = [
        loc for loc in owned
        if isinstance(loc, Powerplant)
    ]

    operational_powerplants = [
        p for p in powerplants
        if (
            hasattr(p, "power_component")
            and p.power_component
            and p.power_component.is_generating
        )
    ]

    operational_factories = [
        f for f in factories
        if (
            hasattr(f, "power_component")
            and f.power_component
            and f.power_component.has_power
        )
    ]

    return {

        "owned_locations":
            len(owned),

        "factories":
            len(factories),

        "powerplants":
            len(powerplants),

        "assigned_workers":
            len([
                npc for npc in getattr(corp, "employees", [])
                if (
                    hasattr(npc, "employment")
                    and npc.employment
                    and npc.employment.workplace is not None
                )
            ]),

        "available_workers":
            len(getattr(corp, "available_workers", [])),

        "operational_powerplants":
            len(operational_powerplants),

        "operational_factories":
            len(operational_factories),
    }