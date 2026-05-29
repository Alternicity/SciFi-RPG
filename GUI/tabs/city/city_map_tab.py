#GUI.tabs.city.city_map_tab.py
import tkinter as tk
from tkinter import ttk
from GUI.inspectors.city.city_region_panel import (
    build_region_panel,
)

from GUI.inspectors.city.city_region_panel import (
    build_region_panel,
)

from GUI.inspectors.city.city_overview_panel import (
    build_city_overview,
)

#ONLY: canvas, region rectangles, bindings, rendering

def create_city_map_tab(gui, parent):

    main_frame = tk.Frame(parent)

    main_frame.pack(
        fill="both",
        expand=True
    )

    # LEFT PANEL
    left_frame = tk.Frame(
        main_frame,
        width=250
    )

    left_frame.pack(
        side="left",
        fill="y"
    )

    left_frame.pack_propagate(False)

    # CENTER PANEL, possible ordering issue
    center_frame = tk.Frame(main_frame)
    
    center_frame.pack(
        side="left",
        fill="both",
        expand=True
    )

    gui.city_center_frame = center_frame

    # RIGHT PANEL
    right_frame = tk.Frame(
        main_frame,
        width=300
    )

    right_frame = ttk.LabelFrame(
        main_frame,
        text="Region Details",
        width=300
    )

    right_frame.pack(
        side="right",
        fill="y",
        padx=10,
        pady=10
    )

    right_frame.pack_propagate(False)

    # LEFT PANEL CONTENT
    build_city_overview(
        gui,
        left_frame
    )

    # RIGHT PANEL CONTENT
    build_region_panel(
        gui,
        right_frame
    )

    # CENTER PANEL CONTENT
    from GUI.tabs.city.city_map_canvas import (
        build_city_map_canvas
    )

    build_city_map_canvas(
        gui,
        center_frame
    )
    
