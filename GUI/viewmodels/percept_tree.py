#GUI.viewmodels.percept_tree.py
from dataclasses import dataclass, field
from perception.perceptibility import extract_appearance_summary
from display.display import build_info_column
from GUI.helpers.formatting import is_highlighted_percept

@dataclass
class DisplayNode:

    #origin: object
    #refers to a specific object - if we re-enable this field how will
    #it handle objects to be aggregated, like empty tables?

    #generic but:
    percept: dict#the relevant test ones will be table and desk

    children: list["DisplayNode"] = field(
        default_factory=list
    )#the relevant ones will be cup and GoldPlatedPistol
    #what function will crete DisplayNode objects?


    @property
    def origin(self):
        return self.percept.get("origin")

    @property
    def data(self):
        return self.percept.get("data", {})


#Utility function
def build_percept_tree(percepts):
    """
    Build a generic parent/child tree from percept records.

    Objects can become children of other perceived objects when
    their percept data contains:

        data["resting_on"] = supporting_object

    The function knows nothing about desks, tables, cups, pistols,
    etc. It only understands the relationship expressed by the
    percept data.
    """

    """ The key is that resting_on currently contains the actual supporting object:
    data["resting_on"] = desk
    So we can use object identity, rather than names """

    #a ViewModel transformation

    """ npc.percepts
     │
     ├── build_percept_sections()
     │       │
     │       ├── regular
     │       ├── sublocations
     │       └── parent_location
     │
     └── build_percept_tree()
             │
             └── parent/child relationships """
    
    nodes = {}
    roots = []

    #build_percept_tree() should not call get_sublocation_percepts()

    #function doesn't know what a Desk, Pistol or Medkit is

    # First create one DisplayNode for every percept.

    # ---------------------------------------------------------
    # Pass 1:
    # Create one DisplayNode for every supplied percept.
    # ---------------------------------------------------------

    for percept in percepts:

        origin = percept.get("origin")

        if origin is None:#this might now be a problem
            continue

        nodes[id(origin)] = DisplayNode(
            percept=percept
        )

    # ---------------------------------------------------------
    # Pass 2:
    # Establish parent/child relationships.
    # ---------------------------------------------------------

    for percept in percepts:

        origin = percept.get("origin")

        if origin is None:
            continue

        node = nodes.get(id(origin))

        if node is None:
            continue

        data = percept.get("data", {})
        resting_on = data.get("resting_on")

        # No supporting object:
        # this is a root-level percept.
        if resting_on is None:
            roots.append(node)
            continue

        # Find the supporting object's DisplayNode.
        parent_node = nodes.get(id(resting_on))

        if parent_node is None:
            # The supporting object wasn't included in the
            # supplied percept collection. Don't lose the object.
            roots.append(node)
            continue

        parent_node.children.append(node)

    # Aggregation is deliberately not performed here.
    # This function builds the semantic percept hierarchy;
    # display aggregation belongs to a later presentation step.
    return roots

    #returns:
    """ DisplayNode
        Desk
            Pistol
            Medkit

    DisplayNode
        Chair

    DisplayNode
        Boss """

#tmp
def debug_percept_tree(nodes, indent=0):

    for node in nodes:

        percept = node.percept
        origin = percept.get("origin")
        data = percept.get("data", {})

        resting_on = data.get("resting_on")

        print(
            " " * indent,
            origin.__class__.__name__,
            data.get("name"),
            "origin_id=",
            id(origin),
            "resting_on=",
            repr(resting_on),
            "resting_on_type=",
            type(resting_on).__name__,
            "resting_on_id=",
            id(resting_on) if resting_on is not None else None,
            "children=",
            len(node.children),
        )

        debug_percept_tree(
            node.children,
            indent + 4
        )

#Eventually remove the Tkinter-specific tree.insert() from render_percept_tree()
#Eventually put this somewhere like GUI.inspectors.percepts
def render_percept_tree(#Tkinter rendering
    #

    #render_percept_tree() is currently designed for the NPC Percepts tab, not the Sublocation Inspector.
    gui,
    nodes,
    parent="",
    npc=None
):
    #This renderer expects:
    tree = gui.percepts_tree#Percepts tab.

    for node in nodes:

        origin = node.origin
        data = node.data
        v = node.percept

        desc = (
            data.get("name")
            or data.get("description")
            or data.get("type")
            or "UNKNOWN"
        )

        type_ = data.get("type", "—")

        if data.get("display_aggregate"):

            appearance = data.get("appearance", "—")
            info = data.get("info", "—")

            tags = ("aggregate",)

        else:

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

            highlight = is_highlighted_percept(
                origin,
                npc
            )

            tags = (highlight,) if highlight else ()

        iid = tree.insert(
            parent,
            "end",
            text=desc,
            values=(
                appearance,
                info
            ),
            tags=tags,
            open=bool(node.children)
        )

        render_percept_tree(
            gui,
            node.children,
            parent=iid,
            npc=npc
        )

