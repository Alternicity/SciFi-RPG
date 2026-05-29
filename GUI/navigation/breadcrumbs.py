#GUI.navigation.breadcrumbs.py
import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk


def build_city_breadcrumbs(gui, parent):

    context = gui.active_context

    bar = ttk.Frame(parent)
    bar.pack(fill="x", pady=5)

    city_link = ttk.Label(
        bar,
        text="City",
        foreground="blue",
        cursor="hand2"
    )

    city_link.bind(
        "<Button-1>",
        lambda e: gui.reset_city_navigation()
    )

    city_link.pack(side="left")

    region = context.get("region")

    if region:

        ttk.Label(
            bar,
            text=" > "
        ).pack(side="left")

        region_link = ttk.Label(
            bar,
            text=region.name,
            foreground="blue",
            cursor="hand2"
        )

        region_link.bind(
            "<Button-1>",
            lambda e, r=region: gui.open_region(r)
        )

        region_link.pack(side="left")

    location = context.get("location")

    if location:

        ttk.Label(
            bar,
            text=" > "
        ).pack(side="left")

        ttk.Label(
            bar,
            text=location.name
        ).pack(side="left")