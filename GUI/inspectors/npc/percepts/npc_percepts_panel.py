#GUI.inspectors.npc.percepts.npc_percepts_panel.py
from objects.InWorldObjects import ObjectInWorld
from GUI.viewmodels.percept_tree import render_percept_tree
from base.location import Location, Sublocation
from location.location_security import can_access_sublocation
import tkinter as tk
from tkinter import ttk
from GUI.helpers.formatting import is_highlighted_percept
from GUI.viewmodels.percept_tree import debug_percept_tree
from GUI.inspectors.npc.percepts.percept_columns import (
    PERCEPT_COLUMNS,
    COLUMN_HEADINGS,
    COLUMN_WIDTHS
)
from GUI.viewmodels.percept_tree import DisplayNode
from character_components.observation_component import can_perceive_sublocation
from GUI.inspectors.percepts.percept_grouping import (
    build_percept_sections
)
from GUI.inspectors.npc.location_inspector import (
    build_location_view_model,
)
from objects.furniture import CafeTable, CafeChair, Sofa, Chair
from objects.expensive_furniture import OrnateChair


def build_percepts_panel(gui, parent):#creates the basic percepts tab, not the subsequent Location or Sublocation panels

    frame = ttk.LabelFrame(parent, text="Percepts")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=PERCEPT_COLUMNS, show="tree headings")

    #new
    tree.heading("#0", text="Percept")
    tree.column(
        "#0",
        width=COLUMN_WIDTHS.get("#0", 220)
    )
    #We could eventually also put the heading into a special configuration dictionary a la PERCEPT_COLUMNS

    for col in PERCEPT_COLUMNS:#Is PERCEPT_COLUMNS badly named? The following seems to 
        #configure more than just the percept column

        tree.tag_configure(
            "self",
            font=("TkDefaultFont", 10, "bold")
        )

        tree.tag_configure(
            "location",
            font=("TkDefaultFont", 10, "bold")
        )

        tree.tag_configure(
            "interaction",
            font=("TkDefaultFont", 10)
        )

        tree.heading(
            col,
            text=COLUMN_HEADINGS.get(col, col)
        )

        tree.column(
            col,
            width=COLUMN_WIDTHS.get(col, 100)
        )

    gui.percepts_tree = tree

    parent = tree.insert(
        "",
        "end",
        text="Parent Location"
    )

    tree._sublocation_map = {}

    tree.pack(fill="both", expand=True)

    def on_tree_click(event):
        iid = tree.identify_row(event.y)
        if not iid:
            return

        sublocation = tree._sublocation_map.get(iid)
        if sublocation:
            gui.inspect(sublocation)

    def on_double_click(event):

        iid = tree.identify_row(event.y)

        if not iid:
            return

        sublocation = tree._sublocation_map.get(iid)

        if sublocation:
            observer = gui.active_context["npc"]

            gui.show_entity_page(
                observer,
                sublocation,
            )
    tree.bind("<Button-1>", on_tree_click)
    tree.bind("<Double-1>", on_double_click)

def refresh_percepts_panel(gui):
    
    """ Introduce the tree structure alongside the existing machinery, prove it works for the Boss Office,
    and only then gradually move formatting into the ViewModel layer. """

    #tmp
    print("REFRESH PERCEPTS PANEL")

    npc = gui.active_context["npc"]#current active_context is npc
    
    if not npc:
        return

    tree = gui.percepts_tree

    from display.aggregate_display_buckets import (collect_display_buckets)
    from display.display import build_info_column
    from perception.perceptibility import (extract_appearance_summary)
    from GUI.viewmodels.percept_tree import build_percept_tree
    sections = build_percept_sections(npc)

    regular_rows = sections["regular"]
    


    #new
    for origin, data, v in regular_rows:

        if isinstance(origin, Location) and not isinstance(origin, Sublocation):
            print("\n=== LOCATION PERCEPT ===")
            print("origin:", origin)
            print("origin type:", type(origin))
            print("data:", data)
            print("percept:", v)
            print("========================\n")


    location_rows = sections["location"]

    sublocation_rows = sections["sublocations"]
    parent_rows = sections["parent_location"]#as in ExpensiveDesk is parent of GoldPlatedPistol

    location_row = location_rows[0] if location_rows else None
    object_percepts = []
    other_regular_rows = []
    self_percept_row = None

    

    regular_percepts = [
        v
        for origin, data, v in regular_rows
    ]

    tree_nodes = build_percept_tree(regular_percepts)

    #Treeviews must be manually cleared.
    for item in tree.get_children():
        tree.delete(item)
    
    buckets = collect_display_buckets(npc)#buckets not accessed ATTN, maybe stale aggregation code

    for origin, data, v in regular_rows:
        #First loop: collect..
        if origin is npc:
            self_percept_row = (origin, data, v)
        
        elif isinstance(origin, ObjectInWorld):
            object_percepts.append(v)

        else:
            other_regular_rows.append((origin, data, v))

    object_nodes = build_percept_tree(object_percepts)
    object_nodes = aggregate_display_nodes(object_nodes)

    #Outside loop: render:
    render_self_percept(gui, self_percept_row, npc)

    if location_row:
        render_location_percept(
            gui,
            location_row,
            npc
        )

    render_percept_tree(
        gui,
        object_nodes,
        npc=npc
    )

    for origin, data, v in other_regular_rows:

        desc = (
            data.get("name")
            or data.get("description")
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

        highlight = is_highlighted_percept(
            origin,
            npc
        )

        tags = (highlight,) if highlight else ()

        tree.insert(
            "",
            "end",
            values=(
                desc,
                type_,
                appearance,
                info
            ),
            tags=tags
        )

    if parent_rows:

        tree.insert(
            "",
            "end",
            values=(
                "──────── PARENT LOCATION ────────",
                "",
                "",
                ""
            )
        )


    for origin, data, v in parent_rows:

        desc = (
            data.get("description")
            or data.get("type")
            or "UNKNOWN"
        )

        type_ = data.get("type", "—")

        tree.insert(
            "",
            "end",
            values=(
                desc,
                type_,
                "",
                ""
            )
        )

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

        data = v.get("data", {})

        desc = (
            data.get("description")
            or data.get("type")
            or "UNKNOWN"
        )
        if origin is getattr(npc, "sublocation", None):
            desc += " (I’m Currently Here)"

        type_ = data.get("type", "—")

        visible = data.get("visible", True)
        accessible = data.get("accessible", True)

        parts = [
            "Visible" if visible else "Private",
            "Accessible" if accessible else "Restricted"
        ]

        info = " | ".join(parts)

        tag = is_highlighted_percept(origin, npc)

        if tag:
            print("SUBLOCATION TAG:", desc, "->", tag)

        iid = tree.insert(
            "",
            "end",
            values=(desc, type_, "", info),
            tags=(tag,) if tag else ()
        )

        tree._sublocation_map[iid] = origin


def render_location_percept(gui, location_row, npc):
    origin, data, percept = location_row

    vm = build_location_view_model(percept)

    tree = gui.percepts_tree

    tree.insert(
        "",
        "end",
        text=vm.name,
        values=(
            vm.description,
            vm.info or "—",
        ),
        tags=("location",)
    )

from perception.perceptibility import extract_appearance_summary
from display.display import build_info_column
def render_self_percept(gui, row, npc):
    origin, data, v = row

    tree = gui.percepts_tree

    appearance = extract_appearance_summary(
        origin,
        observer=npc
    )

    info = build_info_column(
        origin,
        npc,
        v,
        getattr(npc, "current_anchor", None)
    )

    tree.insert(
        "",
        "end",
        text="Self Percept",
        values=(
            appearance,
            info
        ),
        tags=("self",)
    )

def aggregate_display_nodes(nodes):

    result = []
    aggregatable = []

    for node in nodes:

        origin = node.origin

        # Occupied furniture is represented by the Character row.
        if isinstance(origin, (CafeChair, Chair, Sofa)):
            if getattr(origin, "occupants", None):
                if not isinstance(origin, OrnateChair):
                    continue

        if node.children:
            result.append(node)
            continue

        if is_aggregatable(node):
            aggregatable.append(node)
            continue

        result.append(node)

    groups = {}

    for node in aggregatable:
        key = node.data.get("type")
        groups.setdefault(key, []).append(node)

    # temporary: construct aggregate percepts
    aggregate_nodes = []

    for type_, members in groups.items():

        count = len(members)

        if type_ == "CafeTable":
            name = f"Tables (x{count})"
            description = f"{count} empty tables"
            display_type = "CafeTables"

        elif type_ == "CafeChair":
            name = f"Chairs (x{count})"
            description = f"{count} empty chairs"
            display_type = "CafeChairs"

        elif type_ == "Sofa":
            name = f"Sofas (x{count})"
            description = f"{count} empty sofas"
            display_type = "Sofas"

        else:
            continue

        percept = {
            "data": {
                "name": name,
                "description": description,
                "type": display_type,
                "display_aggregate": True,
                "appearance": display_type,
                "info": description,
            },
            "origin": None,
            "source": "display_aggregation",
        }

        aggregate_nodes.append(
            DisplayNode(percept=percept)
        )

    return result + aggregate_nodes


def is_aggregatable(node):
    origin = node.origin

    if not isinstance(origin, (CafeTable, CafeChair, Sofa)):
        return False

    if node.children:
        return False

    if getattr(origin, "occupants", None):
        return False

    return True