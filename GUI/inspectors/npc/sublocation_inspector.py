#GUI.inspectors.npc.sublocation_inspector.py
import tkinter as tk
from tkinter import ttk


def build_sublocation_inspector(gui, parent, observer, sublocation):
    print("=== BUILD SUBLOCATION INSPECTOR ===")
    print("  parent:", parent)
    print("  sublocation:", sublocation.name)
    # Clear existing inspector
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
        text=sublocation.name,
        font=("Arial", 14, "bold")
    ).pack(
        anchor="w",
        padx=10,
        pady=(0, 10)
    )

    # ------------------------------------------------------------
    # Memories about this sublocation
    # ------------------------------------------------------------

    ttk.Label(
        parent,
        text="Memories:"
    ).pack(
        anchor="w",
        padx=10,
        pady=(5, 5)
    )

    mind = getattr(observer, "mind", None)
    memory_system = getattr(mind, "memory", None)

    matching_memories = []

    if memory_system:

        semantic = getattr(
            memory_system,
            "semantic",
            {}
        )

        place_memories = semantic.get("place", [])

        if isinstance(place_memories, list):

            for memory in place_memories:

                if getattr(
                    memory,
                    "object_ref",
                    None
                ) is sublocation:

                    matching_memories.append(memory)

    if matching_memories:

        for memory in matching_memories:

            details = getattr(
                memory,
                "details",
                None
            )

            if details:
                ttk.Label(
                    parent,
                    text=details,
                    wraplength=300,
                    justify="left"
                ).pack(
                    anchor="w",
                    padx=20,
                    pady=(0, 5)
                )

    else:

        ttk.Label(
            parent,
            text="No memories about this place."
        ).pack(
            anchor="w",
            padx=20
        )
