# base/location.py
from base.core_types import LocationBase
from dataclasses import dataclass, field
from typing import Callable, Optional, TYPE_CHECKING, List, Any
import uuid

#from location.location_security import Security
""" MUST NOT import Character.
If you need characters → pass references as "Character" type hints under TYPE_CHECKING """
@dataclass
class Location(LocationBase):
    name: str = "Unnamed Location"
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    region: Optional[Any] = None

    #TMP
    is_shakedown_target: bool = False
    owner = None
    sublocations: Optional[List['Location']] = None
    controlling_faction: Optional[Any] = None
    tags: list[str] = field(default_factory=list)
    menu_options: List[str] = field(default_factory=list)
    security = None#?
    #security: Optional[Any] = None

    objects_present: list[Any] = field(default_factory=list)

    robbable: bool = False
    is_open: bool = True
    condition: str = "Clean"
    fun: int = 0
    is_concrete: bool = False
    secret_entrance: bool = False
    entrance: List[str] = field(default_factory=list)  # Default to an empty list
    upkeep: int = 0
    CATEGORIES = ["residential", "workplace", "public"]
    is_workplace: bool = False
    characters_there: list = field(default_factory=list)  # Tracks characters present at this location
    recent_arrivals: list = field(default_factory=list)

    employees_there: list = field(default_factory=list)
    # Instance-specific categories field
    categories: List[str] = field(default_factory=list) #ALERT

    def __post_init__(self):
        PerceptibleMixin.__init__(self)  # Ensure mixin init is called

    def has_security(self):
        return self.security and (
            self.security.level > 1 or
            self.security.surveillance or
            self.security.alarm_system or
            len(self.security.guards) > 0
        )

    @property
    def security_level(self):
        return self.security.level if self.security else 0

    def get_menu_options(self, character):
        """Returns only the static menu options defined in a location.
        For player centric program flow"""
        return self.menu_options  # No need to involve dynamic_options here

    
    def __post_init__(self):
        # Any additional setup logic if needed
        pass
    
        #Do the following functions need to change to suit a dataclass?
    def list_characters(self, exclude=None):
        if exclude is None:
            exclude = []

        present = []
        if hasattr(self, "characters_there"):
            present += self.characters_there
        if hasattr(self, "employees_there"):
            present += self.employees_there

        # Remove excluded
        present = [c for c in present if c not in exclude]
        return present

    def has_category(self, category):
        return category in self.categories
    
    def add_entrance(self, *entrance):
        self.entrance.extend(entrance)
        print(f"entrance added to {self.name}: {', '.join(entrance)}")

    def has_item(self, item_name: str) -> bool:
        return any(obj.name.lower() == item_name.lower() for obj in self.objects_present)

    def to_dict(self):
        return {"name": self.name, "region": self.region.name if self.region else "None"}


    def __repr__(self):
        return f"{self.name}"  # Just return the name directly