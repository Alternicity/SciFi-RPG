#GUI.viewmodels.sublocation_viewmodel.py
from dataclasses import dataclass

@dataclass
class SublocationViewModel:
    name: str
    visible: bool
    accessible: bool
    accessible_roles: list[str]
    raw: object  # optional reference to Sublocation
    """ This is the only thing UI consumes.
    both panels render the same model (though this must change for the right panel/inspector)
    no Tkinter logic leaks into game logic
    formatting rules live in one place """

#utility functions


#trying to be cleaner than belongs_to_sublocation()
# by using percept data alone—but if the object percepts don't yet include "sublocation", it will naturally find nothing.

""" SublocationViewModel
"What is this sublocation and what does the observer perceive there?"

Percept tree
"How are these percepts related hierarchically?" """

def get_sublocation_percepts(observer, sublocation):

    rows = []

    for percept in observer.percepts.values():

        data = percept["data"]

        if data.get("sublocation") != sublocation.name:
            continue

        rows.append(percept)

    return rows

"""Eventually the GUI should look like

Simulation
↓
Observation
        ↓
Percepts
        ↓
ViewModel
        ↓
GUI

not

Simulation
        ↘
Observation
        ↘
Inspector """

"""Eventually:
PlaceViewModel
↑
│
LocationViewModel

SublocationViewModel
"""


"""Simulation
        ↓
        place_object()
        ↓
        Object metadata
        ↓
        ObservationComponent
        ↓
        observer.percepts
        ↓
        ViewModel
        ↓
        Sublocation Inspector"""