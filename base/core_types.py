# base.core_types.py
#NO IMPORTS
#tiny, pure, Platonic objects
class FactionBase:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags or []

class LocationBase:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags or []

class CharacterBase:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags or []

class RegionBase:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags or []#tags in fine here

class KnowledgeBase:
    def __init__(self, **kwargs):
        # Apply all explicit fields
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Always ensure a tags attribute exists
        self.tags = kwargs.get("tags", [])