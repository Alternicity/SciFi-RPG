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
    both panels render the same model
    no Tkinter logic leaks into game logic
    formatting rules live in one place """

#utility functions
def get_sublocation_percepts(observer, sublocation):

    rows = []

    for percept in observer.percepts.values():

        if percept.get("origin") is not sublocation:
            continue

        rows.append(percept)

    return rows