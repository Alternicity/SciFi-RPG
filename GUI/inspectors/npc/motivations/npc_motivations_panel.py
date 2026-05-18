#GUI.inspectors.npc_motivations_panel.py
import tkinter as tk
from tkinter import ttk
from GUI.helpers.gui_styles import TEXT_SELECTION

def build_motivations_panel(gui, parent):

    frame = ttk.LabelFrame(
        parent,
        text="Motivations"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    gui.motivations_text = tk.Text(
        frame,
        wrap="word",
        height=20
    )

    gui.motivations_text.pack(
        fill="both",
        expand=True
    )
    gui.motivations_text.config(**TEXT_SELECTION)#Selection background

def refresh_motivations_panel(gui):

    npc = gui.active_context["npc"]

    if not npc:
        return

    text_widget = gui.motivations_text

    text_widget.config(state="normal")

    text_widget.delete("1.0", tk.END)

    motivation_manager = getattr(
        npc,
        "motivation_manager",
        None
    )

    motivations = []

    if motivation_manager:
        motivations = motivation_manager.motivations

    if not motivations:

        text_widget.insert(
            tk.END,
            "No motivations.\n"
        )

    else:

        sorted_motives = sorted(
            motivations,
            key=lambda m: getattr(m, "urgency", 0),
            reverse=True
        )

        for motive in sorted_motives:

            motive_type = getattr(motive, "type", "Unknown")

            urgency = getattr(motive, "urgency", "?")

            target = getattr(motive, "target", None)

            persistent = getattr(
                motive,
                "persistent",
                False
            )

            suppressed = getattr(
                motive,
                "suppressed",
                False
            )

            suppression_reason = getattr(
                motive,
                "suppression_reason",
                None
            )

            text_widget.insert(
                tk.END,
                f"{motive_type}\n"
            )

            text_widget.insert(
                tk.END,
                f"  urgency: {urgency:.1f}\n"
            )

            if target:

                if hasattr(target, "name"):
                    target_text = target.name
                else:
                    target_text = str(target)

                text_widget.insert(
                    tk.END,
                    f"  target: {target_text}\n"
                )

            text_widget.insert(
                tk.END,
                f"  persistent: {persistent}\n"
            )

            text_widget.insert(
                tk.END,
                f"  suppressed: {suppressed}\n"
            )

            if suppression_reason:

                text_widget.insert(
                    tk.END,
                    f"  reason: {suppression_reason}\n"
                )

            text_widget.insert(
                tk.END,
                "\n"
            )