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
        
        print("\n========== SUBLOCATION FILTER ==========")
        print("Target:", sublocation.name)
        print("========================================")

        rows = []

        for percept in observer.percepts.values():

                data = percept["data"]

                print(
                f"{data.get('type'):20}"
                f"{data.get('name'):25}"
                f" SUB={repr(data.get('sublocation'))}"
                )

                if data.get("sublocation") != sublocation.name:
                        continue

                rows.append(percept)

        print("----------------------------------------")
        print("MATCHED:", len(rows))
        print("========================================\n")

        return rows

        #trying to be cleaner than belongs_to_sublocation()
        # by using percept data alone—but if the object percepts don't yet include "sublocation", it will naturally find nothing.
    
    #The following temporarily replaced with the above code
        """ rows = []

        for percept in observer.percepts.values():

                data = percept["data"]

                if data.get("sublocation") != sublocation.name:
                continue

                rows.append(percept)
                print("\nSUBLOCATION PERCEPTS")
                print("--------------------")

                for row in rows:
                        data = row["data"]

                        print(
                                data.get("type"),
                                data.get("name"),
                                "SUB:",
                                data.get("sublocation"),
                        )
        return rows """

        """ 
        Eventually the GUI should look like

        Simulation
                ↓
        Observation
                ↓
        ViewModel
                ↓
        Inspector

        not

        Simulation
                ↘
        Observation
                ↘
        Inspector """



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