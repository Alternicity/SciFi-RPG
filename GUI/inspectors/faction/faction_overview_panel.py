#GUI.inspectors.faction.faction_overview_panel.py
import tkinter as tk
from tkinter import ttk

def refresh_faction_list(gui):

    gui.faction_listbox.delete(
        0,
        "end"
    )

    selected_type = (
        gui.faction_type_var.get()
    )

    factions=[]

    if selected_type=="Gangs":

        factions=gui.game_state.gangs

    elif selected_type=="Corporations":

        factions=gui.game_state.corporations

    elif selected_type=="State":

        if gui.game_state.state:

            factions=[
                gui.game_state.state
            ]

    gui.faction_lookup={}

    for faction in factions:

        name=getattr(
            faction,
            "name",
            "Unknown"
        )

        gui.faction_listbox.insert(
            "end",
            name
        )

        gui.faction_lookup[
            name
        ]=faction

def build_faction_selector(gui,parent):

    ttk.Label(
        parent,
        text="Faction Type"
    ).pack(
        pady=(10,5)
    )

    gui.faction_type_var = ttk.Combobox(
        parent,
        values=[
            "Gangs",
            "Corporations",
            "State"
        ],
        state="readonly"
    )

    gui.faction_type_var.pack(
        fill="x",
        padx=10
    )

    gui.faction_type_var.set(
        "Gangs"
    )

    gui.faction_type_var.bind(
        "<<ComboboxSelected>>",
        gui.on_faction_type_change
    )

    gui.faction_listbox = tk.Listbox(
        parent
    )

    gui.faction_listbox.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    gui.faction_listbox.bind(
        "<<ListboxSelect>>",
        gui.on_faction_select
    )

    refresh_faction_list(
        gui
    )

def build_faction_overview_panel(gui, parent):

    gui.faction_overview_text = ttk.Label(
        parent,
        text="Select a faction",
        justify="left",
        anchor="nw"
    )

    gui.faction_overview_text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


def refresh_faction_overview(gui):

    faction = gui.selected_faction

    if not faction:
        return


    text = (

        f"Name: {faction.name}\n"
        f"Type: {faction.type}\n"
        f"Violence: "
        f"{getattr(faction,'violence_disposition','N/A')}\n"

        f"Members: "
        f"{len(getattr(faction,'members',[]))}\n"

        f"HQ: "
        f"{faction.HQ.name if getattr(faction,'HQ',None) else 'None'}"

    )

    gui.faction_overview_text.config(
        text=text
    )