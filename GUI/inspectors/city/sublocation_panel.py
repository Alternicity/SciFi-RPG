#GUI.inspectors.city.sublocation_panel.py
import tkinter
from tkinter import ttk
from dataclasses import dataclass

def build_sublocation_view(gui, parent, sublocation):

    for widget in parent.winfo_children():
        widget.destroy()

    title = ttk.Label(
        parent,
        text=f"{sublocation.name}",
        font=("Arial", 14, "bold")
    )
    title.pack(pady=10)

    # NPCs inside
    ttk.Label(parent, text="Occupants").pack(anchor="w")

    for npc in getattr(sublocation, "characters", []):
        lbl = ttk.Label(
            parent,
            text=npc.name,
            foreground="blue",
            cursor="hand2"
        )

        lbl.pack(anchor="w", padx=10)
        lbl.bind("<Button-1>", lambda e, n=npc: gui.inspect(n))

        


