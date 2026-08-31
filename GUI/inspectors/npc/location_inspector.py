#GUI.inspectors.npc.location_inspector.py
#Call inspector for now to match sublocation_inspector.py
#This will eventually have to change as an inspector is the right panel/single click for context info

from GUI.viewmodels.location_viewmodel import LocationViewModel

def build_location_view_model(percept):#eventually put in location_viewmodel.py
    #Likewise, when we eventually improve Sublocation, we may want to move its builder into its ViewModel module.
    data = percept["data"]

    return LocationViewModel(
        name=data.get("name", "Unknown"),
        description=data.get("description", ""),
        info=data.get("region") or "—",
        region=data.get("region"),
        is_open=data.get("is_open", False),
        has_security=data.get("has_security", False),
        security=data.get("security", 0),
        raw=percept.get("origin"),
    )