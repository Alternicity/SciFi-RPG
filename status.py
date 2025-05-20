from enum import IntEnum
from visual_effects import color_codes, color_text, RED
class StatusLevel(IntEnum):
    NONE = 0
    LOW = 1
    MID = 2
    HIGH = 3
    ELITE = 4

    
class CharacterStatus:
    def __init__(self):
        # Keys can be "public", "gang", "corp_name", etc.
        self.status_by_domain = {}

    def set_status(self, domain, status_obj):
        self.status_by_domain[domain] = status_obj

    def get_status(self, domain):
        return self.status_by_domain.get(domain)

    def has_status(self, domain, level):
        return self.status_by_domain.get(domain, FactionStatus()).level == level

    def update_level(self, domain, new_level):
        if domain in self.status_by_domain:
            self.status_by_domain[domain].level = new_level
        else:
            self.status_by_domain[domain] = FactionStatus(new_level)

    def __repr__(self):
            return "\n".join([f"{domain}: {status}" for domain, status in self.status_by_domain.items()])
    
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


def get_primary_status_display(character):
    status_obj = character.status.get_status(character.primary_status_domain)
    if status_obj:
        base = f"{status_obj.title} ({status_obj.level.name})"
        return color_text(base, RED) if status_obj.level == StatusLevel.HIGH else base
    return "Unknown"