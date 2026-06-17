#GUI.widgets.sublocation_widget.py
from GUI.viewmodels.sublocation_viewmodel import SublocationViewModel

def build_sublocation_view_model(sublocation):
    return SublocationViewModel(
        name=sublocation.name,
        visible=getattr(sublocation, "visible", False),
        accessible=getattr(sublocation, "accessible", False),
        accessible_roles=getattr(sublocation, "accessible_roles", []),
        raw=sublocation
    )


def render_sublocation_view(parent, vm: SublocationViewModel):
    # clears + draws
    pass