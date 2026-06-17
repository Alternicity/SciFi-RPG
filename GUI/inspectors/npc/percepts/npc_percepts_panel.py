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

    frame = ttk.LabelFrame(parent, text="Percepts")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=PERCEPT_COLUMNS, show="headings")


    for col in PERCEPT_COLUMNS:
        tree.heading(
            col,
            text=COLUMN_HEADINGS.get(col, col)
        )

        tree.column(
            col,
            width=COLUMN_WIDTHS.get(col, 100)
        )

    gui.percepts_tree = tree
    tree._sublocation_map = {}

    tree.pack(fill="both", expand=True)

    def on_tree_click(event):
        iid = tree.identify_row(event.y)
        if not iid:
            return

        sublocation = tree._sublocation_map.get(iid)
        if sublocation:
            gui.inspect(sublocation)#updated


    
    def on_double_click(event):

        iid = tree.identify_row(event.y)

        if not iid:
            return

        sublocation = tree._sublocation_map.get(iid)

        if sublocation:
            gui.show_sublocation_center_view(
                sublocation
            )
    tree.bind("<Button-1>", on_tree_click)
    tree.bind("<Double-1>", on_double_click)

def refresh_percepts_panel(gui):
    
    #tmp
    print("REFRESH PERCEPTS PANEL")

    npc = gui.active_context["npc"]#current active_context is npc
    
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
    
    sections = build_percept_sections(npc)

    regular_rows = sections["regular"]
    sublocation_rows = sections["sublocations"]

    #Treeviews must be manually cleared.
    for item in tree.get_children():
        tree.delete(item)
    
    buckets = collect_display_buckets(npc)

    for origin, data, v in regular_rows:
        access_text = ""

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
                if can_perceive_sublocation(#line 154
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

    # Sublocations
    if sublocation_rows:

        divider_iid = tree.insert(
            "",
            "end",
            values=(
                "──────── SUBLOCATIONS ────────",
                "",
                "",
                ""
            )
        )

        tree._sublocation_map[divider_iid] = None


    for origin, data, v in sublocation_rows:
        print("RENDERING SUBLOCATION:", origin)

        data = v.get("data", {})

        desc = (
            data.get("description")
            or data.get("type")
            or "UNKNOWN"
        )

        type_ = data.get("type", "—")

        visible = data.get("visible", True)
        accessible = data.get("accessible", True)

        parts = [
            "Visible" if visible else "Private",
            "Accessible" if accessible else "Restricted"
        ]

        info = " | ".join(parts)

        iid = tree.insert(
            "",
            "end",
            values=(desc, type_, "", info)
        )

        tree._sublocation_map[iid] = origin