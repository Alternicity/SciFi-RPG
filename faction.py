from characters import Boss, CEO, Captain, Manager, Employee, GangMember
from goals import Goal
from tasks import Task

from base_classes import Character, Location, Faction


class Corporation(Faction):
    def __init__(self, name, violence_disposition):
        super().__init__(name, type="corporation")
        
        self.violence_disposition = violence_disposition
        self.HQ = None

        # New attributes
        self.CEO = None
        self.managers = []
        self.accountants = []
        self.security = []
        self.employees = []
        self.members = []  # All employees, accountants, security, managers (not CEO)

    def add_CEO(self, ceo):
        self.CEO = ceo

    def add_manager(self, manager):
        self.managers.append(manager)
        self.members.append(manager)

    def add_accountant(self, accountant):
        self.accountants.append(accountant)
        self.members.append(accountant)

    def add_security(self, guard):
        self.security.append(guard)
        self.members.append(guard)

    def add_employee(self, employee):
        self.employees.append(employee)
        self.members.append(employee)

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
        super().__init__(name, type="state")
        self.name = name
        self.resources = resources  # Dictionary of resources (e.g., money, food, etc.)
        self.laws = laws  # List of laws or policies (e.g., "no theft", "tax rates")
        self.type = "state"
        self.HQ = None 
        self.state_staff = []
        self.members = []

     

    def update_laws(self, new_law):
        self.laws.append(new_law)
        print(f"New law added: {new_law}")


class FactionRelationship: #update class Faction to have a container for the object, and game_state
    def __init__(self, other_faction, hostility=0, trust=5, is_public=True, is_frenemy=False):
        self.other_faction = other_faction  # Could be object or name
        self.hostility = hostility  # 0-10 scale
        self.trust = trust          # 0-10 scale
        self.is_public = is_public
        self.is_frenemy = is_frenemy

    def adjust_trust(self, amount):
        self.trust = max(0, min(10, self.trust + amount))

    def adjust_hostility(self, amount):
        self.hostility = max(0, min(10, self.hostility + amount))

    def summary(self):
        status = "Ally" if self.trust > 7 else "Neutral"
        if self.hostility > 6:
            status = "Enemy"
        if self.is_frenemy:
            status = "Frenemy"
        return f"{self.other_faction.name}: {status} (Trust {self.trust}, Hostility {self.hostility})"



""" class GeneralPopulation(Faction):
    def __init__(self, name, violence_disposition):
        super().__init__(name, type="general population")
        self.violence_disposition = violence_disposition
        self.HQ = None
        self.members """
#made so that Employee can be instantiated with a faction
