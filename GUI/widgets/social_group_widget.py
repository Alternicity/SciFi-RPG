#GUI.widgets.social_group_widget.py
import tkinter as tk
from tkinter import ttk


def build_group_widget(gui, parent, title, members, group=None,):
    card = ttk.LabelFrame(
        parent,
        text=title,
        )
    
    card.bind(
            "<Button-1>",
            lambda e, g=group: gui.inspect(g)
            #lambda e, g=group: print(g.label)
        )

    card.pack(
        side="left",
        padx=10,
        pady=5,
        ipadx=10,
        ipady=5,
        anchor="n"
    )

    for npc in members:

        link = ttk.Label(#here?
            card,
            text=npc.name,
            foreground="blue",
            cursor="hand2"
        )

        link.pack(anchor="w", padx=5)

        link.bind(
            "<Button-1>",
            lambda e, n=npc: gui.inspect(n)
        )

        link.bind(
            "<Double-Button-1>",
            lambda e, n=npc: gui.show_npc_entity_view(
                gui.active_context["npc"],
                n
            )
        )


""" def build_social_group_widget(gui, parent, social_group):

    card = ttk.LabelFrame(
        parent,
        text=getattr(
            social_group,
            "label",
            "Conversation"
        )
    )

    card.pack(
        side="left",
        padx=10,
        pady=5,
        ipadx=10,
        ipady=5,
        anchor="n"
    )

    for npc in social_group.members:

        ttk.Label(
            card,
            text=npc.name
        ).pack(anchor="w", padx=5)

def build_individuals_widget(gui, parent, groups_frame, ungrouped):
    
    card = ttk.LabelFrame(
        parent,
        text="Alone")

    card.pack(
        side="left",
        padx=10,
        pady=5,
        ipadx=10,
        ipady=5,
        anchor="n"
    )

    for npc in ungrouped.members:

        ttk.Label(
            card,
            text=npc.name
        ).pack(anchor="w", padx=5) """