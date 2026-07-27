#GUI.inspectors.npc.social_group_inspector.py
from tkinter import ttk

def build_social_group_inspector(gui, parent, social_group):

    for child in parent.winfo_children():
        child.destroy()

    ttk.Label(
        parent,
        text=social_group.label,
        font=("Arial", 16, "bold")
    ).pack(anchor="w", padx=10, pady=5)

    ttk.Label(
        parent,
        text="Members"
    ).pack(anchor="w", padx=10)

    for npc in social_group.members:

        ttk.Label(
            parent,
            text=npc.name
        ).pack(anchor="w", padx=20)