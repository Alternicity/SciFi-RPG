#GUI.inspectors.npc.thoughts.npc_thoughts_panel.py

import tkinter as tk
from tkinter import ttk


""" mind.thoughts = flat collection of all thoughts
thought.corollary = hierarchical relationship for display/navigation
Treeview = visual representation of that relationship """

def build_thoughts_panel(gui, parent):

    frame = ttk.LabelFrame(
        parent,
        text="Thoughts"
    )

    gui.thoughts_tree = ttk.Treeview(
        frame,
        columns=("urgency", "thought"),
        show="tree headings"
    )

    gui.thoughts_tree.heading(
        "#0",
        text="Thought"
    )

    gui.thoughts_tree.heading(
        "urgency",
        text="Urgency"
    )

    gui.thoughts_tree.column(
        "#0",
        width=500
    )

    gui.thoughts_tree.column(
        "urgency",
        width=70,
        anchor="center"
    )

    gui.thoughts_tree.pack(
        fill="both",
        expand=True
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

def refresh_thoughts_panel(gui):

    

    npc = gui.active_context["npc"]

    if not npc:
        return

    mind = getattr(npc, "mind", None)

    if not mind:
        return

    thoughts = list(
        getattr(mind, "thoughts", [])
    )

    tree = gui.thoughts_tree

    for item in tree.get_children():
        tree.delete(item)

    corollaries = {
        id(corollary)
        for thought in thoughts
        for corollary in getattr(
            thought,
            "corollary",
            []
        )
    }

    root_thoughts = [#A root thought is a thought that does not appear as a child of another thought
        thought
        for thought in thoughts
        if id(thought) not in corollaries
    ]

    if not root_thoughts:
        return

    sorted_thoughts = sorted(
        root_thoughts,
        key=lambda t: getattr(t, "urgency", 0),
        reverse=True
    )

    for thought in sorted_thoughts:
        insert_thought(
            tree,
            thought
        )

def insert_thought(tree, thought, parent=""):

    urgency = getattr(
        thought,
        "urgency",
        "?"
    )

    content = getattr(
        thought,
        "content",
        str(thought)
    )

    item_id = tree.insert(
        parent,
        "end",
        text=content,
        values=(urgency,)
    )

    for corollary in getattr(
        thought,
        "corollary",
        []
    ):
        insert_thought(
            tree,
            corollary,
            parent=item_id
        )