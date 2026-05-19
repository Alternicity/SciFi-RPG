#GUI.widgets.faction_hierarchy_widget.py

import tkinter as tk

from GUI.inspectors.faction.faction_characters_panel import make_entry

class FactionHierarchyWidget:

    def __init__(self, gui, parent):
        self.gui = gui
        self.parent = parent

        self.frames = {}

        self.container = tk.Frame(parent)
        self.container.pack(fill="both", expand=True)

    def render(self, faction):
        print("RENDERING HIERARCHY")
        print(faction)
        # clear old UI
        for w in self.container.winfo_children():
            w.destroy()

        for label, group in faction.iter_hierarchy():
            print(label, group)
            frame = tk.LabelFrame(
                self.container,
                text=label
            )

            frame.pack(
                fill="x",
                padx=10,
                pady=8
            )

            inner = tk.Frame(frame)
            inner.pack(anchor="center", pady=4)

            self.frames[label] = frame

            for npc in (group or []):

                if npc is None:
                    continue

                make_entry(
                self.gui,
                inner,
                npc.name,
                npc
            )
