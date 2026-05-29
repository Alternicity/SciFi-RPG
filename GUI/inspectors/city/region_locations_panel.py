#GUI.inspectors.city.region_locations_panel.py

from tkinter import ttk
from GUI.navigation.breadcrumbs import build_city_breadcrumbs
def build_region_locations_view(gui, parent, region):
    build_city_breadcrumbs(gui, parent)
    title = ttk.Label(
        parent,
        text=f"{region.name} Locations",
        font=("Arial", 14, "bold")
    )

    title.pack(pady=10)

    grid_frame = ttk.Frame(parent)
    grid_frame.pack(expand=True)

    columns = 3
    for col in range(columns):
        grid_frame.grid_columnconfigure(col, weight=1)

    for i, location in enumerate(region.locations):

        row = i // columns
        col = i % columns

        link = ttk.Label(
            grid_frame,
            text=location.name,
            foreground="blue",
            cursor="hand2"
        )

        link.bind(
            "<Button-1>",
            lambda e, l=location: gui.open_location(l)
        )

        link.grid(
            row=row,
            column=col,
            padx=20,
            pady=12
        )

    ttk.Button(
        parent,
        text="← Back to City Map",
        command=gui.reset_city_navigation
    ).pack(anchor="w", padx=10, pady=5)

