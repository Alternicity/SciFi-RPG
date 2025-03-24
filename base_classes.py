#base_classes.py
from dataclasses import dataclass, field
from location_security import Security
from typing import Callable, Dict, Optional, TYPE_CHECKING, List, Any
from goals import Goal
import traceback
from enum import Enum, auto
if TYPE_CHECKING:
    from location import Region
DEBUG_MODE = False  # Set to True when debugging

class Posture(Enum):
    STANDING = auto()
    SITTING = auto()
    LYING = auto()

class Faction:
    def __init__(self, name, type):
        self.name = name
        self.type = type  # "gang" or "corporation"
        
        self.members = []
        #Expand Attributes: Use nested dictionaries if factions need even more data about members.
        self.goals = []  # List of active goals
        self.current_goal = None
        self.Testconst = "Test"
        self.resources = {"money": 1000, "weapons": 10}  # Example default resources
        
        self.region = None

    def add_member(self, member, rank="low", wage=100, perceived_loyalty=1.0):
        if not hasattr(member, "name"):
            print(f"Invalid member object: {member}")
            return
        if member.name in self.members:
            print(f"{member.name} is already a member of {self.name}.")
        else:
            self.members[member.name] = {
                "object": member,
                "rank": rank,
                "wage": wage,
                "perceived_loyalty": perceived_loyalty,
            }
            print(f"{member.name} joined {self.name} as {rank}.")
            print(f"DEBUG: Adding member object: {member} (Type: {type(member)})")

            #faction neutral ranks are: low, mid, high

    def remove_member(self, member_name, removal_type="voluntary"):
        if member_name in self.members:
            del self.members[member_name]
            print(f"{member_name} has left {self.name} ({removal_type}).")
        else:
            print(f"{member_name} is not a member of {self.name}.")

    def set_goal(self, goal):
        """
        Set a new goal for the faction, randomly chosen or specified.
        """
        self.goals.append(goal)
        self.current_goal = goal
        self.current_goal.generate_objectives()
        #print(f"{self.name} has set a new goal: {self.current_goal.goal_type.capitalize()}")

        #possiblz deprecated
        """ from goals import Goal
        if goal_type:
            self.current_goal = Goal(goal_type)
        else:
            # Choose a random goal from faction-defined goals
            available_goals = [goal["goal"] for goal in self.goals]
            self.current_goal = Goal(random.choice(available_goals))

        self.current_goal.generate_objectives()
        print(f"{self.name} has set a new goal: {self.current_goal.goal_type.capitalize()}") """

    def display_current_goal(self):
        """
        Display the current priority goal and its objectives.
        """
        if self.current_goal:
            print(f"Faction: {self.name}, Current Goal: {self.current_goal.goal_type.capitalize()}")
            for i, obj in enumerate(self.current_goal.objectives, 1):
                print(f" Objective {i}: {obj}")
        else:
            print(f"Faction: {self.name} has no active goals.")

    def update_goals(self):
        """Update all faction goals."""
        for goal in self.goals:
            if not goal.is_completed():
                print(f"Updating goal: {goal.description}")
                # Add logic to check progress or adapt to changes

    def list_members(self):
        print(f"Members of {self.name}:")
        for member_name, data in self.members.items():
            rank = data["rank"]
            print(f"- {member_name} (Rank: {rank})")

    def assign_duty(self, member, duty):
        if member in self.members:
            print(f"{member.name} has been assigned to {duty}.")
        else:
            print(f"{member.name} is not a member of {self.name}.")

    def __repr__(self):
        return f"{self.name} {self.type.capitalize()}"
    

class Character:

    VALID_SEXES = ("male", "female")  # Class-level constant
    VALID_RACES = ("Terran", "Martian", "Italian", "Portuguese", "Irish", "French", "Chinese", "German", "BlackAmerican", "Indian", "IndoAryan", "IranianPersian", "Japanese", "WhiteAryanNordic")  # Class-level constant

    is_concrete = False
    def __init__(
        self,
        name,
        region,
        location,
        initial_motivations=None,
        preferred_actions=None,
        behaviors=None,
        partner=None, #greyed from here
        bankCardCash=0,
        fun=1,
        hunger=1,
        faction=None,
        strength=10,
        agility=10,
        intelligence=10,
        luck=10,
        psy=10,
        charisma=10,
        toughness=10,
        observation=10, 
        morale=10,
        race="Terran",
        sex="male", # change
        status=None,
        loyalties=None,  # Default is None; initializes as a dictionary later
        **kwargs,
        
    ):
        #initialization code
        self.name = name
        self.is_player = False
        from utils import get_region_by_name #line 150
        from create_game_state import game_state  
        all_regions = game_state.all_regions

        from location import Region
        region_obj = get_region_by_name(region, all_regions) if isinstance(region, str) else region
        if not isinstance(region_obj, Region):
            raise ValueError(f"Invalid region assigned to character: {region}")
        self.region = region_obj


        self.initial_motivations = initial_motivations or []
        self.location = location
        # Default preferred actions (subclasses can extend this)
        self.base_preferred_actions = {}  
        
        # Individual character preferences (overrides base)
        self.preferred_actions = preferred_actions if preferred_actions else {}

        from behaviours import set_default_behaviour, BehaviourManager
        self.behaviors = set(behaviors) if behaviors else set_default_behaviour()
        self.behaviour_manager = BehaviourManager()
        self.posture = Posture.STANDING
        self.self_esteem = 50  # Neutral starting value. Goes up with needs met, down with increasing hunger or
        #status loss, or lack of money, or tasks failed, or baf personal events
        self.is_visibly_wounded = False

        self.needs = kwargs.get("needs", {"physiological": 10, "safety": 8, "love_belonging": 7, "esteem": 5,
            "self_actualization": 2,})  # Example defaults
        
        from motivation import MotivationManager
        self.motivation_manager = MotivationManager(self)  # NEW: Handles motivation logic
        # Update motivations on creation
        self.motivation_manager.update_motivations()


        # Tasks (individual objectives, replacing "goals")
        self.tasks = kwargs.get("tasks", [])

        # Perception-related attributes
        self.percepts = {}  # List of things character notices (e.g., dangers, opportunities)
                            #Key = Percept, Value = Weight of how attention grabbing it is
                            #This should be  dynamically updating, like whereabouts
                            #So does it need an @property function?
                            # if you want percepts to always be dynamically updated when accessed, you should 
                            # use @property. If it's just a list that updates via a function, then it's not necessary.
        
        self.observation = kwargs.get("observation", 10)  # Determines perception ability

        # Social connections
        self.social_connections = {
            "friends": [],
            "enemies": [],
            "allies": [],
            "partners": [partner] if partner else [],
        }
        #many things marked undefined after here, the entries aftre t equals sign
        self.shift = 'day'  # Can be 'day' or 'night'
        self.is_working = False  # Tracks if the character is working
        self.partner = partner
        self.faction = faction
        # Use kwargs to allow overrides, but default to constructor values
        self.fun = kwargs.get("fun", fun)
        self.hunger = kwargs.get("hunger", hunger)
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.luck = luck
        self.psy = psy
        self.charisma = charisma
        self.toughness = toughness
        self.morale = morale
        self.race = race
        self.sex = sex
        self.status = status  # Add status here
        
        if sex not in self.VALID_SEXES:
            raise ValueError(
                f"Invalid sex: {sex}. Valid options are {self.VALID_SEXES}"
            )
        # variables to begin with lowercase letter, unlike Classes
        if race not in self.VALID_RACES:
            raise ValueError(
                f"Invalid race: {race}. Valid options are {self.VALID_RACES}"
            )

        # Validate that faction is provided
        if not self.faction:
            raise ValueError("Faction must be specified for a character.")
        self.weapon = None
        self.health = 100 + toughness
        self.bankCardCash = bankCardCash
        #self.wallet = Wallet(cash=50, bankCardCash=100)  # Initialize with some default values
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory 
        # Initialize loyalties as a dictionary
        self.loyalties = kwargs.get("loyalties", {})  # Default to empty dictionary if not provided

        # Handle other attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Assign faction HQ if applicable
        if self.faction and hasattr(self.faction, "HQ"):
            self.current_location = self.faction.HQ  # Ensure faction members start in HQ
    def get_preferred_actions(self):
        """Return combined preferences (base + individual)."""
        combined = self.base_preferred_actions.copy()
        combined.update(self.preferred_actions)  # Individual prefs override base
        return combined

    def add_preferred_action(self, action: Callable, target: Any):
        """Add a preferred action for this character."""
        self.preferred_actions[action] = target

    def remove_preferred_action(self, action: Callable):
        """Remove a preferred action."""
        self.preferred_actions.pop(action, None)
    
    @property
    def motivations(self):
        """Returns motivations in a formatted way for display."""
        return self.motivation_manager.get_motivations()

    def update_motivations(self):
        """Triggers motivation recalculation."""
        self.motivation_manager.update_motivations()
        #possibly deprecated for motivations.py or at least the names are confusingly the same

    @property
    def whereabouts(self):
        """Returns the character's full whereabouts dynamically."""
        region_name = self.region.name if hasattr(self.region, "name") else self.region
        location_name = self.location.name if hasattr(self.location, "name") else self.location
        sublocation = getattr(self, "_sublocation", None)
        return f"{region_name}, {location_name}" + (f", {sublocation}" if sublocation else "")


    @whereabouts.setter
    def whereabouts(self, new_location):
        """Allows modifying whereabouts, handling region, location, and optional sublocation."""
        parts = new_location.split(", ")
        self._region = parts[0] if len(parts) > 0 else "Unknown"
        self._location = parts[1] if len(parts) > 1 else "Unknown"
        self._sublocation = parts[2] if len(parts) > 2 else None  # Future-proofing
                                        
    @property
    def percepts(self):
        """Dynamically generates percepts with actionable hints."""
        updated_percepts = {}
        if self.observation > 5:
            updated_percepts["Nearby Friend"] = {"weight": 8, "suggested_actions": ["Talk", "Trade"]}
            updated_percepts["Loud Noise"] = {"weight": 6, "suggested_actions": ["Investigate"]}
        if self.observation > 8:
            updated_percepts["Hidden Enemy"] = {"weight": 4, "suggested_actions": ["Ambush", "Avoid"]}
        return updated_percepts


    @percepts.setter
    def percepts(self, new_percepts):
        """Allows setting percepts."""
        if isinstance(new_percepts, dict):
            self._percepts = new_percepts
        else:
            raise ValueError("Percepts must be a dictionary of {percept: weight}.")

    def adjust_self_esteem(self, amount):
        self.self_esteem = max(0, min(100, self.self_esteem + amount))

    def prefers_action(self, action):
        """Check if an action aligns with the character's behaviors."""
        action_behavior_map = {
            "Eat": "Eating",
            "Steal": "Thievy",
            "Talk": "Social",
        }
        return action_behavior_map.get(action) in self.behaviors

    def __repr__(self):
        """ whereabouts_value = self.whereabouts  # Ensure evaluation
        print(f"🔍 Debug: whereabouts = {whereabouts_value}")  # Now prints the actual value
    """     
        
        return f"{self.name} (Faction: {self.faction}, Cash: {self.bankCardCash}, Fun: {self.fun}, Hunger: {self.hunger})"
    
    def get_loyalty(self, group):
        """
        Get the loyalty level to a specific group. Returns 0 if the group is not in the dictionary.
        """
        return self.loyalties.get(group, 0)

    def update_loyalty(self, group, amount):
        """
        Update the loyalty to a specific group. If the group is not in the dictionary, add it.
        """
        self.loyalties[group] = self.loyalties.get(group, 0) + amount
        #if loyalty goes <0 a treachery event might be triggered

    def set_partner(self, partner):
        """
        Sets the partner attribute.

        :param partner: A Character object or None.
        """
        if partner is None or isinstance(partner, Character):
            self.partner = partner
        else:
            raise ValueError("Partner must be a Character object or None.")

    def remove_partner(self):
        """Removes the partner (sets it to None)."""
        self.partner = None

    def update_location(self, region, location):
        """Update the character's current location."""
        self.current_location.region = region
        self.current_location.location = location

    def get_current_region(self):
        """Get the current region."""
        return self.current_location.region

    def get_current_location(self):
        """Get the current location within the region."""
        return self.current_location.location


@dataclass
class Location:
    region: Optional['Region'] = None
    location: Optional['Location'] = None  # Specific location within the location
    name: str = "Unnamed Location"
    menu_options: List[str] = field(default_factory=list)
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))
    from InWorldObjects import ObjectInWorld #check for circular import 
    objects_present: list[ObjectInWorld] = field(default_factory=list)

    condition: str = "Unknown Condition"
    fun: int = 0
    is_concrete: bool = False
    secret_entrance: bool = False
    entrance: List[str] = field(default_factory=list)  # Default to an empty list
    upkeep: int = 0
    CATEGORIES = ["residential", "workplace", "public"]
    is_workplace: bool = False
    characters_there: list = field(default_factory=list)  # Tracks characters present at this location
    employees_there: list = field(default_factory=list)
    # Instance-specific categories field
    categories: List[str] = field(default_factory=list) #ALERT

    def get_menu_options(self, character):
        """Returns only the static menu options defined in a location."""
        return self.menu_options  # No need to involve dynamic_options here
        #I still dont understand why we need a function for this, rather than lists of options in each subclass, like shop
        #returns a list - self.menu_options
    @property
    def stealable_items(self) -> list[ObjectInWorld]:
        """Return a list of stealable items present at this location."""
        return [obj for obj in self.objects_present if obj.is_stealable]

    @property
    def has_stealable_items(self) -> bool:
        """Check if there are any stealable items in the location."""
        return bool(self.stealable_items)
    
    def __post_init__(self):
        # Any additional setup logic if needed
        pass
    
        #Do the following functions need to change to suit a dataclass?
    def list_characters(self):
        """List characters currently at the location."""
        return self.characters

    def has_category(self, category):
        return category in self.categories
    
    def add_entrance(self, *entrance):
        self.entrance.extend(entrance)
        print(f"entrance added to {self.name}: {', '.join(entrance)}")

    def to_dict(self):
        return {"name": self.name, "region": self.region.name if self.region else "None"}


    def __repr__(self):
        return f"Location({self.name})"

