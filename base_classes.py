#base_classes.py
from dataclasses import dataclass, field
from location_security import Security
from typing import Callable, Dict, Optional, TYPE_CHECKING, List, Any
from goals import Goal
import traceback
from enum import Enum, auto
from collections import deque
from tasks import TaskManager
from perceptibility import PerceptibleMixin
from character_mind import Mind
from character_thought import Thought
from ai_utility import UtilityAI
from character_memory import MemoryEntry, Memory, FactionRelatedMemory
import uuid

import time
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

    def get_symbolic_clues(self):
        return ["wears red bandana", "tattoo on neck", "corp ID badge"]
    
    def __repr__(self):
        return f"{self.name} {self.type.capitalize()}"
    
class Factionless(Faction):
    def __init__(self, name="Factionless", violence_disposition="Low"):
        super().__init__(name=name, type="neutral")
        self.violence_disposition = violence_disposition
        self.HQ = None
        self.goals = []
        self.current_goal = None
        self.resources = {}
        self.region = None
        self.members = []

class Character(PerceptibleMixin):

    VALID_SEXES = ("male", "female")  # Class-level constant
    VALID_RACES = ("Terran", "Martian", "Italian", "Portuguese", "Irish", "French", "Chinese", "German", "BlackAmerican", "Indian", "IndoAryan", "IranianPersian", "Japanese", "WhiteAryanNordic")  # Class-level constant

    is_concrete = False
    def __init__(
        self,
        name,
        race,
        sex,
        region,
        location,
        is_player=False,
        ai=None,
        wallet=None,
        motivations=None,
        preferred_actions=None,
        behaviors=None, #possibly deprecate in favour of preferred_actions, as it overlaps
        partner=None,
        fun=1,
        hunger=1,
        faction=None,
        strength=10,
        agility=10,
        intelligence=10,
        luck=10,
        psy=10,
        charisma=10, #1-20
        toughness=10,
        observation=10, #1-20 scale
        morale=10,
        status=None,
        loyalties=None,# Default is None; initializes as a dictionary later
        custom_skills=None,
        **kwargs,
        
    ):
        #print(f"[Character Init] name={name}, race={race}, sex={sex}")
        #verbose, prints all characters

        #initialization code
        self.name = name
        self.is_player = False
        self.is_test_npc = False  # Default to False
        if not self.is_player:
            
            self.ai = ai or UtilityAI(self)
        else:
            self.ai = None

        from utils import get_region_by_name #line 150
        from create_game_state import get_game_state
        game_state = get_game_state()
        all_regions = game_state.all_regions

        from location import Region
        self.region = get_region_by_name(region, all_regions) if isinstance(region, str) else region
        if not isinstance(self.region, Region):
            raise ValueError(f"Invalid region assigned to character: {region}")
        
        self.location = location
        # Default preferred actions (subclasses can extend this)
        self.base_preferred_actions = {}

        self.skills = self.default_skills()
        """ if custom_skills:
            self.skills.update(custom_skills) """

        # Individual character preferences (overrides base)
        self.preferred_actions = preferred_actions if preferred_actions else {}
        self.is_alert = False
        from behaviours import set_default_behaviour, BehaviourManager
        self.behaviors = set(behaviors) if behaviors else set_default_behaviour()
        self.behaviour_manager = BehaviourManager()
        self.posture = Posture.STANDING
        
        self.memory = Memory()  # Handles both episodic and semantic memory now

        self.task_manager = TaskManager(self)
        

        """ Should Tasks Be Stored in Memory?
        Yes, that makes a lot of sense — but with separation of concerns:

        Memory stores past and ongoing tasks for recall, journaling, or planning.

        tasks[] list should still exist for actively assigned or planned tasks (like a task queue). """

        self.self_awareness_score = 0
        self.self_awareness_level = SelfAwarenessLevel.ANIMAL
        self.intelligence = intelligence

        #self.mind = Mind(maxlen=self.intelligence)
        self.mind = Mind(owner=self, capacity=self.intelligence)

        self._percepts = {}
        self.percepts_updated = False

        self.race = race
        self.sex = sex
        self.clothing = None
        self.notable_features = []
        self.bloodstained = None  # Will hold a reference to a Character or a string of name/ID
        self.is_visibly_wounded = False
        
        # Appearance traits
        #If you want self.appearance to always reflect the latest values of self.race, 
        #self.sex, etc., you can make it a @property, but your current method is fine if 
        #you're OK with updating it manually when needed.
        self.overall_impression = None
        self.appearance = {
        "race": self.race,
        "sex": self.sex,
        "clothing": self.clothing,
        "notable_features": self.notable_features,
        "bloodstained": self.bloodstained,  # This can be None, a Character, or a string
        "is_visibly_wounded": self.is_visibly_wounded,
        "overall_impression": self.overall_impression  # To be updated by observers
    }

        # Add faction clues later (safely)
        if hasattr(self, "faction") and self.faction:
            self.appearance["faction_semiotics"] = self.faction.get_symbolic_clues()
        else:
            self.appearance["faction_semiotics"] = []


        from motivation import MotivationManager, Motivation

        self.motivation_manager = MotivationManager(self)
        if motivations:
            for m in motivations:
                if isinstance(m, Motivation):
                    self.motivation_manager.motivations.append(m)
                else:
                    # assume tuple (type, urgency)
                    self.motivation_manager.update_motivations(m[0], m[1])

        

        self.self_esteem = 50  # Neutral starting value. Goes up with needs met, down with increasing hunger or
        #status loss, or lack of money, or tasks failed, or baf personal events
        from status import StatusLevel, CharacterStatus, FactionStatus

        # If status isn't passed, assign a new CharacterStatus instance
        self.status = status if status is not None else CharacterStatus()
        
        self.primary_status_domain = kwargs.get("primary_status_domain", "public")
        self.status.set_status("public", FactionStatus(StatusLevel.LOW, "Unknown"))
        self.status.set_status("criminal", FactionStatus(StatusLevel.MID, "Midd"))
        self.status.set_status("corporate", FactionStatus(StatusLevel.NONE, None))
        self.status.set_status("state", FactionStatus(StatusLevel.NONE, None))
        
        self.observation = kwargs.get("observation", 10)  # Determines perception ability
        self.attention_focus = None
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
        
        self.luck = luck
        self.psy = psy
        self.charisma = charisma
        self.toughness = toughness
        self.morale = morale
        self.status = status  # Add status here
        
        # Check for accidental shadowing of the motivations property
        if "motivations" in self.__dict__:
            print(f"[WARNING] motivations instance attribute exists on {self.name}. Full traceback:")
            print("\n" + "="*30 + f"\n[WARNING] motivations shadowed on {self.name}\n" + "="*30)
            traceback.print_stack()

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
        """ if not self.faction:
            raise ValueError("Faction must be specified for a character.") """
        #remove 
        
        self.health = 100 + toughness
        
        from InWorldObjects import Wallet
        self.wallet = wallet if wallet else Wallet()
        #print(f"[DEBUG, from class Character] {self.name} wallet: {self.wallet.bankCardCash}")

        from inventory import Inventory
        self.inventory = kwargs.get("inventory", Inventory(owner=self))

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
    
    @property
    def motivations(self):
        return self.motivation_manager.get_motivations()

    @motivations.setter
    def motivations(self, value):
        raise AttributeError("Use 'motivation_manager.update_motivations()' instead of setting motivations directly.")

    def get_attribute(self, name):
        return getattr(self, name, 0)  # default to 0 if not found

    def add_preferred_action(self, action: Callable, target: Any):
        """Add a preferred action for this character."""
        self.preferred_actions[action] = target

    def remove_preferred_action(self, action: Callable):
        """Remove a preferred action."""
        self.preferred_actions.pop(action, None)

    def remember_task(self, task): #Remember your TOP task
        self.memory.append({
            "type": "task",
            "name": task.name,
            "time": "now",  # or use game clock
            "status": task.status,
        })

    """ def convert_legacy_motivations(motivations):
        if isinstance(motivations, dict):
            print(f"[INFO] Legacy initial_motivations format used.")
            print("[TRACE] Where legacy format was passed:")
            traceback.print_stack(limit=5)
            return list(motivations.items())
        return motivations """

    def receive_task(self, task):
        self.tasks.append(task)
        print(f"{self.name} is now handling task: '{task}'.")

    def display_location(self, verbose=False):
        region_name = self.region.name if hasattr(self.region, "name") else str(self.region)
        location_name = self.location.name if hasattr(self.location, "name") else str(self.location)
        sublocation = getattr(self, "sublocation", None)

        if not self.region or not self.location:
            if verbose:
                print(f"Decisions.. {self.name} is in {self.region} but no specific location")
            return f"{region_name}, {location_name}"

        if sublocation:
            return f"{region_name}, {location_name}, {sublocation}"
        return f"{region_name}, {location_name}"
    
    def get_appearance_description(self):
        parts = []
        if self.appearance.get("bloodstained"):
            parts.append("bloodstained")
        if self.appearance.get("is_visibly_wounded"):
            parts.append("wounded")

        parts.append(self.race)
        parts.append(self.sex)

        clothing = self.appearance.get("clothing", "indistinct clothing")
        if clothing:
            parts.append(f"wearing {clothing}")

        features = self.appearance.get("notable_features", [])
        if features:
            parts.extend(features)

        faction_clues = self.appearance.get("faction_semiotics", [])
        if faction_clues:
            parts.append(f"faction symbols: {', '.join(faction_clues)}")

        return " ".join(filter(None, parts))
    
    def default_skills(self):
        # Basic human-level skills
        return {
            "stealth": 4,
            "melee_attack": 2,
            "melee_defend": 3,
            "dodge": 2,
            "persuasion": 5,
            "threaten": 3,
            "complain": 7,
        }
    
    def alert(self, instigator):
        print(f"{self.name} has been alerted by {instigator.name}!")
        self.is_alert = True
        
    def get_skill(self, skill_name):
        return self.skills.get(skill_name, 1)  # Minimum 1

    """ Motivations are inputs or drives

    Utility AI is the decision engine

    Tasks are outputs or choices selected by that engine """

    @property
    def motivations(self):
        """Returns motivations in a formatted way for display."""
        return self.motivation_manager.get_motivations()
    
    def get_percept_data(self, observer=None):
        #You can abstract this into a helper method later

        tags = ["human"]
        salience = 1  # baseline

        if self.bloodstained:
            tags.append("bloodstained")
            salience += 5
        if self.is_visibly_wounded:
            tags.append("wounded")
            salience += 10

        if observer and "violence" in getattr(observer, "motivations", []):
            salience += 2  # violence-oriented characters notice more

        return {
            "description": f"{self.name} (Character)",
            "origin": self,
            "urgency": 2,
            "tags": tags,
            "source": None,
            "salience": salience
        }

    def observe(self, nearby_objects=None, target=None, region=None, location=None):
        print(f"[Observe] {self.name} is observing objects in {location.name if location else 'unknown'}")

        if nearby_objects is None:
            from worldQueries import get_nearby_objects
            nearby_objects = get_nearby_objects(self, region, location)

        new_percepts = {}

        # Clear existing percepts or comment out if you want to accumulate
        # self._percepts.clear()

        for obj in nearby_objects:
            if isinstance(obj, PerceptibleMixin):
                percept = obj.get_percept_data(observer=self)
                if percept:
                    # Use obj.id as dictionary key (string, hashable)
                    new_percepts[obj.id] = percept

                    print(f"[Observe] Found perceptible: {obj} → {percept['description']}")
                    print(f"[Observe] {self.name} perceived: {percept['description']} with salience {percept['salience']}")

        # Self-perception - store under special key 'self'
        self_percept = self.get_percept_data(observer=self)
        if self_percept:
            new_percepts["self"] = {'data': self_percept, 'salience': self_percept["salience"]}

        # Replace old percepts with the new dict keyed by IDs
        self._percepts = new_percepts

        self.percepts_updated = True
        print(f"[Observe, last line] {self.name} now has {len(self._percepts)} percepts.")


    @property
    def percepts(self):
        """Dynamically generates percepts with actionable hints. allows behavior trees or utility-based AI 
        to “poll” the characters perception of the world without storing stale data. Its like their short-term
          awareness. percepts are what the character is noticing right now."""
        #types> characters, events, utility, factions, locations, regions, chainOfActions
        #percepts, must include actual object references for the "origin" field

        updated_percepts = {} #not accessed, deprecated?

        #should the following code be moved elsewhere out of class Character, it looks like placeholder code that
        #would need to grow very long.

        #Keep this simple and side-effect free:
        #If you want fancier output later (e.g., filtered by urgency), create a get_high_salience_percepts() 
        #method instead.
        return self._percepts
    
    """     Example percept dict:
        {
    "description": "There is a riot in Sector 3",
    "origin": riot_event_object,
    "urgency": 5,
    "tags": ["violence", "threat"],
    "source": None,
    "salience": 17
    } """

    def perceive_event(self, percept: dict):
        """
        Called when some external event (like a robbery) forces a perception.
        """
        key = percept.get("description", f"event_{id(percept)}")
        # Merge it in, respecting salience, etc.
        self.update_percepts([percept])

    @percepts.setter
    def percepts(self, new_percepts):
        """Allows setting percepts."""
        if isinstance(new_percepts, dict):
            self._percepts = new_percepts ##Try Without
        else:
            raise ValueError("Percepts must be a dict..")
        #Something here needs to convert percepts into think() creating Thought object and memories

    def update_percepts(self, new_percepts: list[dict]):
        """
        Merge or update percepts based on salience and replace logic.
        """
        for p in new_percepts:
            key = p.get("id") or str(p)  # or hashable unique representation
            salience = p.get("salience", 1)

            if key in self._percepts:
                # Keep the more salient percept
                if salience > self._percepts[key]['salience']:
                    self._percepts[key] = {'data': p, 'salience': salience}
            else:
                self._percepts[key] = {'data': p, 'salience': salience}

        # Optionally prune to observation capacity
        if len(self._percepts) > self.observation:
            # Keep top-N salience only
            sorted_items = sorted(self._percepts.items(), key=lambda kv: kv[1]['salience'], reverse=True)
            self._percepts = dict(sorted_items[:self.observation])

    def get_percepts(self, sort_by_salience=True) -> list[dict]:
        """
        Returns a list of percept dictionaries, optionally sorted by salience (descending).
        """
        percepts = list(self._percepts.values())

        if sort_by_salience:
            percepts = sorted(percepts, key=lambda p: p.get('salience', 0), reverse=True)

        return percepts
    

    @property
    def whereabouts(self):
        """Returns the character's full whereabouts dynamically."""
        region_name = self.region.name if hasattr(self.region, "name") else self.region
        location_name = self.location.name if hasattr(self.location, "name") else self.location
        sublocation = getattr(self, "_sublocation", None)
        print(f"DEBUG: Accessing whereabouts -> region: {region_name}, location: {location_name}")
        return f"{region_name}, {location_name}" + (f", {sublocation}" if sublocation else "")

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

    def calculate_self_awareness(self):
        score = 0
        score += len(self.memory) * 0.5  # More memory, more reflective
        score += self.psy * 0.75         # Psy sensitivity
        if self.has_autonomous_goals():
            score += 2
        if self.detects_pattern_glitches():
            score += 1.5
        if self.reflects_on_failures():
            score += 1

        self.self_awareness_score = round(score, 2)
        self.update_awareness_level()

    def update_awareness_level(self):
        if self.self_awareness_score < 2:
            self.self_awareness_level = SelfAwarenessLevel.ANIMAL
        elif self.self_awareness_score < 4:
            self.self_awareness_level = SelfAwarenessLevel.BASIC
        elif self.self_awareness_score < 6:
            self.self_awareness_level = SelfAwarenessLevel.PERSONAL
        elif self.self_awareness_score < 8:
            self.self_awareness_level = SelfAwarenessLevel.REFLECTIVE
        elif self.self_awareness_score < 10:
            self.self_awareness_level = SelfAwarenessLevel.META
        else:
            self.self_awareness_level = SelfAwarenessLevel.TRANSCENDENT

    @property
    def bankCardCash(self):
        return self.wallet.bankCardCash

    @property
    def cash(self):
        return self.wallet.cash

    def __repr__(self):
        """ whereabouts_value = self.whereabouts  # Ensure evaluation
        print(f"🔍 Debug: whereabouts = {whereabouts_value}")  # Now prints the actual value
    """     
        
        return (
            f"{self.name} "
            f"(Faction: {self.faction.name if self.faction else 'None'}, "
            f"Cash: {self.wallet.cash}, "
            f"BankCard: {self.wallet.bankCardCash}, "
            f"Fun: {self.fun}, Hunger: {self.hunger})"
        )
    
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
        return self.location.region

    def get_current_location(self):
        """Get the current location within the region."""
        return self.location.location

        #About the Underscore _
        """ Yes — the leading underscore isn't magical, but it's a common convention meaning “internal use only”. It helps:
        Avoid name clashes with properties (self._motivations vs self.motivations)
        Signal “dont touch this unless you know what youre doing”
        Work nicely with @property decorators """



        

class SelfAwarenessLevel:
    ANIMAL = 0        # Instinctual
    BASIC = 1         # Recognizes self vs other
    PERSONAL = 2      # Understands goals/memory
    REFLECTIVE = 3    # Understands self in time
    META = 4          # Realizes they are inside a system
    TRANSCENDENT = 5  # Can access/change "reality" (aether etc.)


@dataclass
class Location(PerceptibleMixin):
    name: str = "Unnamed Location"
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    region: Optional['Region'] = None
    child_location: Optional['Location'] = None  # Specific location within the location
    
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
    robbable: bool = False
    is_open: bool = True
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

    def has_security(self):
        return False

    @property
    def security_level(self):
        return 0


    def get_percept_data(self, observer=None):
        tags = ["location"]
        salience = 1

        if self.security and self.security.level > 1:
            tags.append("secure")

        return {
            "description": f"{self.name} (Location)",
            "origin": self,
            "urgency": 1,
            "tags": tags,
            "source": None,
            "salience": salience
        }


    def get_menu_options(self, character):
        """Returns only the static menu options defined in a location."""
        return self.menu_options  # No need to involve dynamic_options here
        #I still dont understand why we need a function for this, rather than lists of options in each subclass, like shop
        #returns a list - self.menu_options
    
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

