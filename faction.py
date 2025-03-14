from characters import Boss, CEO, Captain, Manager, Employee, GangMember
from goals import Goal
from tasks import Task
import yaml
import json

from base_classes import Character, Location, Faction


class Corporation(Faction):
    def __init__(self, name, violence_disposition):
        super().__init__(name, type="corporation")
        
        self.violence_disposition = violence_disposition
        self.HQ = None

class Gang(Faction):
    def __init__(self, name, violence_disposition, race):
        super().__init__(name, type="gang")
        self.violence_disposition = violence_disposition
        self.HQ = None
        self.race = race
        self.goal_status = None
        self.boss = None
        self.captains = []
        self.members = []
        self.is_street_gang = False

    def add_boss(self, boss):
        if boss.race == self.race:  # Ensure race matches
            self.boss = boss
            boss.faction = self  # Assign faction to the boss
        else:
            raise ValueError(f"Boss race '{boss.race}' does not match gang race '{self.race}'.")

class State(Faction):
    def __init__(self, name, resources, laws, region=None):
        super().__init__(name, type="State")
        self.name = name
        self.resources = resources  # Dictionary of resources (e.g., money, food, etc.)
        self.laws = laws  # List of laws or policies (e.g., "no theft", "tax rates")
        self.type = "The State"
        self.HQ = None 
        self.state_staff = []
        self.members = []

    def update_laws(self, new_law):
        self.laws.append(new_law)
        print(f"New law added: {new_law}")



class GeneralPopulation(Faction):
    def __init__(self, name, violence_disposition):
        super().__init__(name, type="general population")
        self.violence_disposition = violence_disposition
        self.HQ = None
        self.members
#made so that Employee can be instantiated with a faction
