# base/core_types.py
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
        self.tags = tags or []