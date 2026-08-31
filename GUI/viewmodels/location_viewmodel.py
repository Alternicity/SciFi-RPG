#GUI.viewmodels.location_viewmodel.py
from dataclasses import dataclass
@dataclass
class LocationViewModel:#We can always change the fields later
    name: str
    description: str
    info: str
    region: str | None
    is_open: bool
    has_security: bool
    security: int
    raw: object