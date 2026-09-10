#GUI.inspectors.sublocations.sublocation_entity_page.py
import tkinter as tk
from tkinter import ttk

from GUI.inspectors.npc.sublocation_inspector import build_sublocation_inspector
from GUI.widgets.sublocation_widget import build_sublocation_view_model

from GUI.inspectors.npc.percepts.npc_percepts_panel import aggregate_display_nodes

from GUI.widgets.social_group_widget import build_group_widget
from GUI.viewmodels.sublocation_viewmodel import get_sublocation_percepts
from GUI.viewmodels.percept_tree import build_percept_tree

from base.character import Character
from social.social_groups import SocialGroup

def build_sublocation_entity_page(gui, parent, observer, sublocation):

    # clear frame
    for child in parent.winfo_children():
        child.destroy()

    vm = build_sublocation_view_model(sublocation)

    # title
    title = tk.Label(parent, text=vm.name, font=("Arial", 16, "bold"))
    title.pack(anchor="w", padx=10, pady=5)

    # visibility
    """ vis_text = "Visible" if vm.visible else "Not Visible"#marked for deprecation
    tk.Label(parent, text=f"Visibility: {vis_text}").pack(anchor="w", padx=10) """

    # accessibility
    """ acc_text = "Accessible" if vm.accessible else "Not Accessible"#needs an edit
    tk.Label(parent, text=f"Accessibility: {acc_text}").pack(anchor="w", padx=10) """

    # Who can enter?
    """ if vm.accessible_roles:
        tk.Label(parent, text="Accessible Roles:").pack(anchor="w", padx=10)
        for role in vm.accessible_roles:
            tk.Label(parent, text=f" - {role}").pack(anchor="w", padx=20) """


    occupants = sublocation.list_characters()#this should probably instead use the perceiving npcs percepts?
    groups = []#When many npcs, create global container
    ungrouped = []
    seen = set()

    ttk.Label(
        parent,
        text="Social Groups"
    ).pack(anchor="w", padx=10, pady=(10, 0))

    for npc in occupants:

        group = npc.current_social_group

        if group is None:
            ungrouped.append(npc)

        elif id(group) not in seen:
            seen.add(id(group))
            groups.append(group)

    groups_frame = ttk.Frame(parent)
    groups_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    for group in groups:#refers to Social groups
        print("Groups found:", len(groups))
        build_group_widget(
            gui,
            groups_frame,
            title=group.label,
        members=group.members,
        group=group
        )

    if ungrouped:

        build_group_widget(
            gui,
            groups_frame,
            title="Individuals",
        members=ungrouped,
        group = None
        )


    ttk.Label(
        parent,
        text="Objects"
    ).pack(anchor="w", padx=10, pady=(10, 0))


    object_tree = ttk.Treeview(
        parent,
        columns=("description", "info"),
        show="tree headings"
    )

    object_tree.heading("#0", text="Percept")
    object_tree.heading("description", text="Description")
    object_tree.heading("info", text="Info")

    object_tree.column("#0", width=180)
    object_tree.column("description", width=250)
    object_tree.column("info", width=150)

    object_tree.pack(
        fill="x",#"was both"
        #expand=True,
        padx=20,
        pady=5
    )

    percepts = get_sublocation_percepts(observer, sublocation)

    #ATTN ViewModel
    """ I think the ViewModel should own this
    Personally I would probably move even this logic into
    GUI/viewmodels/sublocation_viewmodel.py """
    #Your comment
    
    if not percepts:

        ttk.Label(
            parent,
            text="None"
        ).pack(anchor="w", padx=20)
        
    else:

        objects = []
        characters = []
        groups = []

        for percept in percepts:

            origin = percept["origin"]

            if isinstance(origin, Character):
                characters.append(percept)

            elif isinstance(origin, SocialGroup):
                groups.append(percept)

            else:
                objects.append(percept)#i assume books pass through here

        ttk.Label(
            parent,
            text="Characters"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        character_tree = ttk.Treeview(
            parent,
            columns=("description", "info"),
            show="tree headings",
            height=max(1, len(characters))
        )

        character_tree.heading("#0", text="Percept")
        character_tree.heading("description", text="Description")
        character_tree.heading("info", text="Info")

        character_tree.column("#0", width=180)
        character_tree.column("description", width=250)
        character_tree.column("info", width=150)

        # Treeview styling: define how the "self" display tag is rendered.
        character_tree.tag_configure(
            "self",
            font=("Arial", 10, "bold")
        )

        character_tree.pack(
            fill="x",
            padx=20,
            pady=5
        )

        render_sublocation_character_rows(
            character_tree,
            characters,
            observer
        )

        object_nodes = build_percept_tree(objects)

        object_nodes = aggregate_display_nodes(object_nodes)

        render_sublocation_object_tree(
            object_tree,
            object_nodes
        )





    #Ambience section
    ttk.Label(
        parent,
        text="Ambience"
    ).pack(anchor="w", padx=10, pady=(10, 0))

    ambience = getattr(
        sublocation,
        "ambience",
        None
    )

    if ambience and ambience.vibes:

        for vibe, power in ambience.vibes.items():

            ttk.Label(
                parent,
                text=f"{vibe}: {power:.2f}"
            ).pack(anchor="w", padx=20)

    else:

        ttk.Label(
            parent,
            text="None"
        ).pack(anchor="w", padx=20)

    if hasattr(sublocation, "ambience"):
        print("AMBIENCE:", sublocation.ambience.vibes)
        



def render_sublocation_object_tree(tree, nodes, parent=""):
    for node in nodes:

        data = node.data

        text = (
            data.get("name")
            or data.get("description")
            or data.get("type")
            or "UNKNOWN"
        )

        description = data.get("description", "")
        info = data.get("details", "")

        item_id = tree.insert(
            parent,
            "end",
            text=text,
            values=(description, info),
            open=bool(node.children)
        )

        render_sublocation_object_tree(
            tree,
            node.children,
            parent=item_id
        )


from display.display import build_info_column#no longer accessed
from GUI.helpers.formatting import is_highlighted_percept#no longer accessed

from GUI.viewmodels.character_display import get_character_display_data
def render_sublocation_character_rows(tree, percepts, observer):
    #is the display-row → Tkinter Treeview rendering.

    #gui.active_context["npc"]
    #without it getting passed in, gui is still not defined

    for percept in percepts:

        name, description, info, highlight = get_character_display_data(#new
            percept,
            observer
        )
        tags = (highlight,) if highlight else ()

        tree.insert(
            "",
            "end",
            text=name,
            values=(description, info),
            tags=tags
        )