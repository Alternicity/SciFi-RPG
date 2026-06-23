#GUI.inspectors.npc.sublocation_inspector.py
import tkinter as tk
from tkinter import ttk
from GUI.widgets.sublocation_widget import build_sublocation_view_model


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
    vis_text = "Visible" if vm.visible else "Not Visible"#marked for deprecation
    tk.Label(parent, text=f"Visibility: {vis_text}").pack(anchor="w", padx=10)

    # accessibility
    acc_text = "Accessible" if vm.accessible else "Not Accessible"#needs an edit
    tk.Label(parent, text=f"Accessibility: {acc_text}").pack(anchor="w", padx=10)

    # roles
    if vm.accessible_roles:#can stay for now
        tk.Label(parent, text="Accessible Roles:").pack(anchor="w", padx=10)
        for role in vm.accessible_roles:
            tk.Label(parent, text=f" - {role}").pack(anchor="w", padx=20)

    occupants = sublocation.list_characters()

    ttk.Label(
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
    print("HAS list_characters:", hasattr(sublocation, "list_characters"))
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

