#GUI.inspectors.city.location_panel.py
from location.locations import Nightclub
from economy.economy_queries.nightclub_queries import get_nightclub_economy_data
from tkinter import ttk
from base.faction import Faction

from economy.economy_queries.location_queries import (
    get_location_economy_data
)
from GUI.navigation.breadcrumbs import build_city_breadcrumbs

def build_location_view(gui, parent, location):
    from economy.economy_queries.location_queries import get_location_owner
    build_city_breadcrumbs(gui, parent)

    title = ttk.Label(
        parent,
        text=f"{location.name}",
        font=("Arial", 14, "bold")
    )

    title.pack(pady=10)

    econ = get_location_economy_data(location)

    controlling_text = ""#controlling_text not accessed

    owner = get_location_owner(location)


    #tmp debug block
    owner = get_location_owner(location)

    print(
        "[LOCATION DEBUG]",
        location.name,
        "owner=",
        getattr(owner, "name", None)
    )



    if isinstance(owner, Faction):

        controlling_text = (#controlling_text not accessed
            f"Controlling Faction: "
            f"{owner.name}"
        )

    if econ["is_generator"]:

        economy_text = f"""
    Economy:
    Generating: {econ['generating']}
    Consumers: {len(econ['consumers'])}
    Employees: {econ['employees']}
    Owner: {econ['owner']}
    """

    else:

        economy_text = f"""
    Economy:
    Powered: {econ['powered']}
    Supplier: {econ['supplier']}
    Employees: {econ['employees']}
    Owner: {econ['owner']}
    Resources: {econ['resources']}
    """
    
    owner = get_location_owner(location)
    lines = [
        f"Owner: {getattr(owner, 'name', None)}"
    ]

    owner = get_location_owner(location)
    if isinstance(owner, Faction):

        lines.append(
            f"Controlling Faction: {owner.name}"
        )

    lines.extend([
        f"Condition: {location.condition}",
        f"Base Fun: {location.fun}",
        f"Open: {location.is_open}",
        f"Tags: {location.tags}",
        "",
        economy_text.strip()
    ])

    if isinstance(location, Nightclub):

        club_data = get_nightclub_economy_data(location)

        lines.extend([
            "",
            "Nightclub:",
            f"Bartenders: {club_data['bartenders']}",
            f"Bouncers: {club_data['bouncers']}",
            f"DJs: {club_data['djs']}",
            f"Managers: {club_data['managers']}",
            f"Security: {club_data['security_level']}",
            f"Fun Rating: {club_data['fun']}",
        ])

    info_text = "\n".join(lines)
        
    info = ttk.Label(
        parent,
        text=info_text,
        justify="left"
    )

    info.pack(
        anchor="w",
        padx=10
    )