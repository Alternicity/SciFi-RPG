#GUI.inspectors.percepts.npc_percepts_panel.py
from location.location_security import can_access_sublocation
import tkinter as tk
from tkinter import ttk
from GUI.inspectors.npc.percepts.percept_columns import (
    PERCEPT_COLUMNS,
    COLUMN_HEADINGS,
    COLUMN_WIDTHS
)
from character_components.observation_component import can_perceive_sublocation
from GUI.inspectors.percepts.percept_grouping import (
    build_percept_sections
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
    
    sections = build_percept_sections(npc)#here

    regular_rows = sections["regular"]
    sublocation_rows = sections["sublocations"]

    print(
        "SUBLOCATION COUNT:",
        len(sublocation_rows)
    )

    print(
        "SUBLOCATION ROWS:",
        sublocation_rows
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

    for origin, data, v in regular_rows:
        access_text = ""
        
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

        type_ = data.get("type", "—")


        appearance = extract_appearance_summary(
            origin,
            observer=npc
        )

        access_text = ""
        visibility_text = ""

        if hasattr(origin, "accessible_roles"):

            print(
                "[SUBLOCATION PERCEPT]",
                npc.name,
                origin.name,
                can_perceive_sublocation(
                    npc,
                    origin
                ),
                can_access_sublocation(
                    npc,
                    origin
                )
            )
            
            access_text = (
                "Accessible"
                if can_access_sublocation(
                    npc,
                    origin
                )
                else "Restricted"
            )

            visibility_text = (
                "Visible"
                if can_perceive_sublocation(
                    npc,
                    origin
                )
                else "Private"
            )

        parts = []

        if visibility_text:
            parts.append(visibility_text)

        if access_text:
            parts.append(access_text)

        if hasattr(origin, "accessible_roles"):

            info = " | ".join(parts)

        else:

            info = build_info_column(
                origin,
                npc,
                v,
                getattr(npc, "current_anchor", None)
            )

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
    
    

    #the original table handling code
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

    #Sublocations
    if sublocation_rows:

        tree.insert(
            "",
            "end",
            values=(
                "──────── SUBLOCATIONS ────────",
                "",
                "",
                ""
            )
        )

    for origin, data, v in sublocation_rows:
        print("RENDERING SUBLOCATION:", origin)
        
        data = v.get("data", {})

        desc = (
            data.get("description")
            or data.get("type")
            or "UNKNOWN"
        )

        type_ = data.get("type", "—")

        parts = []

        if can_perceive_sublocation(
            npc,
            origin
        ):
            parts.append("Visible")
        else:
            parts.append("Private")

        if can_access_sublocation(
            npc,
            origin
        ):
            parts.append("Accessible")
        else:
            parts.append("Restricted")

        info = " | ".join(parts)

        print(
            "INSERTING SUBLOCATION:",
            origin.name,
            info
        )

        tree.insert(
            "",
            "end",
            values=(
                desc,
                type_,
                "",
                info
            )
        )