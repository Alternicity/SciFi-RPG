#sublocations.simulation_utils.py
#Do they conform to needed patterns?

from typing import List, Optional, Union, field, Any
from dataclasses import dataclass
from base.location import Sublocation
@dataclass
class HospitalSublocation(Sublocation):
    """Base class for hospital-specific sublocations."""
    accessible_roles: List[str] = field(default_factory=list)

    def get_percept_data(self, observer=None):
        accessible = True
        visible = True
        # marked not defined etc
        """ if observer:
            accessible = can_access_sublocation(observer, self)
            visible = can_perceive_sublocation(observer, self) """

        return {
            "name": self.name,
            "description": getattr(self, "description", self.name),
            "type": self.__class__.__name__,
            "origin": self,
            "accessible": accessible,
            "visible": visible,
            "parent": getattr(self.parent_location, "name", None),
        }


@dataclass
class EmergencyRoom(HospitalSublocation):
    name: str = "Emergency Room"
    description: str = "Bright lights, beeping monitors, and the smell of antiseptic."
    accessible_roles: List[str] = field(default_factory=lambda: ["doctor", "nurse", "patient", "visitor", "security"])

    # Gameplay hooks
    patients_waiting: int = 0
    trauma_bays: int = 6
    is_overcrowded: bool = False


@dataclass
class Morgue(HospitalSublocation):
    name: str = "Morgue"
    description: str = "Cold, silent, and lined with stainless steel drawers. The air hums with refrigeration."
    accessible_roles: List[str] = field(default_factory=lambda: ["doctor", "coroner", "mortician", "security"])

    # Gameplay hooks
    bodies_stored: int = 0
    max_capacity: int = 24
    has_autopsy_room: bool = True
    is_locked: bool = True  # Restricted access
    temperature_celsius: float = 2.0

    def get_percept_data(self, observer=None):
        data = super().get_percept_data(observer)
        data.update({
            "bodies_stored": self.bodies_stored,
            "max_capacity": self.max_capacity,
            "has_autopsy_room": self.has_autopsy_room,
            "is_locked": self.is_locked,
            "temperature_celsius": self.temperature_celsius,
            "spooky": True,
        })
        return data

    @property
    def is_full(self) -> bool:
        return self.bodies_stored >= self.max_capacity

    @property
    def has_space(self) -> bool:
        return self.bodies_stored < self.max_capacity

    def store_body(self, body=None) -> bool:
        """Attempt to store a body. Returns True if successful."""
        if self.is_full:
            return False
        self.bodies_stored += 1
        return True

    def release_body(self) -> bool:
        """Release a body (e.g., to family or authorities)."""
        if self.bodies_stored <= 0:
            return False
        self.bodies_stored -= 1
        return True


@dataclass
class Pharmacy(HospitalSublocation):
    name: str = "Pharmacy"
    description: str = "Shelves of medicine behind a counter. A pharmacist checks prescriptions."
    accessible_roles: List[str] = field(default_factory=lambda: ["doctor", "nurse", "pharmacist", "patient", "security"])

    items_available: List[Any] = field(default_factory=list)
    is_open: bool = True
    requires_prescription: bool = True
    controlled_substances_locked: bool = True


@dataclass
class WaitingRoom(HospitalSublocation):
    name: str = "Waiting Room"
    description: str = "Rows of plastic chairs, old magazines, and a flickering TV."
    accessible_roles: List[str] = field(default_factory=lambda: ["patient", "visitor", "doctor", "nurse", "security"])

    people_waiting: int = 0
    estimated_wait_minutes: int = 45


@dataclass
class OperatingTheatre(HospitalSublocation):
    name: str = "Operating Theatre"
    description: str = "A sterile room with an operating table and surgical lights."
    accessible_roles: List[str] = field(default_factory=lambda: ["surgeon", "doctor", "nurse", "anesthesiologist"])

    is_sterile: bool = True
    surgery_in_progress: bool = False
    equipment_quality: int = 3  # 1-5 scale


@dataclass
class PatientWard(HospitalSublocation):
    name: str = "Patient Ward"
    description: str = "Beds with curtains, patients resting, and the quiet beep of monitors."
    accessible_roles: List[str] = field(default_factory=lambda: ["doctor", "nurse", "patient", "visitor", "security"])

    beds_total: int = 20
    beds_occupied: int = 0
    visiting_hours: bool = True

    @property
    def beds_available(self) -> int:
        return max(0, self.beds_total - self.beds_occupied)
