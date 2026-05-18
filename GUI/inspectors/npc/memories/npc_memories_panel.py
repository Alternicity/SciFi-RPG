#GUI.inspectors.memories.npc_memories_panel.py
import tkinter as tk
from tkinter import ttk
from GUI.helpers.gui_styles import TEXT_SELECTION

def build_memories_panel(gui, parent):

    frame = ttk.LabelFrame(
        parent,
        text="Memories"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    gui.memories_text = tk.Text(
        frame,
        wrap="word"
    )

    gui.memories_text.pack(
        fill="both",
        expand=True
    )
    gui.memories_text.config(**TEXT_SELECTION)#Selection background

def refresh_memories_panel(gui):

    npc = gui.active_context["npc"]

    if not npc:
        return

    text_widget = gui.memories_text

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

    memory = getattr(mind, "memory", None)

    if not memory:

        text_widget.insert(
            tk.END,
            "No memory system.\n"
        )

        text_widget.config(state="disabled")

        return

    episodic = getattr(
        memory,
        "episodic",
        []
    )

    semantic = getattr(
        memory,
        "semantic",
        {}
    )

    # --- Episodic ---

    text_widget.insert(
        tk.END,
        "=== Episodic ===\n\n"
    )

    if episodic:

        for mem in episodic[-20:]:

            subject = getattr(mem, "subject", "?")
            verb = getattr(mem, "verb", "")
            object_ = getattr(mem, "object_", "")

            line = f"{subject} {verb} {object_}".strip()

            text_widget.insert(
                tk.END,
                f"- {line}\n"
            )

            details = getattr(mem, "details", None)

            if details:

                text_widget.insert(
                    tk.END,
                    f"  {details}\n"
                )

            importance = getattr(
                mem,
                "importance",
                None
            )

            if importance is not None:

                text_widget.insert(
                    tk.END,
                    f"  importance: {importance}\n"
                )

            text_widget.insert(
                tk.END,
                "\n"
            )

    else:

        text_widget.insert(
            tk.END,
            "No episodic memories.\n\n"
        )

    # --- Semantic ---

    text_widget.insert(
        tk.END,
        "\n=== Semantic ===\n\n"
    )

    semantic_found = False

    for category, memories in semantic.items():

        if not isinstance(memories, list):
            continue

        if not memories:
            continue

        semantic_found = True

        text_widget.insert(
            tk.END,
            f"[{category}]\n"
        )

        for mem in memories[-10:]:

            if hasattr(mem, "subject"):

                subject = getattr(mem, "subject", "?")
                verb = getattr(mem, "verb", "")
                object_ = getattr(mem, "object_", "")

                line = f"{subject} {verb} {object_}".strip()

                text_widget.insert(
                    tk.END,
                    f"- {line}\n"
                )

            else:

                text_widget.insert(
                    tk.END,
                    f"- {str(mem)}\n"
                )

        text_widget.insert(
            tk.END,
            "\n"
        )

    if not semantic_found:

        text_widget.insert(
            tk.END,
            "No semantic memories.\n"
        )

    text_widget.config(state="disabled")