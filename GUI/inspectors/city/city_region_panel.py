#GUI.inspectors.city.city_region_panel.py
import tkinter as tk


def build_region_panel(gui, parent):

    gui.region_info_label = tk.Label(
        parent,
        text="Select a region",
        justify="left",
        anchor="nw"
    )

    gui.region_info_label.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

def refresh_region_panel(gui):

    region = gui.selected_region

    if not region:
        return

    #tmp, later populate in create npc functions with append
    resident_count = len(

    [

            c for c in gui.game_state.all_characters

            if (
                hasattr(c,"home")
                and c.home
                and c.home.region == region
            )

        ]
    )

    text = (
        f"Name: {region.name_for_player}\n"#still not outputting capitalised names
        f"Wealth: {region.wealth}\n"
        f"Locations: {len(region.locations)}\n"
        f"Residents: {resident_count}\n"
        f"Gangs: {len(region.region_gangs)}\n"
        f"Culture: {', '.join(region.cultural_adjectives)}\n"
    )

    gui.region_info_label.config(text=text)