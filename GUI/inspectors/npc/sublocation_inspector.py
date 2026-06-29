#GUI.inspectors.npc.sublocation_inspector.py
import tkinter as tk
from tkinter import ttk
from GUI.widgets.sublocation_widget import build_sublocation_view_model
from GUI.widgets.social_group_widget import build_group_widget

from perception.sublocation_percepts import get_sublocation_percepts



def build_sublocation_inspector(gui, parent, sublocation):
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


    occupants = sublocation.list_characters()#Should this instead use the perceiving npcs percepts?
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

    for group in groups:
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
    


    ttk.Label(#this is going to be deprecated
        parent,
        text="Occupants"
    ).pack(anchor="w", padx=10, pady=(10, 0))

    for npc in occupants:

        link = ttk.Label(
            parent,
            text=npc.name,
            foreground="blue",
            cursor="hand2"
        )

        link.pack(anchor="w", padx=20)

        link.bind(
            "<Button-1>",
            lambda e, n=npc: gui.inspect(n)
        )
    
        link.bind(
            "<Double-Button-1>",
            lambda e, n=npc: gui.show_npc_entity_view(
                gui.active_context["npc"],
                n
            )
        )

    ttk.Label(
        parent,
        text="Objects"
    ).pack(anchor="w", padx=10, pady=(10, 0))


    percepts = get_sublocation_percepts(
        sublocation
    )

    if not percepts:

        ttk.Label(
            parent,
            text="None"
        ).pack(anchor="w", padx=20)

    else:

        for text in percepts:

            ttk.Label(
                parent,
                text=f"- {text}"
            ).pack(anchor="w", padx=20)

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



    print("SUBLOCATION TYPE:", type(sublocation))
    print("HAS characters_there:", hasattr(sublocation, "characters_there"))
    print("HAS list_characters:", hasattr(sublocation, "list_characters"))# a class Location method, only uesd here!
    print("OBJECTS:", sublocation.objects_present)

    if hasattr(sublocation, "ambience"):
        print("AMBIENCE:", sublocation.ambience.vibes)
        
    print(f"from build_sublocation_inspector {type(sublocation)}")
    #print(f"from build_sublocation_inspector {dir(sublocation)}")
    #verbose

    """ Preventing future duplication (the important part)

    To stop this from becoming messy later, enforce this rule:

    Never do this:
    building Tkinter widgets directly from Sublocation in multiple places
    formatting visibility/access rules inside panels

    Always do this
    convert → ViewModel
    render → shared renderer """

