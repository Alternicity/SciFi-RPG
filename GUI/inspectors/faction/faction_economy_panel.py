#GUI.inspectors.faction.faction_economy_panel.py

from tkinter import ttk

def build_faction_economy_panel(gui, parent):

    gui.faction_economy_text = ttk.Label(
        parent,
        text="No economy data",
        justify="left",
        anchor="nw"
    )

    gui.faction_economy_text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

from economy.economy_queries.corporation_queries import (
    get_corporation_economy_data
)

def refresh_faction_economy_panel(gui):

    faction = gui.active_context.get("faction")

    if not faction:
        return

    data = get_corporation_economy_data(faction)

    text = (
        f"Owned Locations: {data['owned_locations']}\n"#one output
        f"Factories: {data['factories']}\n"
        f"Powerplants: {data['powerplants']}\n\n"

        f"Workers Assigned: {data['assigned_workers']}\n"
        f"Workers Available: {data['available_workers']}\n\n"

        f"Operational Powerplants: "
        f"{data['operational_powerplants']}\n"

        f"Operational Factories: "
        f"{data['operational_factories']}\n"
    )

    gui.faction_economy_text.config(
        text=text
    )