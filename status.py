from enum import Enum

class Status(Enum):
    LOW = "low"
    MID = "mid"
    HIGH = "high"
    ELITE = "elite"

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