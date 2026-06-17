#GUI.inspectors.sublocations.sublocation_page.py
from tkinter import ttk
from ambience.ambience_and_psy_utils import compute_location_ambience
from GUI.viewmodels.sublocation_viewmodel import get_sublocation_percepts

def build_sublocation_page(gui, parent, observer, sublocation):
    
    notebook = ttk.Notebook(parent)

    compute_location_ambience(sublocation, observer)

    percepts = get_sublocation_percepts(observer, sublocation)

    overview_tab = ttk.Frame(notebook)
    percepts_tab = ttk.Frame(notebook)

    notebook.add(
        overview_tab,
        text="Overview"
    )

    notebook.add(
        percepts_tab,
        text="Percepts"
    )

    notebook.pack(
        fill="both",
        expand=True
    )


    ambience = compute_location_ambience(
        sublocation,
        observer
    )
    ttk.Label(
        overview_tab,
        text="Ambience"
    ).pack(...)#not sure what to do with this yet


    for vibe, strength in ambience.items():

        ttk.Label(
            overview_tab,
            text=f"{vibe}: {strength:.1f}"
        ).pack(anchor="w")

        
    """ Eventually, tabs:
    Overview
    Percepts
    Thoughts
    Memories
    Psy """