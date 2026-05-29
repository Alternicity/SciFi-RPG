#economy.economy_queries.location_queries.py

from location.locations import Powerplant


def get_location_economy_data(location):
    #might need updating if an owner can be an npc
    power_component = getattr(
        location,
        "power_component",
        None
    )

    supplier = None

    if power_component:
        supplier = power_component.power_supplier

    is_generator = isinstance(location, Powerplant)

    data = {

        "owner": (
            location.owner.name
            if getattr(location, "owner", None)
            else None
        ),

        "employees": len(
            getattr(
                location,
                "employees_there",
                []
            )
        ),

        "resources": getattr(
            location,
            "resources",
            {}
        ),

        "location_type": type(location).__name__,

        "is_generator": is_generator,
    }

    if is_generator:

        consumers = []

        for loc in getattr(location.region, "locations", []):

            loc_power = getattr(loc, "power_component", None)

            if (
                loc_power
                and loc_power.power_supplier == location
            ):
                consumers.append(loc.name)

        data.update({

            "generating": (
                power_component.is_generating
                if power_component
                else False
            ),

            "consumers": consumers,
        })

    else:

        data.update({

            "powered": (
                power_component.has_power#has_power?
                if power_component
                else False
            ),

            "requires_power": (
                power_component.requires_power
                if power_component
                else False
            ),

            "supplier": (
                supplier.name
                if supplier
                else None
            ),
        })

    return data