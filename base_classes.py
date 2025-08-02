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
from character_mind import Mind, Curiosity
from character_thought import Thought
from ai_utility import UtilityAI

#from location import Region
#tmp? debug use

import uuid
from worldQueries import observe_location, get_nearby_objects

import time
if TYPE_CHECKING:
    from location import Region
DEBUG_MODE = False  # Set to True when debugging

class Posture(Enum):
    STANDING = auto()
    SITTING = auto()
    LYING = auto()

class Faction:
    def __init__(self, name, type, violence_disposition="1"):
        self.name = name
        self.type = type  # "gang" or "corporation"
        self.members = []
        #Expand Attributes: Use nested dictionaries if factions need even more data about members.
        self.goals = []  # List of active goals
        self.current_goal = None
        self.resources = {"money": 1000, "weapons": 10}  # Example default resources
        self.region = None
        self.is_vengeful = False
        self.violence_disposition = violence_disposition
        self.enemies = {}  # Key: Faction name or object, Value: hostility level 1-10

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

    def add_enemy(self, other_faction, hostility=5):
        self.enemies[other_faction.name] = hostility

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
    
    def increase_violence(self, amount=1):
        self.violence_disposition = min(10, self.violence_disposition + amount)

    def decrease_violence(self, amount=1):
        self.violence_disposition = max(0, self.violence_disposition - amount)

    def violence_level_description(self):
        if self.violence_disposition >= 7:
            return "High"
        elif self.violence_disposition >= 4:
            return "Medium"
        return "Low"

    def __repr__(self):
        return f"{self.name} {self.type.capitalize()}"
    
class Factionless(Faction):
    def __init__(self, name="Factionless", violence_disposition="1"):
        super().__init__(name=name, type="neutral")
        self.violence_disposition = violence_disposition
        self.HQ = None
        self.goals = []
        self.current_goal = None
        self.resources = {}
        self.region = None
        self.members = []

class Character(PerceptibleMixin):
    #keep PerceptibleMixin at the start of the base class list

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
        concentration = 10,
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
        super().__init__()
        #PerceptibleMixin.__init__(self)  # Explicit call instead of super()


        #print(f"[Character Init] name={name}, race={race}, sex={sex}")
        #verbose, prints all characters

        #initialization code
        self.name = name
        self.is_player = False
        self.is_test_npc = False  # Default to False
        self.is_peaceful_npc = False
        self.has_plot_armour = False# characters should perceive this but not print it to user

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
        self.home_region = self.region
        self.residences: List[Location] = []
        
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

        self.intelligence = intelligence
        self.mind = Mind(owner=self, capacity=intelligence)
        self.max_thinks_per_tick = kwargs.get("max_thinks_per_tick", 1)
        self.curiosity = Curiosity(base_score=self.intelligence // 2)
        self.concentration = concentration

        self.task_manager = TaskManager(self)
        """ Should Tasks Be Stored in Memory?
        Yes, that makes a lot of sense — but with separation of concerns:

        Memory stores past and ongoing tasks for recall, journaling, or planning.

        tasks[] list should still exist for actively assigned or planned tasks (like a task queue). """

        self.self_awareness_score = 0
        self.self_awareness_level = SelfAwarenessLevel.ANIMAL
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

        self.current_anchor = None
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
        
        # Social connections
        self.social_connections = {
            "friends": [],
            "enemies": [],
            "allies": [],
            "neutral": [],
            "partners": [partner] if partner else [],
        }

        self.isArmed = False
        self.hasRangedWeapon = False
        self.hasMeleeWeapon = False
        self.just_arrived = False
        self.workplace: Optional[Location] = None
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

    def has_recently_acquired(self, tag: str):
        return self.inventory and any(tag in item.tags for item in self.inventory.recently_acquired)

    def add_preferred_action(self, action: Callable, target: Any):
        """Add a preferred action for this character."""
        self.preferred_actions[action] = target

    def remove_preferred_action(self, action: Callable):
        """Remove a preferred action."""
        self.preferred_actions.pop(action, None)

    def remember_task(self, task): #Remember your TOP task
        self.mind.memory.append({
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
        """
        Return perceptual information for this character.
        Subclasses should call super().get_percept_data(observer)
        and then override or extend fields as needed.
        """

        tags = ["human"]
        salience = 1.0  # baseline salience

        if self.bloodstained:
            tags.append("bloodstained")
            salience += 5.0
        if self.is_visibly_wounded:
            tags.append("wounded")
            salience += 5.0 #Anchor refactor: salience to what?

        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "description": f"{self.name}, a {self.__class__.__name__}",
            "region": self.region.name if getattr(self, "region", None) else "Unknown",
            "location": self.location.name if getattr(self, "location", None) else "Unknown",
            "sublocation": self.sublocation.name if getattr(self, "sublocation", None) else "Unknown",
            "origin": self,
            "salience": salience,
            "tags": tags,
            "urgency": 2,
            "source": None,
            "menu_options": [],
            "has_security": getattr(self, "has_security", lambda: False)()
        }

    def observe_region(self, region, include_memory_check=True, include_inventory_check=False):
        from location import Region
        #assert isinstance(region, Region), f"[BUG] {self.name} was passed a non-Region as a region: {region} ({type(region)})"
        assert isinstance(region, Region), f"[DEV] {self.name} observe_region got {type(region)} — {region}"

        if not isinstance(region, Region):
            print(f"[BUG] {self.name} was passed {region} of type {type(region).__name__} to observe_region().")
            return

        for loc in region.locations:  #line530
            pass  # observe_location(self, loc)

        for char in region.characters_there:
            if char is not self:
                self.perceive_object(char)

        #should not be inside observe_region() unless you want memory injection to
        #  happen every time the region is observed.
        #Move to character instantiation, later add a lesser version for child or stupid characters
        #a one-time call like initialize_knowledge() during startup / setup.
            from memory_entry import RegionKnowledge
            rk = RegionKnowledge(
                region_name=region.name,
                character_or_faction=self,
                tags = ["gangs", "region", "street_gang"],
                region_gangs={g.name for g in region.region_gangs},
                is_street_gang=any(getattr(g, "is_street_gang", False) for g in region.region_gangs),
            )
            self.mind.memory.semantic.setdefault("region_knowledge", []).append(rk)

            for gang in region.region_gangs: #line 534
                self.mind.memory.semantic.setdefault("factions", []).append(gang)

                # Form thought if hostile
                if gang.name != self.faction.name:
                    self._remember_hostile_faction(gang, region)

            for gang in region.region_street_gangs:
                if gang.name != self.faction.name:
                    self._remember_hostile_faction(gang, region)

        # Trigger subclass reaction if it exists
        if hasattr(self, "handle_observation"):
            self.handle_observation(region)

        if include_inventory_check and self.location and hasattr(self.location, "inventory"):#line 587
            #include_inventory_check is marked as not defined, it needs to be passed in from the call
            for item in self.location.inventory.items.values():
                if isinstance(item, PerceptibleMixin):
                    percept = item.get_percept_data(observer=self)
                    if percept:
                        self._percepts[item.id] = {
                            "data": percept,
                            "origin": item
                    }
        
    def observe(self, *, nearby_objects=None, target=None, region=None, location=None):
        from location import Region, Location#line 609
        if isinstance(region, Location):
            region = region.region
        if not isinstance(region, Region):
            raise TypeError(f"[DEV] {self.name} observe_region got invalid region type {type(region)} — {region}")
            #will this block exclude nearby_objects from the subsequent call to observe_objects()?
        if self.is_test_npc:
            simple_list = [f"{c.name}, {c.__class__.__name__}" for c in location.characters_there]
            #print(f"[DEBUG] {self.name} observe() called, count these: {simple_list}")
        
        self.observe_region(region, include_memory_check=True, include_inventory_check=True)
        self.observe_objects(nearby_objects=nearby_objects, location=location, include_inventory_check=True)

        # Main perception logic for a character NPC.
        region = region or self.region
        location = location or getattr(self, "location", None) 
        
        # Observe specific location if provided
        if location:
            observe_location(self, location)

            # Perceive self
            self_percept = self.get_percept_data(observer=self)
            if self_percept:
                new_percepts = {}
                new_percepts["self"] = {
                    "data": self_percept,
                    "origin": self
                }
                self._percepts.update(new_percepts)
                self.percepts_updated = True

            #print(f"[Observe] {self.name} now has {len(self._percepts)} percepts.")

    def observe_objects(self, nearby_objects=None, location=None, include_inventory_check=False):
        """
        Gathers percepts from nearby Perceptible objects and optionally from the location's inventory.
        Updates self._percepts.
        """
        self._percepts.clear()
        new_percepts = {}

        # Auto-fetch nearby objects if not provided
        if nearby_objects is None and location:
            from worldQueries import get_nearby_objects
            nearby_objects = get_nearby_objects(self, region=self.region, location=location)
        else:
            nearby_objects = nearby_objects or []

        # Perceive items from the location's inventory (if enabled)
        if include_inventory_check and location and hasattr(location, "inventory"):
            for item in location.inventory.items.values():
                if isinstance(item, PerceptibleMixin):
                    percept = item.get_percept_data(observer=self)
                    if percept:
                        new_percepts[item.id] = {
                            "data": percept,
                            "origin": item
                        }

        # Perceive nearby loose objects (including employees, characters, containers, etc.)
        for obj in nearby_objects:
            if isinstance(obj, PerceptibleMixin):
                percept = obj.get_percept_data(observer=self)
                if percept:
                    new_percepts[obj.id] = {
                        "data": percept,
                        "origin": obj
                    }
                else:
                    print(f"[BUG] {obj.name} ({type(obj).__name__}) returned None from get_percept_data.")

        self._percepts.update(new_percepts)
        self.percepts_updated = True

    def perceive_current_location(self):
        if self.location:
            self.observe(
                nearby_objects=self.location.characters_there,
                location=self.location,
                region=self.region
                #You can extend it later to trigger memory, thoughts, logging, or other perception mechanics
            )

    def _remember_hostile_faction(self, gang, region):
        hostile_thought = Thought(
            content=f"Enemy gang {gang.name} is here...",
            subject=gang,
            origin=region.name,
            urgency=5,
            tags=["gang", "hostile"],
            source="ThreatDetection",
            timestamp=time.time()
        )

        #self.mind.add(hostile_thought)
        self.mind.memory.semantic.setdefault("enemies", []).append(hostile_thought)
        self.is_alert = True

        if hasattr(self, 'utility_ai'):
            self.utility_ai.evaluate_thought_for_threats(hostile_thought)

    @property
    def percepts(self):
        """Dynamically generates percepts with actionable hints. allows behavior trees or utility-based AI 
        to “poll” the characters perception of the world without storing stale data. Its like their short-term
          awareness. percepts are what the character is noticing right now."""
        #types> characters, events, utility, factions, locations, regions, chainOfActions
        #percepts, must include actual object references for the "origin" field

        updated_percepts = {} #not accessed, deprecated? line 689

        #should the following code be moved elsewhere out of class Character, it looks like placeholder code that
        #would need to grow very long.

        #Keep this simple and side-effect free:
        #If you want fancier output later (e.g., filtered by urgency), create a get_high_salience_percepts() 
        #method instead.
        return self._percepts or {}
    
    """     Example percept dict:
        {
    "description": "There is a riot in Sector 3",
    "origin": riot_event_object,
    "urgency": 5,
    "tags": ["violence", "threat"],
    "source": None,
    "salience": 1.3
    } """

    def perceive_event(self, percept: dict):
        """
        Called when some external event (like a robbery) forces a perception.
        """
        key = percept["description"] if "description" in percept else f"event_{id(percept)}"
        # Merge it in, respecting salience, etc.
        self.update_percepts([percept])

    def perceive_object(self, obj):
        """
        Perceive an object in the world. Can be overridden by subclasses.
        """
        if isinstance(obj, PerceptibleMixin):
            percept = obj.get_percept_data(observer=self)
            if percept:
                self.update_percepts([percept])

                if 'description' not in percept:
                    print(f"ERROR: Object {obj} (type: {type(obj)}) has no 'description' key in its percept: {percept}")
                #print(f"[{self.name}] perceived object: {percept['description']}")

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
        Update the character's internal percept dictionary with new percepts.
        Each percept must be wrapped as {"data": ..., "origin": ...}
        If only a raw percept is passed, this will auto-wrap it using origin = data.get("origin").
        """

        for p in new_percepts:
            # Auto-wrap flat percepts if needed
            if "data" not in p:
                wrapped = {
                    "data": p,
                    "origin": p.get("origin", None)
                }
            else:
                wrapped = p

            data = wrapped["data"]
            origin = wrapped.get("origin", data.get("origin", None))

            # Validate required fields
            if not isinstance(data, dict):
                print(f"[WARNING] Percept data is not a dict: {data}")
                continue
            if "description" not in data:
                print(f"[WARNING] Percept missing description: {data}")
            if origin is None:
                print(f"[WARNING] Percept missing origin: {data}")

            key = getattr(origin, "id", None) or data.get("id") or str(origin)
            salience = data.get("salience", 1.0)

            # Keep the more salient version if duplicate
            if key in self._percepts:
                if salience > self._percepts[key]["data"].get("salience", 0.0):
                    self._percepts[key] = {"data": data, "origin": origin}
            else:
                self._percepts[key] = {"data": data, "origin": origin}

        # Prune by salience to observation capacity
        if len(self._percepts) > self.observation:
            sorted_items = sorted(
                self._percepts.items(), key=lambda kv: kv[1]["data"].get("salience", 0.0), reverse=True
            )
            self._percepts = dict(sorted_items[:self.observation])

    def get_percepts(self, sort_by_salience=True) -> list[dict]:
        """
        Returns a list of percept dictionaries, optionally sorted by salience (descending).
        """
        percepts = list(self._percepts.values())
        if sort_by_salience:
            percepts.sort(key=lambda p: p.get("salience", 1.0), reverse=True)

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
        score += len(self.mind.memory.capacity) * 0.5  # More memory, more reflective
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

        """def __repr__(self):
         return (
            f"{self.name} "
            f"(Faction: {self.faction.name if self.faction else 'None'}, "
            f"Cash: {self.wallet.cash}, "
            f"BankCard: {self.wallet.bankCardCash}, "
            f"Fun: {self.fun}, Hunger: {self.hunger})"
        ) """

    #could possibly show "Location: None" if location is missing or explicitly set to None
    def __repr__(self):
        return f"<Character: {self.name}, Location: {getattr(self, 'location', 'Unknown')}>"
    
    
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

    sublocations: Optional[List['Location']] = None  # Specific location within the location
    controlling_faction: Optional[Faction] = None

    tags: list[str] = field(default_factory=list)
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


    def get_percept_data(self, observer=None):
        tags = ["location"]
        salience = 1.0

        if self.security and self.security.level > 1:
            tags.append("secure")

        if self.controlling_faction and self.controlling_faction.is_vengeful():
            tags.append("rival_faction")

        return {
            "description": f"{self.name} (Location)",
            "type": self.__class__.__name__,
            "origin": self,
            "urgency": 1,
            "tags": tags,
            "source": None,
            "salience": salience,
            "robbable": self.robbable,
            "has_security": self.has_security(),
            "security_level": self.security_level
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

