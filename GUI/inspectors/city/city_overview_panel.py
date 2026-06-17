#GUI.inspectors.city.city_overview_panel.py
from tkinter import ttk

def build_city_overview(gui,parent):

    frame = ttk.LabelFrame(
        parent,
        text="City Overview"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    gui.city_labels={}

    fields = [

        "City",
        "Regions",
        "Population",
        "Civilians",
        "Families",
        "Corporations",
        "Gangs",
        "Homeless"
    ]
    for field in fields:

        row = ttk.Frame(frame)
        row.pack(fill="x", padx=5, pady=2)

        ttk.Label(
            row,
            text=f"{field}:",
            width=15
        ).pack(side="left")

        value = ttk.Label(
            row,
            text="-"
        )

        value.pack(side="left")

        gui.city_labels[field] = value

def refresh_city_overview(gui):

    gs=gui.game_state

    values={

        "City":"Ember City",
        "Regions":len(gs.all_regions),
        "Population":len(gs.all_characters),
        "Civilians":len(gs.civilians),
        "Families":len(gs.families),
        "Corporations":len(gs.corporations),
        "Gangs":len(gs.gangs),
        "Homeless":len(gs.homeless),
    }

    for field, value in values.items():

        if field in gui.city_labels:

            gui.city_labels[field].config(
                text=str(value)
            )