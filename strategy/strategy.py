#strategy.py

class StrategicInfo:
    def __init__(self, type, severity=0, tags=[]):
        self.type = type
        self.severity = severity
        self.tags = tags

class TurfWarInfo(StrategicInfo):
    def __init__(self, region, factions_involved):
        super().__init__("TurfWar", severity=5, tags=["gang", "turf"])
        self.region = region
        self.factions_involved = factions_involved
