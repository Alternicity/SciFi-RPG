from characters import Boss, CEO, Captain, Grunt, Manager
from goals import Goal
from tasks import Task


class Faction:
    def __init__(
        self,
        name,
        type,
    ):
        self.name = name
        self.type = type  # gang or corporation
        self.members = []
        self.current_goal = None  # Current faction goal
        self.resources = {"money": 1000, "weapons": 10}  # Example resources

    def add_member(self, member):
        self.members.append(member)

    def set_goal(self, goal_type=None):
        """
        Set a new goal for the faction.
        """
        self.current_goal = Goal(goal_type)
        self.current_goal.generate_objectives()
        print(
            f"{self.name} has set a new goal: {self.current_goal.goal_type.capitalize()}"
        )

    def display_goal(self):
        """
        Display the current goal and its objectives.
        """
        if self.current_goal:
            print(
                f"Faction: {self.name}, Current Goal: {self.current_goal.goal_type.capitalize()}"
            )
            for i, obj in enumerate(self.current_goal.objectives, 1):
                print(f" Objective {i}: {obj}")
        else:
            print(f"Faction: {self.name} has no active goals.")

    def get_hierarchy(self):
        hierarchy = {"Boss": [], "Mid-Tier": [], "Grunts": []}
        for member in self.members:
            if isinstance(member, (Boss, CEO)):
                hierarchy["Boss"].append(member)
            elif isinstance(member, (Captain, Manager)):
                hierarchy["Mid-Tier"].append(member)
            else:
                hierarchy["Grunts"].append(member)
        return hierarchy

    def __repr__(self):
        return f"{self.name} ({self.type} with {len(self.members)} members"

    def addMember(self, member):
        if member not in self.members:
            self.members.append(member)
            print(f"{member.name} joined {self.name}.")
        else:
            print(f"{member.name} is already in {self.name}.")

    def removeMember(self, member, removal_type):
        if member in self.members:
            self.members.remove(member)
            print(f"{member.name} left {self.name} ({removal_type}).")
        else:
            print(f"{member.name} is not in {self.name}.")

    def assignDuty(self, member, duty):
        if member in self.members:
            print(f"{member.name} has been assigned to {duty}.")
        else:
            print(f"{member.name} is not in {self.name}.")


class Corporation(Faction):
    def __init__(self, name, identity=None):
        super().__init__(name, type)
        self.identity = identity or "Generic Corporation"

    # identity = (Globetek, Hannival, UltraEngine, Saquia)


class Gang(Faction):
    def __init__(self, name, affiliation):
        super().__init__(name)
        self.affiliation = affiliation


class Civilian:
    def __init__(self, name, role, faction=None, loyalty=0):
        self.name = name
        self.role = role  # e.g., "worker", "merchant", "spy"
        self.faction = faction  # Faction they belong to, if any
        self.loyalty = loyalty  # Loyalty to the faction or state (0 to 100)

    def update_loyalty(self, amount):
        self.loyalty = max(0, min(100, self.loyalty + amount))
        print(f"{self.name}'s loyalty is now {self.loyalty}.")


class State:
    def __init__(self, name, resources, laws):
        self.name = name
        self.resources = resources  # Dictionary of resources (e.g., money, food, etc.)
        self.laws = laws  # List of laws or policies (e.g., "no theft", "tax rates")

    def update_laws(self, new_law):
        self.laws.append(new_law)
        print(f"New law added: {new_law}")
