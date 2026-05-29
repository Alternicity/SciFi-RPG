#GUI.tabs.faction.build_faction_parts.py
import tkinter
from tkinter import ttk
from GUI.inspectors.faction.faction_economy_panel import (
    build_faction_economy_panel
)
def build_faction_center(gui,parent):

    gui.faction_notebook = ttk.Notebook(parent)

    gui.faction_notebook.pack(
        fill="both",
        expand=True
    )

    overview_tab = ttk.Frame(gui.faction_notebook)
    characters_tab = ttk.Frame(gui.faction_notebook)
    hq_tab = ttk.Frame(gui.faction_notebook)

    economy_tab = ttk.Frame(gui.faction_notebook)#this is where we paused gui dev beofre and began the economy pass
    
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
        economy_tab,
        text="economy"
    )

    gui.faction_notebook.add(
        goals_tab,
        text="Goals"
    )

    gui.faction_notebook.add(
        culture_tab,
        text="Culture"
    )
    #it seems odd that these imports are here
    from GUI.inspectors.faction.faction_characters_panel import build_faction_characters_panel
    from GUI.inspectors.faction.faction_hq_panel import build_faction_hq_panel
    from GUI.inspectors.faction.faction_overview_panel import (
        build_faction_overview_panel,
        refresh_faction_overview#not accessesd
    )
    
    #I added this code here, should it have been in Correct build_faction_mode instead?
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
    build_faction_economy_panel(
        gui,
        economy_tab
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