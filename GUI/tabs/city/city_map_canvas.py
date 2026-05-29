#GUI.tabs.city.city_map_canvas.py

import tkinter as tk

MAP_OFFSET_X = 50
MAP_OFFSET_Y = 75

REGION_LAYOUT = {

    "northville": (250, 50, 450, 150),
    "westborough": (50, 200, 250, 300),
    "downtown": (250, 200, 450, 300),
    "easternhole": (450, 200, 650, 300),
    "southville": (250, 350, 450, 450),

}

def build_city_map_canvas(gui, center_frame):
    print("BUILD CITY MAP CANVAS")
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

    gui.map_canvas = canvas
    gui.region_rectangles = {}

    regions = gui.game_state.all_regions

    for region in regions:

        coords = REGION_LAYOUT.get(region.name)

        if not coords:
            continue

        x1, y1, x2, y2 = coords

        x1 += MAP_OFFSET_X
        x2 += MAP_OFFSET_X

        y1 += MAP_OFFSET_Y
        y2 += MAP_OFFSET_Y

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
            fill="white"
        )

        # Single click = inspect region
        canvas.tag_bind(

            rect_id,

            "<Button-1>",

            lambda e, r=region:
                gui.on_region_select(r)
        )

        canvas.tag_bind(

            text_id,

            "<Button-1>",

            lambda e, r=region:
                gui.on_region_select(r)
        )

        # Double click = open region
        canvas.tag_bind(

            rect_id,

            "<Double-Button-1>",

            lambda e, r=region:
                gui.open_region(r)
        )

        canvas.tag_bind(

            text_id,

            "<Double-Button-1>",

            lambda e, r=region:
                gui.open_region(r)
        )

        gui.region_rectangles[region.id] = rect_id

