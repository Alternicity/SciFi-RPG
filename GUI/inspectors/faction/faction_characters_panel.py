#GUI.inspectors.faction.faction_characters_panel.py

from tkinter import ttk


def build_faction_characters_panel(gui,parent):

    gui.faction_characters_text = ttk.Label(
        parent,
        text="No faction selected",
        justify="left",
        anchor="nw"
    )

    gui.faction_characters_text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


def refresh_faction_characters(gui):

    faction = gui.selected_faction

    if not faction:
        return


    lines=[]


    if hasattr(faction,"boss") and faction.boss:

        lines.append(
            f"Boss: {faction.boss.name}"
        )


    if hasattr(faction,"CEO") and faction.CEO:

        lines.append(
            f"CEO: {faction.CEO.name}"
        )


    for captain in getattr(
        faction,
        "captains",
        []
    ):

        lines.append(
            f"Captain: {captain.name}"
        )


    for manager in getattr(
        faction,
        "managers",
        []
    ):

        lines.append(
            f"Manager: {manager.name}"
        )


    for member in getattr(
        faction,
        "members",
        []
    ):

        lines.append(
            f"Member: {member.name}"
        )


    if not lines:

        lines.append(
            "No characters"
        )


    gui.faction_characters_text.config(
        text="\n".join(lines)
    )