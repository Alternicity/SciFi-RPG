#GUI.inspectors.npc.sublocation_inspector.py

import tkinter as tk
from tkinter import ttk

def build_sublocation_inspector(gui, parent, observer, sublocation):
    # Temporary minimal inspector
    for child in parent.winfo_children():
        child.destroy()

    ttk.Label(
        parent,
        text="Inspecting:"
    ).pack(
        anchor="w",
        padx=10,
        pady=(10, 5)
    )

    ttk.Label(
        parent,
        text=sublocation.name
    ).pack(
        anchor="w",
        padx=10
    )





