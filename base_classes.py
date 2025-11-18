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
        charisma=10,
        toughness=10,
        observation=10, #1-20 scale
        morale=10,
        status=None,
        loyalties=None,
        custom_skills=None,
        **kwargs,
        
    ):
        #assert hasattr(self, "region"), "region must be set by end of Character.__init__"
        super().__init__()
        #PerceptibleMixin.__init__(self)  # Explicit call instead of super()
        
        from utils import get_region_by_name
        from create_game_state import get_game_state
        from location import Region

        # --- Load global regions early ---
        game_state = get_game_state()
        all_regions = game_state.all_regions

    # --- Assign region first ---
        self.region = get_region_by_name(region, all_regions) if isinstance(region, str) else region
        if not isinstance(self.region, Region):
            raise ValueError(f"Invalid region assigned to character: {region}")

        # --- Assign location and home region ---
        self.location = location

        #new. line 217
        #self._location = None
        #for debugging npc placement/movement, deprecated unless movement debugging needed again, but also see visit_location_auto

        self.current_destination = location
        self.previous_location = None
        self.home_region = self.region
        self.just_arrived = False
        self.just_left_location = False
        
        self.name = name
        self.debug_role = None   # "primary" | "secondary" | "civilian_test" | etc.
        self.is_player = False
        self.is_test_npc = False  # Default to False
        self.is_peaceful_npc = False
        self.has_plot_armour = False# characters should perceive this but not print it to user

        # --- AI initialization (after region is defined) ---

        self.ai = ai  # only assign if provided, don’t auto-create here

        

        self.residences: List[Location] = []

        # --- Validation ---
        assert isinstance(self.region, Region), \
            f"[DEV] {self.name if hasattr(self, 'name') else '?'} region must be a valid Region at end of Character.__init__"
        
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
        self._last_promote_tick = -1 #promoting thoughts to anchor should happen only once
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
        self.anchors = []
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
            "friends": [],#no code yet exists  to populate this
            "enemies": [],
            "allies": [],
            "neutral": [],
            "partners": [partner] if partner else [],#partners exists
        }

        self.isArmed = False
        self.hasRangedWeapon = False
        self.hasMeleeWeapon = False
        
        
        self.workplace: Optional[Location] = None
        self.shift = 'day'  # Can be 'day' or 'night'
        self.is_working = False  # Tracks if the character is working, in world, at a job, or "off duty"
        self.partner = partner
        self.faction = faction
        # Use kwargs to allow overrides, but default to constructor values
        self.fun = kwargs.get("fun", fun)
        self.fun_prefs = None
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

    #new
    #This block for debugging npc location/placement, deprecated, but see visit_location_auto
    """ @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_loc):
        from debug_utils import debug_print
        import inspect
        caller = inspect.stack()[1]
        caller_info = f"{caller.function} @ {caller.filename}:{caller.lineno}"

        old = getattr(self, "_location", None)
        # safe name retrieval: object may not yet have .name during __init__
        obj_name = getattr(self, "name", None) or getattr(self, "id", None) or repr(self)
        old_name = getattr(old, "name", None) or (old.__class__.__name__ if old else None)
        new_name = getattr(new_loc, "name", None) or (new_loc.__class__.__name__ if new_loc else None)

        
        try:
            debug_print(self,
                f"[LOCATION-SET] {obj_name}: {old_name} -> {new_name}  triggered_by={caller_info}",
                category="movement")
        except Exception:
            # swallow any debug errors (keeps init robust); optionally print minimal fallback
            try:
                print(f"[LOCATION-SET-ERR] {obj_name}: {old_name} -> {new_name}  triggered_by={caller_info}")
            except Exception:
                pass
        self._location = new_loc """


    def register_anchor(self, anchor):
        """
        Registers an Anchor with this character.
        """
        if not hasattr(self, "anchors"):
            self.anchors = []

        # filter out None anchors
        if anchor is None:
            return

        if anchor not in self.anchors:
            self.anchors.append(anchor)
            from debug_utils import debug_print
            debug_print(self, f"[ANCHOR] Registered anchor: {anchor.name}", category="anchor")

    def get_preferred_actions(self):
        """Return combined preferences (base + individual)."""
        combined = self.base_preferred_actions.copy()
        combined.update(self.preferred_actions)  # Individual prefs override base
        return combined
    
    @property
    def motivations(self):
        return self.motivation_manager.get_motivations()

    """ @property
    def is_test_npc(self):
        return self.is_test_npc """
    #Delete

    @motivations.setter
    def motivations(self, value):
        raise AttributeError("Use 'motivation_manager.update_motivations()' instead of setting motivations directly.")

    def get_attribute(self, name):
        return getattr(self, name, 0)  # default to 0 if not found

    def has_recently_acquired(self, tag: str):#probably deprecated
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

    def add_percept_from(self, obj):
        """
        Convert an observed object (Character, Item, Location, etc.)
        into a percept entry and add it to this character's percept list.
        """

        # Avoid self-perception (handled separately)
        if obj is self:
            return

        

        # Ask the object for its perceptual data
        percept_data = None
        if hasattr(obj, "get_percept_data"):
            percept_data = obj.get_percept_data(observer=self)
        else:
            # Fallback for non-perceptible objects
            percept_data = {
                "name": getattr(obj, "name", str(obj)),
                "type": obj.__class__.__name__,
                "description": f"{obj.__class__.__name__} (unclassified)",
                "origin": obj,
                "salience": 1.0,
                "tags": [],
                "urgency": 1,
                "source": None,
                "menu_options": [],
            }

        if "name" not in percept_data:
            print(f"[BUG] Object {obj} returned percept with NO name: {percept_data}")
            
        if not percept_data:
            return

        # Store percept by name (unique key)
        # Defensive ensure-name
        name = percept_data.get("name") or getattr(obj, "name", None) or str(obj)

        key = name

        # Initialize percept dict if missing
        if not hasattr(self, "_percepts"):
            self._percepts = {}

        # Add/update percept data
        self._percepts[key] = {
            "data": percept_data,
            "origin": obj
        }

        #from debug_utils import debug_print
        #debug_print(self, f"[PERCEPT ADDED] {self.name} perceived {obj.name} ({obj.__class__.__name__})", category = "percept")
        #verbose

        # Mark percepts as updated
        self.percepts_updated = True

    def observe_region(self, region, include_memory_check=True):
        from location import Region
        #assert isinstance(region, Region), f"[BUG] {self.name} was passed a non-Region as a region: {region} ({type(region)})"
        assert isinstance(region, Region), f"[DEV] {self.name} observe_region got {type(region)} — {region}"

        if not isinstance(region, Region):
            print(f"[BUG] {self.name} was passed {region} of type {type(region).__name__} to observe_region().")
            return

        for loc in region.locations:
            pass

        for char in region.characters_there:
            if char is not self:
                self.perceive_object(char)

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
        
    def observe(self, *, nearby_objects=None, target=None, region=None, location=None):
        """
        Main observation routine for NPCs — clears percepts and gathers new ones from
        characters, objects, and the surrounding region.
        """
        from location import Region, Location
        from debug_utils import debug_print
        from create_game_state import get_game_state
        import inspect
        game_state = get_game_state()
        npc = self

        # caller info for diagnostics
        caller = inspect.stack()[1].function

        # Ensure only runs once per tick
        if getattr(self, "_observed_this_tick", False):
            debug_print(npc, f"[OBSERVE SKIP] already observed this tick={game_state.tick} (caller={caller})", "percept")
            return
        self._observed_this_tick = True

        debug_print(npc, f"[OBSERVE TRACE] {self.name} observing at tick {game_state.tick} (caller={caller})", category="observation")
        debug_print(npc, f"[OBSERVE TRACE] npc.location={npc.location}, region={npc.region}", category="perception")
        #debug_print(npc, f"[OBSERVE] RAW location param={location} (type={type(location)})", "perception")
        if region is not None and location is None:
            print(f"[BUG] observe() called with region but no location! Caller={caller}")

        # --- show before/after counts for easier debugging ---

        try:
            before_count = len(self.percepts)
        except Exception:
            before_count = 0
        debug_print(npc, f"[OBSERVE] Before clearing percepts, count={before_count}, location param={(location.name if location else None)}", "percept")

        # --- clear percepts for new observation cycle ---
        self.percepts.clear()
        self.percepts_update = False

        # --- perceive self (always included) ---
        self_percept = self.get_percept_data(observer=self)
        if self_percept:
            self._percepts["self"] = {
                "data": self_percept,
                "origin": self
            }
            self.percepts_updated = True

        debug_print(self, f"[OBSERVE] Final percept count from oberve() ={len(self.percepts)} at {location.name}", "percept")

        # --- determine current location if not passed ---
        if location is None:
            location = getattr(self, "location", None)

        # If someone passed a Region (bad), fallback to npc.location
        if isinstance(location, Region):
            debug_print(self, "[BUGFIX] observe() received Region instead of Location; switching to self.location", "percept")
            location = npc.location

        if not location:
            debug_print(npc, f"[OBSERVE WARNING] {self.name} has no valid location.", "percept")
            return

        if isinstance(location, Location):

            # --- perceive other characters in the same location ---
            for char in getattr(location, "characters_there", []):
                if char is self:
                    continue
                self.add_percept_from(char)

                """ debug_print(
                npc,
                f"[OBSERVE TRACE] Seeing {other.name} because source={source}",
                category="perception"
                ) """
                #other and source still not defined here

        # --- perceive additional objects if any (location-provided list preferred) ---
        if nearby_objects:
            for obj in nearby_objects:#is this nearby_objects even populated?
                self.add_percept_from(obj)
        else:
            # If caller didn't provide nearby_objects, ask the location for perceptibles.
            if hasattr(location, "list_perceptibles"):
                for obj in location.list_perceptibles():
                    self.add_percept_from(obj)
            else:
                # fallback to worldQueries
                from worldQueries import get_nearby_objects
                for obj in get_nearby_objects(self, region=region, location=location):
                    self.add_percept_from(obj)

        # --- perceive a specific target if requested ---
        if target:
            self.add_percept_from(target)#not used

        # --- mark update complete ---
        self.percepts_updated = True
        final_count = len(self._percepts)
        debug_print(npc, f"[OBSERVE COMPLETE] {self.name} perceived {final_count} entities at {location.name} (tick={game_state.tick})", category="percept")

    def observe_objects(self, nearby_objects=None, location=None, include_inventory_check=False):
        """
        Gathers percepts from nearby Perceptible objects and optionally from the location's inventory.
        Updates self._percepts.
        """
        from debug_utils import debug_print
        debug_print(self, f"[OBSERVE] Before clearing percepts, from observe_objects() object count={len(self.percepts)}", "percept")

        self._percepts.clear()
        new_percepts = {}

        # Auto-fetch nearby objects if not provided
        if hasattr(location, "list_perceptibles"):
            nearby_objects = location.list_perceptibles()
        else:
            nearby_objects = get_nearby_objects(self, region=self.region, location=self.location)


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

        if not any("shop" in p["data"]["tags"] for p in self._percepts.values()):
            print(f"[DEBUG] {self.name}: No shop percepts detected in {self.location.name}")


        self._percepts.update(new_percepts)
        self.percepts_updated = True
        debug_print(self, f"[OBSERVE] Final percept count from observe_objects ={len(self.percepts)} at {location.name}", "percept")

    def perceive_current_location(self):
        """
        Compatibility wrapper: the canonical perception entrypoint is observe().
        Keep this small so code that calls perceive_current_location() still works.
        """
        from debug_utils import debug_print
        if not self.location:
            debug_print(self, f"[WARN] {self.name} tried to perceive with no valid location.", "percept")
            return

        # Delegate entirely to observe(). Do not compute or mutate percept lists here.
        # Pass location and prefer the location's perceptible list if available.
        self.observe(location=self.location, region=self.region)


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
        #this block commented out cos it caps observation
        if len(self._percepts) > self.observation:
            sorted_items = sorted(
                self._percepts.items(), key=lambda kv: kv[1]["data"].get("salience", 0.0), reverse=True
            )
            self._percepts = dict(sorted_items[:self.observation])

    def get_percepts(self, sort_by_salience=True) -> list[dict]:
        #The type hint means: the function returns a list
        #Each item in the list is a dictionary representing a single percept

        #Returns a list of percept dictionaries, optionally sorted by salience (descending).

        percepts = list(self._percepts.values())
        if sort_by_salience:
            percepts.sort(key=lambda p: p.get("salience", 1.0), reverse=True)

        """ sort_by_salience is a legacy pre-anchor system where percepts had a static salience.
            Today, anchor-centric salience has replaced that.
            What should be done?
            Either remove salience values from percepts entirely,
            or keep sort_by_salience=False everywhere (which you already do).
            This part of the system is effectively deprecated. """

        """ keep the list format.
            The dictionary-of-percepts (self._percepts) is an internal store.
            The public API returns a list.
            This is good design: the internal representation may change, the external API does not expose it. """

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

    def list_perceptibles(self):
        items = []

        # Characters
        if hasattr(self, "characters_there"):
            items.extend(self.characters_there)

        # Employees
        if hasattr(self, "employees_there"):
            items.extend(self.employees_there)

        # Loose objects in the world
        if hasattr(self, "objects_present"):
            items.extend(self.objects_present)

        # Shop inventory items
        if hasattr(self, "inventory"):
            for item in getattr(self.inventory, "items", {}).values():
                items.append(item)

        # Cash register
        if hasattr(self, "cash_register"):
            items.append(self.cash_register)

        return [o for o in items if o is not None]

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

