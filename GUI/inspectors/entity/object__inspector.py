#GUI.inspectors.entity.object_inspector.py
from tkinter import ttk

from objects.InWorldObjects import ObjectInWorld


def build_object_inspector(gui, parent, obj):

    data = obj.get_percept_data()

    ttk.Label(
        parent,
        text=data.get("name", "Unknown Object"),
        font=("Arial", 14, "bold")
    ).pack(
        anchor="w",
        padx=10,
        pady=(10, 5)
    )

    ttk.Label(
        parent,
        text=f"Type: {data.get('type', 'Unknown')}"
    ).pack(
        anchor="w",
        padx=10
    )

    ttk.Label(
        parent,
        text=f"Description: {data.get('description', '')}"
    ).pack(
        anchor="w",
        padx=10
    )

    ttk.Label(
        parent,
        text=f"Details: {data.get('details', '')}"
    ).pack(
        anchor="w",
        padx=10
    )