from enum import IntEnum

class StatusLevel(IntEnum):
    NONE = 0
    LOW = 1
    MID = 2
    HIGH = 3
    ELITE = 4

    
class CharacterStatus:
    def __init__(self):
        # Keys can be "public", "gang", "corp_name", etc.
        self.status = {}

    def set_status(self, domain, status_obj):
        self.status[domain] = status_obj

    def get_status(self, domain):
        return self.status.get(domain)

    def has_status(self, domain, level):
        return self.status.get(domain, FactionStatus()).level == level

    def update_level(self, domain, new_level):
        if domain in self.status:
            self.status[domain].level = new_level
        else:
            self.status[domain] = FactionStatus(new_level)

    def __repr__(self):
            return "\n".join([f"{domain}: {status}" for domain, status in self.status.items()])
    
class FactionStatus:
    def __init__(self, level=StatusLevel.LOW, title=""):
        self.level = level
        self.title = title

    def __repr__(self):
            return f"{self.title} ({self.level.name})"

class GangStatus(FactionStatus):
    def __init__(self, level=StatusLevel.LOW, title=""):
        super().__init__(level, title)

    def __repr__(self):
        return f"Gang Status: {self.title} ({self.level.name})"

class CorporationStatus(FactionStatus):
    def __init__(self, level=StatusLevel.LOW, title=""):
        super().__init__(level, title)

    def __repr__(self):
        return f"Corporation Status: {self.title} ({self.level.name})"

    def __str__(self):
            return self.name.capitalize()





""" status will be more fully developed. For example, different types of status, status within a faction, public status, status within a friend group etc
So that enum will need to be expanded eventually to at least a dictionary of Entity/Value pairs, perhaps using integers rather than strings, but with those integers mapped onto strings.
For example
A character has status
public : High, respected
faction x : Mid, ally
faction y : High, enemy """

""" character.status = {
"public": {"level": Status.HIGH, "title": "Respected"},
"faction_x": {"level": Status.MID, "title": "Ally"},
"faction_y": {"level": Status.HIGH, "title": "Enemy"}
} """