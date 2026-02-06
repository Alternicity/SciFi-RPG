# base/faction.py
from base.core_types import FactionBase
from debug_utils import debug_print

class Faction(FactionBase):
    def __init__(self, name, type, violence_disposition=1):
        super().__init__(name=name, tags=[])
        self.name = name
        self.type = type  # "gang" or "corporation"
        self.members = {}#changed
        #Expand Attributes: Use nested dictionaries if factions need even more data about members.
        self.goals = []  # List of active goals
        self.current_goal = None
        self.resources = {"money": 1000, "weapons": 10}  # unused
        self.region = None
        self.is_vengeful = False
        self.violence_disposition = violence_disposition
        self.enemies = {}  # Key: Faction name or object, Value: hostility level 1-10

    def add_member(self, member, rank="low", wage=100, perceived_loyalty=1.0):
        if not hasattr(member, "name"):

            debug_print(member, f"[ERROR] Invalid member object: {member}", category="ERROR")

            
            return
        if member.name in self.members:

            debug_print(member, f"[FACTION] {member.name} is already a member of: {self.name}", category="FACTION")
        else:
            self.members[member.name] = {
                "object": member,
                "rank": rank,#for now rank just defaults to low. rank is a placeholder
                "wage": wage,
                "perceived_loyalty": perceived_loyalty,
            }

            debug_print(member, f"[FACTION] Adds member: {member.name} as {rank}.", category="FACTION")

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

    def display_current_goal(self):
        """
        Display the current priority goal and its objectives.
        """
        if self.current_goal:
            print(f"Faction: {self.name}, Current Goal: {self.current_goal.goal_type.capitalize()} Also debug me")
            for i, obj in enumerate(self.current_goal.objectives, 1):
                print(f" Objective {i}: {obj}")
        else:
            print(f"Faction: {self.name} has no active goals. Also debug me")

    def update_goals(self):
        """Update all faction goals."""
        for goal in self.goals:
            if not goal.is_completed():
                print(f"Updating goal: {goal.description} Also debug me")
                # Add logic to check progress or adapt to changes

    def list_members(self):
        print(f"Members of {self.name}:")
        for member_name, data in self.members.items():
            rank = data["rank"]
            print(f"- {member_name} (Rank: {rank}) Also debug me")

    def assign_duty(self, member, duty):
        if member.name in self.members:
            print(f"{member.name} has been assigned to {duty}. Also debug me")
        else:
            print(f"{member.name} is not a member of {self.name}. Also debug me")

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
    def __init__(self, name="Factionless", violence_disposition=1):
        super().__init__(name=name, type="neutral")
        self.violence_disposition = violence_disposition
        self.HQ = None
        self.goals = []
        self.current_goal = None
        self.resources = {}
        self.region = None
        self.members = {}#changed, see above