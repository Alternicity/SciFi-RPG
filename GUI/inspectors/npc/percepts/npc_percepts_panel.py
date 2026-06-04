#GUI.inspectors.percepts.npc_percepts_panel.py

import tkinter as tk
from tkinter import ttk
from GUI.inspectors.npc.percepts.percept_columns import (
    PERCEPT_COLUMNS,
    COLUMN_HEADINGS,
    COLUMN_WIDTHS
)

def build_percepts_panel(gui, parent):

    frame = ttk.LabelFrame(
        parent,
        text="Percepts"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    tree = ttk.Treeview(
        frame,
        columns=PERCEPT_COLUMNS,
        show="headings"
    )

    for column in PERCEPT_COLUMNS:

        tree.heading(
            column,
            text=COLUMN_HEADINGS[column]
        )

        tree.column(
            column,
            width=COLUMN_WIDTHS[column],
            anchor="w"
        )

    tree.pack(
        fill="both",
        expand=True
    )

    gui.percepts_tree = tree


def refresh_percepts_panel(gui):
    #print("refresh_percepts_panel called")
    npc = gui.active_context["npc"]
    
    if not npc:
        return

    tree = gui.percepts_tree

    from display.aggregate_display_buckets import (
        collect_display_buckets
    )
    from display.display import build_info_column
    from perception.perceptibility import (
        extract_appearance_summary
    )
    

    #Treeviews must be manually cleared.
    for item in tree.get_children():
        tree.delete(item)
    
    buckets = collect_display_buckets(npc)

    #tmp
    print(
        "NORMAL ROWS:",
        len(buckets["normal_rows"])
    )

    for origin, data, v in buckets["normal_rows"]:

        #tmp
        print(
            "ROW:",
            type(origin).__name__,
            getattr(origin, "name", None)
        )

        desc = (
            data.get("description")
            or data.get("type")
            or "UNKNOWN"
        )

        type_ = data.get("type", "—")#type can drift
        #type_ = origin.__class__.__name__
        #this line for class 


        appearance = extract_appearance_summary(
            origin,
            observer=npc
        )

        access_text = ""

        if hasattr(origin, "accessible_roles"):

            if not origin.accessible_roles:
                access_text = "Accessible"

            elif getattr(npc, "role", None) in origin.accessible_roles:
                access_text = "Accessible"

            else:
                access_text = "Restricted"

        info = build_info_column(
            origin,
            npc,#does role go in here?
            v,
            getattr(npc, "current_anchor", None)
        )
        if access_text:
            info = f"{info} | {access_text}"

        #tmp
        print(
            "INSERTING:",
            desc,
            type_,
            appearance,
            info
        )

        tree.insert(
            "",
            "end",
            values=(
                desc,
                type_,
                appearance,
                info
            )
        )
    
    for table in buckets["occupied_tables"]:

        seated = table.get_occupants(npc.location)

        occupant_descriptions = [
            f"{o.race}, {o.sex}"
            for o in seated
        ]

        tree.insert(
            "",
            "end",
            values=(
                table.name,
                "CafeTable",
                f"Occupied ({len(seated)})",
                ", ".join(occupant_descriptions)
            )
        )
    empty_tables = buckets["empty_tables"]

    if empty_tables:

        count = len(empty_tables)

        tree.insert(
            "",
            "end",
            values=(
                f"Tables (x{count})",
                "CafeTables",
                f"{count} empty tables",
                "Empty"
            )
        )



        """ collect_display_buckets
        extract_appearance_summary
        build_info_column

        are NOT terminal-only.

        They are actually reusable presentation utilities."""
