#GUI.tabs.city.city_map_tab.py
import tkinter as tk

from GUI.inspectors.city.city_region_panel import (
    build_region_panel,
)
from GUI.inspectors.city.city_overview_panel import refresh_city_overview

MAP_OFFSET_X = 50
MAP_OFFSET_Y = 75


REGION_LAYOUT = {
    "northville": (250, 50, 450, 150),
    "westborough": (50, 200, 250, 300),
    "downtown": (250, 200, 450, 300),
    "easternhole": (450, 200, 650, 300),
    "southville": (250, 350, 450, 450),
}



def create_city_map_tab(gui, parent):

    main_frame = tk.Frame(parent)
    main_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(
        main_frame,
        width=250
    )

    center_frame = tk.Frame(
        main_frame
    )

    right_frame = tk.Frame(
        main_frame,
        width=300
    )

    canvas = tk.Canvas(
        center_frame,
        width=700,
        height=600,
        bg="black"
    )

    canvas.pack(
        fill="both",
        expand=True
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

    #I am unsure if this goes here:
    from GUI.inspectors.city.city_overview_panel import build_city_overview
    build_city_overview(
        gui,
        left_frame
    )
    refresh_city_overview(gui)


    build_region_panel(gui, right_frame)

    regions = gui.game_state.all_regions
    gui.region_rectangles = {}

    for region in regions:

        coords = REGION_LAYOUT.get(region.name)

        if not coords:
            continue

        x1, y1, x2, y2 = coords

        x1 += MAP_OFFSET_X
        x2 += MAP_OFFSET_X

        y1 += MAP_OFFSET_Y
        y2 += MAP_OFFSET_Y

        #selected region/unselected region border width setting here?

        rect_id = canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="gray20",
            outline="white",
            width=2
        )

        text_id = canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text=region.name,
            fill="White"
        )

        canvas.tag_bind(
            rect_id,
            "<Button-1>",
            lambda e, r=region: gui.on_region_select(r)
        )
        #Does this now deprecate any of the above?
        gui.region_rectangles[region.id] = rect_id
    

        canvas.tag_bind(
            text_id,
            "<Button-1>",
            lambda e, r=region: gui.on_region_select(r)
        )
        gui.map_canvas = canvas
        