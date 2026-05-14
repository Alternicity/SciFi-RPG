#GUI.inspectors.npc_thoughts_panel.py

import tkinter as tk
from tkinter import ttk
from GUI.helpers.gui_styles import TEXT_SELECTION

def build_thoughts_panel(gui, parent):

    frame = ttk.LabelFrame(
        parent,
        text="Thoughts"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    gui.thoughts_text = tk.Text(
        frame,
        wrap="word"
    )
    
    gui.thoughts_text.config(**TEXT_SELECTION)#Selection background

    gui.thoughts_text.pack(
        fill="both",
        expand=True
    )


def refresh_thoughts_panel(gui):

    npc = gui.selected_npc

    if not npc:
        return

    text_widget = gui.thoughts_text

    text_widget.config(state="normal")

    text_widget.delete("1.0", tk.END)

    mind = getattr(npc, "mind", None)

    if not mind:

        text_widget.insert(
            tk.END,
            "No mind.\n"
        )

        text_widget.config(state="disabled")

        return

    thoughts = list(getattr(mind, "thoughts", []))

    if not thoughts:

        text_widget.insert(
            tk.END,
            "No thoughts.\n"
        )

    else:

        sorted_thoughts = sorted(
            thoughts,
            key=lambda t: getattr(t, "urgency", 0),
            reverse=True
        )

        for thought in sorted_thoughts:

            urgency = getattr(thought, "urgency", "?")

            content = getattr(
                thought,
                "content",
                str(thought)
            )

            tags = getattr(
                thought,
                "tags",
                []
            )

            text_widget.insert(
                tk.END,
                f"[{urgency}] {content}\n"
            )

            if tags:

                text_widget.insert(
                    tk.END,
                    f"tags: {', '.join(tags)}\n"
                )

            text_widget.insert(
                tk.END,
                "\n"
            )

    text_widget.config(state="disabled")