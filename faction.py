from characters import Boss, CEO, Captain, Manager, Employee, GangMember
from goals import Goal
from tasks import Task
import yaml
import json

from base_classes import Character, Location, Faction


class Corporation(Faction):
    def __init__(self, name, violence_disposition, identity=None):
        super().__init__(name, type="corporation")
        self.identity = identity or "Generic Corporation"
        self.violence_disposition = violence_disposition
        self.HQ = None

class Gang(Faction):
    def __init__(self, name, violence_disposition, affiliation=None):
        super().__init__(name, type="gang", affiliation=affiliation)
        self.violence_disposition = violence_disposition
        self.HQ = None

class State:
    def __init__(self, name, resources, laws, region=None):
        self.name = name
        self.resources = resources  # Dictionary of resources (e.g., money, food, etc.)
        self.laws = laws  # List of laws or policies (e.g., "no theft", "tax rates")
        self.type = "The State"
        self.HQ = None 
        self.region = region

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
            faction = Corporation(faction_data["name"], goals=faction_data["goals"])
        elif faction_data["type"] == "gang":
            faction = Gang(faction_data["name"], affiliation=faction_data["affiliation"], goals=faction_data["goals"])
        
        # Add members
        for member_data in faction_data.get("members", []):
            if member_data["role"] == "Boss":
                member = Boss(member_data["name"], **member_data["attributes"])
            elif member_data["role"] == "Captain":
                member = Captain(member_data["name"], **member_data["attributes"])
            elif member_data["role"] == "GangMember":
                member = GangMember(member_data["name"], **member_data["attributes"])
            faction.add_member(member)
        
        factions.append(faction)
    return factions


#print(f"{faction.name} operates in the following locations: {locations}")
