#GUI.inspectors.entity.npc_entity_page.py
from tkinter import ttk

from GUI.helpers.gui_styles import configure_gui_styles
from social.social_utils import calculate_attraction, calculate_familiarity, calculate_respect

def build_npc_entity_page(gui, parent, observer, target):

    print("BUILD NPC ENTITY PAGE")
    print("PARENT =", parent)
    print("PARENT EXISTS =", parent.winfo_exists())

    
    notebook = ttk.Notebook(parent)

    overview_tab = ttk.Frame(notebook)
    thoughts_tab = ttk.Frame(notebook)
    memories_tab = ttk.Frame(notebook)
    motivations_tab = ttk.Frame(notebook)
    psy_tab = ttk.Frame(notebook)

    notebook.add(overview_tab, text="Overview")
    notebook.add(thoughts_tab, text="Thoughts")
    notebook.add(memories_tab, text="Memories")
    notebook.add(motivations_tab, text="Motivations")
    notebook.add(psy_tab, text="Psy")

    notebook.pack(fill="both", expand=True)

    configure_gui_styles()

    style = ttk.Style()

    style.configure(
        "EntityHeading.TLabel",
        font=("TkDefaultFont", 10, "bold")
    )

    #Overview tab
    ttk.Frame(
        overview_tab,
        height=10
    ).pack()
    

    ttk.Label(
        overview_tab,
        text=f"Perspective: {observer.name}",
        style="EntityHeading.TLabel"
    ).pack(anchor="w", padx=10)

    ttk.Frame(
        overview_tab,
        height=5
    ).pack()



    #Can we put a single line of whitespace here to separate it a bit from the above?
    ttk.Label(
        overview_tab,
        text=f"Interacting with {target.name}"
    ).pack(anchor="w", padx=10)


    relation = None
    social = observer.mind.memory.semantic.get("social")

    if social:
        relation = social.get_relation(target)

    if relation:

        ttk.Label(
            overview_tab,
            text=f"Relationship: {relation.current_type}"
        ).pack(anchor="w", padx=10)

    else:
        ttk.Label(
            overview_tab,
            text="No social relation found."
        ).pack(anchor="w", padx=10)

    status_text = "None"

    if target.status:

        status = target.status.get_status(
            target.primary_status_domain
        )

        if status is not None:
            status_text = status.name

    ttk.Label(
        overview_tab,
        text=f"Status: {status_text}"
    ).pack(anchor="w", padx=10)

    print("STATUS DONE")

    respect = calculate_respect(target)

    print("RESPECT DONE")

    ttk.Label(
        overview_tab,
        text=f"Respect: {respect}"
    ).pack(anchor="w", padx=10)

    ttk.Label(
        overview_tab,
        text=f"Trust: {relation.trust}"#ATTN for consistency
    ).pack(anchor="w", padx=10)

    ttk.Label(
        overview_tab,
        text=f"Fear: {relation.fear}"#ATTN for consistency
    ).pack(anchor="w", padx=10)

    ttk.Label(
        overview_tab,
        text=f"Envy: {relation.envy}"#ATTN for consistency
    ).pack(anchor="w", padx=10)

    familiarity = calculate_familiarity(relation)

    print("FAMILIARITY DONE")

    ttk.Label(
        overview_tab,
        text=f"Familiarity: {familiarity}"
    ).pack(anchor="w", padx=10)


    attraction = calculate_attraction(target)

    print("ATTRACTION DONE")

    ttk.Label(
        overview_tab,
        text=f"Attraction: {attraction}"
    ).pack(anchor="w", padx=10)

    ttk.Label(
        overview_tab,
        text=f"Subject: {target.name}"
    ).pack(anchor="w", padx=10)

    #Thoughts tab
    ttk.Label(
        thoughts_tab,
        text=f"{observer.name}'s thoughts about {target.name}"
    ).pack(anchor="w", padx=10, pady=10)

    #Memories tab
    ttk.Label(
        memories_tab,
        text=f"{observer.name}'s memories of {target.name}"
    ).pack(anchor="w", padx=10, pady=10)

    #Motivations tab

    motives = observer.motivation_manager.get_targeted_motivations(
        target
    )

    #if there are motivations toward target
    ttk.Label(
        motivations_tab,
        text=f"{observer.name}'s motivations toward {target.name}"
    ).pack(anchor="w", padx=10, pady=10)
    #else:

    motives = (
        observer
        .motivation_manager
        .get_targeted_motivations(target)
    )

    if not motives:

        ttk.Label(
            motivations_tab,
            text="No motivations toward this character."
        ).pack(anchor="w", padx=10)

    else:

        for motive in motives:

            ttk.Label(
                motivations_tab,
                text=f"{motive.type} ({motive.urgency})"
            ).pack(anchor="w", padx=10)

    #Psy tab
    ttk.Label(
        psy_tab,
        text=f"{observer.name}'s psychic impressions of {target.name}"
    ).pack(anchor="w", padx=10, pady=10)




    print("NPC ENTITY PAGE COMPLETE")

    