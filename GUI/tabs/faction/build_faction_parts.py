#GUI.tabs.faction.build_faction_parts.py
import tkinter
from tkinter import ttk

def build_faction_center(gui,parent):

    gui.faction_notebook = ttk.Notebook(parent)

    gui.faction_notebook.pack(
        fill="both",
        expand=True
    )

    overview_tab = ttk.Frame(gui.faction_notebook)
    characters_tab = ttk.Frame(gui.faction_notebook)
    hq_tab = ttk.Frame(gui.faction_notebook)
    connections_tab = ttk.Frame(gui.faction_notebook)
    goals_tab = ttk.Frame(gui.faction_notebook)
    culture_tab = ttk.Frame(gui.faction_notebook)

    gui.faction_notebook.add(
        overview_tab,
        text="Overview"
    )

    gui.faction_notebook.add(
        characters_tab,
        text="Characters"
    )

    gui.faction_notebook.add(
        hq_tab,
        text="HQ"
    )

    gui.faction_notebook.add(
        connections_tab,
        text="Connections"
    )

    gui.faction_notebook.add(
        goals_tab,
        text="Goals"
    )

    gui.faction_notebook.add(
        culture_tab,
        text="Culture"
    )
    from GUI.inspectors.faction.faction_characters_panel import build_faction_characters_panel
    from GUI.inspectors.faction.faction_hq_panel import build_faction_hq_panel
    from GUI.inspectors.faction.faction_overview_panel import (
        build_faction_overview_panel,
        refresh_faction_overview
    )
    #I will move these imports to the top when edits complete

    build_faction_overview_panel(
        gui,
        overview_tab
    )

    build_faction_characters_panel(
        gui,
        characters_tab
    )

    build_faction_hq_panel(
        gui,
        hq_tab
    )


def build_faction_details(gui,parent):

    gui.faction_detail_label=ttk.Label(
        parent,
        text="No selection",
        justify="left"
    )

    gui.faction_detail_label.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )