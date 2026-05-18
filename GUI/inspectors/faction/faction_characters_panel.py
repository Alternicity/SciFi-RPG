#GUI.inspectors.faction.faction_characters_panel.py
import tkinter as tk
from tkinter import ttk


def build_faction_characters_panel(gui,parent):
    from GUI.widgets.faction_hierarchy_widget import FactionHierarchyWidget

    print("BUILDING FACTION CHARACTERS PANEL")
    gui.faction_hierarchy_widget = (
        FactionHierarchyWidget(gui, parent)
    )

def jump_to_npc(self, npc):
    pass

def refresh_faction_characters(gui):

    faction = gui.active_context["faction"]

    if not faction:
        return

    gui.faction_hierarchy_widget.render(faction)

def make_entry(gui, parent, name, npc):
    lbl = tk.Label(
        parent,
        text=name,
        fg="cyan",
        cursor="hand2"
    )

    lbl.pack(side="left", padx=8, pady=4)

    lbl.bind(
        "<Button-1>",
        lambda e, n=npc: gui.open_npc(n)
    )

    return lbl

