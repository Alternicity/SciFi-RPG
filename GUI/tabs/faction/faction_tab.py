#GUI.tabs.faction.faction_tab.py

import tkinter as tk
from tkinter import ttk
from GUI.tabs.faction.build_faction_parts import build_faction_center, build_faction_details
from GUI.inspectors.faction.faction_overview_panel import build_faction_selector
from GUI.inspectors.faction.faction_hq_panel import (
    build_faction_hq_panel,
    refresh_faction_hq_panel
)

def create_faction_tab(gui, parent):

    main_frame = ttk.Frame(parent)
    main_frame.pack(
        fill="both",
        expand=True
    )

    left_frame = ttk.Frame(
        main_frame,
        width=250
    )

    center_frame = ttk.Frame(
        main_frame
    )

    right_frame = ttk.Frame(
        main_frame,
        width=250
    )

    left_frame.pack(
        side="left",
        fill="y"
    )

    center_frame.pack(
        side="left",
        fill="both",
        expand=True
    )

    right_frame.pack(
        side="right",
        fill="y"
    )

    left_frame.pack_propagate(False)
    right_frame.pack_propagate(False)
    

    build_faction_selector(
        gui,
        left_frame
    )

    build_faction_center(
        gui,
        center_frame
    )

    build_faction_details(
        gui,
        right_frame
    )

