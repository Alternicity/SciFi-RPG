# base/character.py
from base.core_types import CharacterBase
from base.posture import Posture
from base.self_awareness_levels import SelfAwarenessLevel
from perception.perceptibility import PerceptibleMixin
from typing import Callable, Any

class Character(PerceptibleMixin, CharacterBase):
    
    VALID_SEXES = ("male", "female")  # Class-level constant
    VALID_RACES = ("Terran", "Martian", "Italian", "Portuguese", ...)  # Class-level constant

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
        motivations=None,
        preferred_actions=None,
        behaviors=None, #unused, possibly deprecate in favour of preferred_actions, as it overlaps
        partner=None,
        fun=1,# integer attributes have a 1-20 scale
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
        observation=10,
        morale=10,
        status=None,
        loyalties=None,
        custom_skills=None,
        **kwargs,
        
    ):

        super().__init__()

        self.region = region
        self.location = location
        self.current_destination = location
        self.previous_location = None
        self.home_region = None
        self.just_arrived = False
        self.just_left_location = False
        
        self.name = name
        self.first_name = None
        self.family_name = None
        self.family = None # Will hold a Family component later
        self.debug_role = None   # "primary" | "secondary" | "civilian_test" | etc.
        self.is_player = False
        self.is_test_npc = False  # Default to False
        self.is_peaceful_npc = False
        self.has_plot_armour = False#rare, currently unused
        self.ai = ai  # added at instantiation as a component
        self.residences = []
        self.base_preferred_actions = {}
        self._initial_motivations = motivations
        self.motivation_manager = None
        self.skills = self.default_skills()
        # Individual character preferences (overrides base)
        self.preferred_actions = preferred_actions if preferred_actions else {}
        self.is_alert = False
        self.posture = Posture.STANDING
        self.intelligence = intelligence
        self.mind = None
        self.max_thinks_per_tick = kwargs.get("max_thinks_per_tick", 1)
        self._last_promote_tick = -1 #promoting thoughts to anchor should happen only once
        self.curiosity = None
        self.concentration = concentration
        self.task_manager = None#undeveloped system, utilityAI does not use this. Tasks will be recipes issued by high status
        #npcs to their subordinates, please ignore for now.
        self.self_awareness = None
        self.race = race
        self.sex = sex
        self.clothing = None
        self.notable_features = []
        self.bloodstained = None  # Will hold a reference to a Character or a string of name/ID. ie whose blood?
        self.is_visibly_wounded = False
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
        self.current_anchor = None
        self.anchors = []
        self.self_esteem = 50  # Neutral starting value. Goes up with needs met, down with increasing hunger or
        #status loss, or lack of money, or tasks failed, or bad personal events. Currently unused.
        self.observation = kwargs.get("observation", 10)  # Determines perception ability

        # Social connections
        self.social_connections = {
            "friends": [],#no code yet exists  to populate this
            "enemies": [],
            "allies": [],
            "neutral": [],
            "co_workers": [],#If an npc has worked 3 shift with another, then set this
            "partners": [partner] if partner else [],#partners exists
        }

        self.isArmed = False
        self.hasRangedWeapon = False
        self.hasMeleeWeapon = False
        self.employment = None#object added as a component at instantiation, of during sim flow
        self.shift = 'day'  # Can be 'day' or 'night'
        self.is_working = False
        self.just_got_off_shift =False #Just finished a work shift
        self.partner = partner
        self.faction = faction
        self.fun = kwargs.get("fun", fun)#under developed, but some building blocks are in place
        self.fun_prefs = None
        self.hunger = kwargs.get("hunger", hunger)
        self.strength = strength
        self.agility = agility
        self.luck = luck
        self.psy = psy
        self.charisma = charisma
        self.toughness = toughness
        self.morale = morale
        self.status = status
        self.primary_status_domain = kwargs.get("primary_status_domain", "public")
        self.health = 100 + toughness
        self.wallet = None
        self.inventory_component = None
        #I predict this will break all npc.inventory type calls
        # Initialize loyalties as a dictionary
        self.loyalties = kwargs.get("loyalties", {})  # Default to empty dictionary if not provided

    # Assign faction HQ if applicable
        if self.faction and hasattr(self.faction, "HQ"):
            self.current_location = self.faction.HQ  # Ensure faction members start in HQ
        
        self.observation_component = None
        # compatibility shim — DO NOT REMOVE until migration is complete
    @property
    def percepts(self):
        """Compatibility shim.
        Eventually all perception will live inside observation_component.
        For now, if the observation component exists, delegate to it.
        Otherwise fall back to the old _percepts dict.
        """
        if self.observation_component is not None:
            return self.observation_component.percepts
        return self._percepts

    @property
    def inventory(self):
        if self.inventory_component:
            return self.inventory_component.inventory
        return None
    #compatibility property. Needed bc I removed self.inventory

    def register_anchor(self, anchor):
        """
        Registers an Anchor with this character.
        """
        if not hasattr(self, "anchors"):
            self.anchors = []

        # filter out None anchors
        if anchor is None:
            return

    def get_preferred_actions(self):
        """Return combined preferences (base + individual)."""
        combined = self.base_preferred_actions.copy()
        combined.update(self.preferred_actions)  # Individual prefs override base
        return combined
    
    def get_attribute(self, name):
        return getattr(self, name, 0)  # default to 0 if not found
    
    def add_preferred_action(self, action: Callable, target: Any):
        """Add a preferred action for this character."""
        self.preferred_actions[action] = target

    def remove_preferred_action(self, action: Callable):
        """Remove a preferred action."""
        self.preferred_actions.pop(action, None)

    def display_location(self, verbose=False):
        region_name = self.region.name if hasattr(self.region, "name") else str(self.region)
        location_name = self.location.name if hasattr(self.location, "name") else str(self.location)
        sublocation = getattr(self, "sublocation", None)

        if not self.region or not self.location:
            if verbose:
                print(f"Decisions.. {self.name} is in {self.region} but no specific location")
            return f"{region_name}, {location_name}"

        if sublocation:#sublocations is an underdeveloped feature. Basic world structure is regions have locations.
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
        # Basic human-level skills, will likely expand and need to become an npc component
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

    def perceive_current_location(self):
        """
        Compatibility wrapper: the canonical perception entrypoint is observe().
        Keep this small so code that calls perceive_current_location() still works.
        """

        # Delegate entirely to observe(). Do not compute or mutate percept lists here.
        # Pass location and prefer the location's perceptible list if available.
        self.observe(location=self.location, region=self.region)

    def get_percept_data(self, observer=None): #stays here
            #Return perceptual information for this character. Self perception.
            tags = ["human"]

            if self.bloodstained:
                tags.append("bloodstained")
            if self.is_visibly_wounded:
                tags.append("wounded")
                
            return {
                "name": self.name,
                "type": self.__class__.__name__,
                "description": f"{self.name}, a {self.__class__.__name__}",
                "region": self.region.name if getattr(self, "region", None) else "Unknown",
                "location": self.location.name if getattr(self, "location", None) else "Unknown",
                "sublocation": self.sublocation.name if getattr(self, "sublocation", None) else "Unknown",
                "origin": self,

                "tags": tags,
                "urgency": 2,
                "source": None,
                "menu_options": [],
                "has_security": getattr(self, "has_security", lambda: False)()
            }

    def perceive_event(self, percept: dict):
        """
        Called when some external event (like a robbery) forces a perception.
        """
        key = percept["description"] if "description" in percept else f"event_{id(percept)}"
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

    @percepts.setter
    def percepts(self, new_percepts):
        """Compatibility setter.
        If the observation component exists, delegate to it.
        Otherwise fall back to legacy _percepts storage.
        """

        # Validate — percepts must remain dict-like during migration
        if not isinstance(new_percepts, dict):
            raise ValueError("Percepts must be a dict during migration.")

        # If the new observation component is active, store them there
        if self.observation_component is not None:
            # Ensure the component exposes a setter too
            self.observation_component.percepts = new_percepts
            return

        # Otherwise use the legacy storage
        self._percepts = new_percepts

    def update_percepts(self, new_percepts):
        self.observation_component.update_percepts(new_percepts)

    def add_percept_from(self, obj):
        self.observation_component.add_percept_from(obj)

    def get_percepts(self, sort_by_salience=True):
        return self.observation_component.get_percepts(sort_by_salience=sort_by_salience)

    @property
    def whereabouts(self):
        """Returns the character's full whereabouts dynamically."""
        region_name = self.region.name if hasattr(self.region, "name") else self.region
        location_name = self.location.name if hasattr(self.location, "name") else self.location
        sublocation = getattr(self, "_sublocation", None)
        print(f"DEBUG: Accessing whereabouts -> region: {region_name}, location: {location_name}")
        #Elsewhere in the code, print is being deprecated in favor of custom debug_print which has filtering
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
        #unused. partners are set during world creation for now
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




