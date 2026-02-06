#region.region.py
from base.core_types import RegionBase
from location.locations import Location
from dataclasses import dataclass, field
from typing import List, Optional
import uuid
@dataclass #when you add things here, update region_knowledge
class Region(RegionBase):
    name: str
    name_for_player: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    wealth: str = "Normal"   
    tags: List[str] = field(default_factory=list)
    shops: List[str] = field(default_factory=list)
    locations: list = field(default_factory=list)
    factions: List[str] = field(default_factory=list)#Strings? ATTN
    cultural_adjectives: List[str] = field(default_factory=list)
    danger_level: any = None
    region_gangs: List = field(default_factory=list) #dataclass syntax.  ensures each instance of Region gets a unique list for region_gangs
    region_street_gangs: List = field(default_factory=list)
    turf_war_triggered: bool = False
    characters_there: List = field(default_factory=list)
    region_corps: List = field(default_factory=list)
    residents: List = field(default_factory=list)
    active_regional_events: List = field(default_factory=list)
    recent_regional_events: List = field(default_factory=list)
    historical_regional_events: List = field(default_factory=list)
    gossip: List = field(default_factory=list)
    economic_info: List = field(default_factory=list)
    
    def __post_init__(self):
        pass#perceptibleMixin removed

    def add_character(self, character):
        if character not in self.characters_there:
            self.characters_there.append(character)
            """ You should register the NPC to a Region once
            After that, their movement between locations should not change Region membership """

    def remove_character(self, character):
        if character in self.characters_there:
            self.characters_there.remove(character)

    def get_percept_data(self, observer=None):
        return {
            "name": self.name,
            "description": f"Region: {self.name}, Wealth: {self.wealth}",
            "type": self.__class__.__name__,
            "origin": self,
            "danger_level": str(self.danger_level) if self.danger_level else "Unknown"
        }

    def list_perceptibles(self):
        # Regions should NOT expose characters_there for perception
        return []

    def get_all_locations(self):
        return self.locations
    
    def get_location_by_name(self, name: str) -> Optional["Location"]:#problem
        for loc in self.locations:
            if loc.name.lower() == name.lower():
                return loc
        return None
        
    def add_location(self, location: Location):#problem
        """Adds a location to this region and updates the location's region reference."""
        location.region = self
        self.locations.append(location)
        from create.create_game_state import get_game_state
        get_game_state().all_locations.append(location)


    def trigger_event(self, event_type: str):
        print(f"Event triggered: {event_type} in {self.name}")
        
    def __repr__(self):
        return f"Region(name='{self.name}')"

    def __str__(self):
        return self.name  # Ensures `str(region)` returns just its name

@dataclass
class UndevelopedRegion(Region):

    def has_security(self):
        return False
    is_open: bool = True
    security_level: int = 0
    name: str
    locations: List[str] = field(default_factory=list)
    factions: List[str] = field(default_factory=list)