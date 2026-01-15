# base/location.py
from base.core_types import LocationBase
from dataclasses import dataclass, field
from typing import Callable, Optional, TYPE_CHECKING, List, Any
import uuid

#from location.location_security import Security
""" MUST NOT import Character.
If you need characters → pass references as "Character" type hints under TYPE_CHECKING """

class LocationItems:
    def __init__(self):
        self.objects_present = []
        self.items_available = []

@dataclass
class Location(LocationBase):
    name: str = "Unnamed Location"
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    region: Optional[Any] = None
    items: LocationItems = field(default_factory=LocationItems)#is this used?
    #TMP
    is_shakedown_target: bool = False
    owner = None
    sublocations: Optional[List['Location']] = None
    controlling_faction: Optional[Any] = None
    tags: list[str] = field(default_factory=list)
    menu_options: List[str] = field(default_factory=list)
    security = None#?
    #security: Optional[Any] = None

    #remove
    #objects_present: list[Any] = field(default_factory=list)
    #objects_present now lives in LocationItems
    
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
    is_public_facing: bool = False
    employees_there: list = field(default_factory=list)
    # Instance-specific categories field
    categories: List[str] = field(default_factory=list) #ALERT

    def __post_init__(self):
        
        super().__init__(self.name, tags=getattr(self, "tags", None))
        # initialise structured items container
        #self.items = LocationItems()
        print(">>> Location.__post_init__ CALLED for", self)

        """ With dataclasses, the canonical pattern is:
        define the field with init=False
        initialise it in __post_init__
        This is exactly what __post_init__ is for """

    @property
    def objects_present(self):
        return self.items.objects_present
    
    @objects_present.setter
    def objects_present(self, value):
        self.items.objects_present = value

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
    
    def get_front_of_house_staff(self):
        staff = []
        for c in self.characters_there:
            emp = getattr(c, "employment", None)#is this testing the self /locations attribute? OR just whether characters_there have this?
            if not emp:
                continue
            if emp.workplace is self and emp.role == "front_of_house":
                staff.append(c)
        return staff


    def update_dynamic_ambience(self):
        employees = self.employees_there if isinstance(self, WorkplaceMixin) else []
        total_fun = sum(c.fun for c in self.characters_there + employees)#add the locations fun

        self.ambience.vibes["fun"] = min(total_fun / 100, 1.0)  # normalize to 0-1
        if len(self.characters_there) > 3:
            self.ambience.vibes["social"] = 0.4 + len(self.characters_there) * 0.05

        #Do the following functions need to change to suit a dataclass?
    def list_characters(self, exclude=None):
        if exclude is None:
            exclude = []

        present = []
        if hasattr(self, "characters_there"):
            present += self.characters_there
        if isinstance(self, WorkplaceMixin):
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


