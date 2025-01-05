from characters import Boss, CEO, Captain, Grunt, Manager
from goals import Goal
from tasks import Task
import yaml

class Faction:
    def __init__(self, name, type, affiliation=None, goals=None):
        self.name = name
        self.type = type  # "gang" or "corporation"
        self.affiliation = affiliation  # Color or identifier (e.g., "red", "blue")
        self.members = []
        self.current_goal = None
        self.resources = {"money": 1000, "weapons": 10}  # Example default resources
        self.goals = goals or []  # List of faction goals

    def add_member(self, member):
        if member not in self.members:
            self.members.append(member)
            print(f"{member.name} joined {self.name}.")
        else:
            print(f"{member.name} is already a member of {self.name}.")

    def remove_member(self, member, removal_type="voluntary"):
        if member in self.members:
            self.members.remove(member)
            print(f"{member.name} has left {self.name} ({removal_type}).")
        else:
            print(f"{member.name} is not a member of {self.name}.")

    def set_goal(self, goal_type=None):
        """
        Set a new goal for the faction, randomly chosen or specified.
        """
        if goal_type:
            self.current_goal = Goal(goal_type)
        else:
            # Choose a random goal from faction-defined goals
            available_goals = [goal["goal"] for goal in self.goals]
            self.current_goal = Goal(random.choice(available_goals))

        self.current_goal.generate_objectives()
        print(f"{self.name} has set a new goal: {self.current_goal.goal_type.capitalize()}")

    def display_goal(self):
        """
        Display the current goal and its objectives.
        """
        if self.current_goal:
            print(f"Faction: {self.name}, Current Goal: {self.current_goal.goal_type.capitalize()}")
            for i, obj in enumerate(self.current_goal.objectives, 1):
                print(f" Objective {i}: {obj}")
        else:
            print(f"Faction: {self.name} has no active goals.")

    def get_hierarchy(self):
        """
        Returns a dictionary of faction hierarchy, dividing members by their roles.
        """
        hierarchy = {"Boss": [], "Mid-Tier": [], "Grunts": []}
        for member in self.members:
            if isinstance(member, (Boss, CEO)):
                hierarchy["Boss"].append(member)
            elif isinstance(member, (Captain, Manager)):
                hierarchy["Mid-Tier"].append(member)
            else:
                hierarchy["Grunts"].append(member)
        return hierarchy

    def assign_duty(self, member, duty):
        if member in self.members:
            print(f"{member.name} has been assigned to {duty}.")
        else:
            print(f"{member.name} is not a member of {self.name}.")

    def __repr__(self):
        return f"{self.name} ({self.type}, {len(self.members)} members, {self.resources['money']} money)"

class Corporation(Faction):
    def __init__(self, name, identity=None, goals=None):
        super().__init__(name, type="corporation", goals=goals)
        self.identity = identity or "Generic Corporation"

class Gang(Faction):
    def __init__(self, name, affiliation=None, goals=None):
        super().__init__(name, type="gang", affiliation=affiliation, goals=goals)

class State:
    def __init__(self, name, resources, laws):
        self.name = name
        self.resources = resources  # Dictionary of resources (e.g., money, food, etc.)
        self.laws = laws  # List of laws or policies (e.g., "no theft", "tax rates")

    def update_laws(self, new_law):
        self.laws.append(new_law)
        print(f"New law added: {new_law}")

# Utility to load factions from YAML
def load_factions_from_yaml(filepath):
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
    factions = []
    for faction_data in data["factions"]:
        if faction_data["type"] == "corporation":
            factions.append(Corporation(faction_data["name"], goals=faction_data["goals"]))
        elif faction_data["type"] == "gang":
            factions.append(Gang(faction_data["name"], affiliation=faction_data["affiliation"], goals=faction_data["goals"]))
    return factions
