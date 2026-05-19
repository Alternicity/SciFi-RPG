#GUI.inspectors.faction.faction_hq_panel.py


import tkinter as tk


def build_faction_hq_panel(gui, parent):

    gui.faction_hq_text = tk.Label(
        parent,
        text="No faction selected",
        justify="left",
        anchor="nw"
    )

    gui.faction_hq_text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


def refresh_faction_hq_panel(gui):
    from faction import State
    faction = gui.active_context["faction"]

    if not faction:

        gui.faction_hq_text.config(
            text="No faction selected"
        )

        return

    if isinstance(faction, State):

        buildings = faction.government_buildings#depends on either class faction, or class State have government_buildings populated

        if not buildings:
            text = "No government buildings"

        else:

            lines = ["Government Buildings\n"]

            for building in buildings:

                region_name = getattr(
                    building.region,
                    "name",
                    "Unknown"
                )

                lines.append(
                    f"{region_name}: {building.name}"
                )

            text = "\n".join(lines)

        gui.faction_hq_text.config(text=text)

        return

    hq = getattr(
        faction,
        "HQ",
        None
    )

    if not hq:

        if getattr(
            faction,
            "is_street_gang",
            False
        ):

            start_location = getattr(
                faction,
                "street_gang_start_location",
                None
            )

            location_name = (
                start_location.name
                if start_location
                else "Unknown"
            )

            text = (

                "Street Gang\n\n"
                "No permanent headquarters\n\n"
                f"Current Base: {location_name}"

            )

        else:

            text = "No HQ"

    else:

        security = hq.security

        features = ", ".join(
            hq.special_features
        )

        if not features:
            features = "None"

        inventory_count = len(
            hq.inventory.items
        )

        text = (

            f"Name: {hq.name}\n"
            f"Description: {hq.description}\n\n"

            f"Open: {hq.is_open}\n"
            f"Powered: {hq.is_powered}\n"
            f"Energy Cost: {hq.energy_cost}\n\n"

            f"Security Level: {security.level}\n"
            f"Guards: {len(security.guards)}\n"
            f"Surveillance: {security.surveillance}\n"
            f"Alarm System: {security.alarm_system}\n\n"

            f"Inventory Items: {inventory_count}\n"
            f"Resources: {len(hq.resource_storage)}\n"
            f"Features: {features}"

        )


    gui.faction_hq_text.config(
        text=text
    )