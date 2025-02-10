#base_classes.py
from dataclasses import dataclass, field
from location_security import Security
from typing import Optional
from typing import List
from goals import Goal



class Faction:
    def __init__(self, name, type, affiliation=None):
        self.name = name
        self.type = type  # "gang" or "corporation"
        self.affiliation = affiliation  # Color or identifier (e.g., "red", "blue")
        self.members = {}
        #Expand Attributes: Use nested dictionaries if factions need even more data about members.
        self.goals = []  # List of active goals
        self.current_goal = None
        self.resources = {"money": 1000, "weapons": 10}  # Example default resources
        self.startingRegion = None
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

    def set_goal(self, current_goal):
        """
        Set a new goal for the faction, randomly chosen or specified.
        """
        self.goals.append(current_goal)
        print(f"Goal '{current_goal.description}' added to {self.name}.")

        #possiblz deprecated 
        if goal_type:
            self.current_goal = Goal(goal_type)
        else:
            # Choose a random goal from faction-defined goals
            available_goals = [goal["goal"] for goal in self.goals]
            self.current_goal = Goal(random.choice(available_goals))

        self.current_goal.generate_objectives()
        print(f"{self.name} has set a new goal: {self.current_goal.goal_type.capitalize()}")

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
        return f"{self.name} ({self.type}, {len(self.members)} members, {self.resources['money']} money)"


class Character:

    VALID_SEXES = ("male", "female")  # Class-level constant
    VALID_RACES = ("Terran", "Martian", "Italian", "Portuguese", "French", "Chinese", "German", "Indian", "IndoAryan", "IranianPersian", "Japanese")  # Class-level constant

    is_concrete = False
    def __init__(
        self,
        name,
        start_region,
        start_location,
        initial_motivations=None,
        partner=None,
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
        morale=10,
        race="Terran",
        sex="male",
        status=None,
        loyalties=None,  # Default is None; initializes as a dictionary later
        **kwargs,
    ):
        from motivation import Motivation
        if initial_motivations is None or not initial_motivations:
            initial_motivations = ["earn_money"]  # Ensure at least one valid motivation
        # Ensure we only initialize valid motivations
        self.motivations = [Motivation(m) for m in initial_motivations if m in Motivation.VALID_MOTIVATIONS]
        
        #initialization code
        self.name = name
        self.start_location = start_location
        self.current_region = start_region  
        self.current_location = start_location
        
        self.needs = {
            "physiological": 10, 
            "safety": 8,
            "love_belonging": 7,
            "esteem": 5,
            "self_actualization": 2,
        }

        # Store motivations as objects, not strings
        from motivation import Motivation  # Avoid circular import issues
        self.motivations = (
            [Motivation(m) for m in initial_motivations]
            if initial_motivations
            else []
        )
        self.update_motivations()



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
        self.motivations = kwargs.get(
            "motivations", []
        )  # Use kwargs safely to add extra attributes
        # validation
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
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.toughness = toughness
        self.morale = morale
        self.health = 100 + toughness
        self.bankCardCash = bankCardCash
        #self.wallet = Wallet(cash=50, bankCardCash=100)  # Initialize with some default values
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        self.status = status  # LOW, MID, HIGH, ELITE 
        # Initialize loyalties as a dictionary
        self.loyalties = kwargs.get("loyalties", {})  # Default to empty dictionary if not provided

        # Handle other attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Assign faction HQ if applicable
        if self.faction and hasattr(self.faction, "HQ"):
            self.current_location = self.faction.HQ  # Ensure faction members start in HQ

    def update_motivations(self):
        """Updates motivations based on needs."""
        from motivation import Motivation  # Ensure Motivation is imported
        self.motivations.clear()  # Reset motivations

        if self.needs["physiological"] > 7:
            self.motivations.extend([Motivation("eat"), Motivation("sleep"), Motivation("shelter")])

        if self.needs["safety"] > 7:
            self.motivations.append(Motivation("find_safety"))

        if self.needs["love_belonging"] > 7:
            self.motivations.append(Motivation("seek_friends"))

        if self.needs["esteem"] > 7:
            self.motivations.append(Motivation("gain_status"))

        if self.needs["self_actualization"] > 7:
            self.motivations.append(Motivation("pursue_dreams"))

    @property
    def whereabouts(self):
        """Returns whereabouts as 'Region, Location, Sublocation' or just 'Region, Location' or 'Region'."""
        parts = [
        self.current_region if self.current_region else "Unknown Region"
        ]
        if self.current_location:
            parts.append(self.current_location)
        if getattr(self, "current_sublocation", None):  # Safe way to check if the attribute exists
            parts.append(self.current_sublocation)
        return ", ".join(parts)

    def __repr__(self):
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
    region: Optional['Region'] = None  # Reference to the Region object
    location: Optional['Location'] = None  # Specific location within the region (optional)
    name: str = "Unnamed Location"
    side: str = "Unknown Side" # marked for project wide deletion
    security: Security = field(default_factory=lambda: Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    ))
    condition: str = "Unknown Condition"
    fun: int = 0
    is_concrete: bool = False
    secret_entrance: bool = False
    entrance: List[str] = field(default_factory=list)  # Default to an empty list
    upkeep: int = 0

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):
        # Any additional setup logic if needed
        pass

    def add_entrance(self, *entrance):
        self.entrance.extend(entrance)
        print(f"entrance added to {self.name}: {', '.join(entrance)}")

# Decorator to check entrance state
""" def check_entrance_state(func):
    def wrapper(self, *args, **kwargs):
        if self.secret_entrance:
            print(f"Accessing secret entrance to {self.name}.")
            return func(self, *args, **kwargs)
        else:
            print(f"Secret entrance not available at {self.name}.")
            return None
    return wrapper """