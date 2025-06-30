#salience.py
#this file must surely become more sophisticated as it is 
#all if, elif statements that wont scale well

#Centralize all salience into salience.py, with specific helpers for object types.


from weapons import Pistol
import time
from anchor_utils import Anchor
from events import Event


""" Optional Improvements (Later)
If compute_salience() fails often (e.g. for unexpected objects), consider:
Adding type guards or preprocessing origin_obj
Skipping percepts with "type": "unknown" or "origin": None
When motivations mature further, you may replace motivation objects entirely with
anchors passed down from higher-level decision-making or goal generation. """

def compute_salience(obj, observer, anchor: Anchor):
    from base_classes import Character, Location
    if isinstance(obj, Location):
        return compute_location_salience(obj, observer, anchor)
    elif isinstance(obj, Character):
        return compute_character_salience(obj, observer, anchor)
    elif isinstance(obj, Event):
        return compute_event_salience(obj, observer, anchor)
    else:
        return compute_object_salience(obj, observer, anchor)

#Ensure observer.enemies and faction.enemies use a consistent structure for reliable checking.

def compute_character_salience(character, observer, anchor: Anchor = None):
    if character is observer:
        return 0  # Ignore self

    salience = 1.0

    if getattr(character, "bloodstained", False):
        salience += 0.4

    if getattr(character, "is_visibly_wounded", False):
        salience += 0.3

    if anchor:
        if anchor.name == "violence":
            salience += 0.5
        if "enemy" in anchor.tags and hasattr(observer, "enemies") and character in observer.enemies:
            salience += 0.6
        if "friend" in anchor.tags and hasattr(observer, "friends") and character in observer.friends:
            salience += 0.3

    return salience



def compute_location_salience(location, observer, anchor: Anchor = None):
    salience = 1.0

    if anchor:
        if anchor.name in ["rob", "steal"]:
            if getattr(location, "robbable", False):
                salience += 1.3
            if getattr(location, "security", 0) > 1:
                salience -= 0.4

        if anchor.name in ["obtain_weapon", "obtain_ranged_weapon"] and getattr(location, "contains_weapons", False):
            salience += 1.0

    return salience


def compute_object_salience(obj, observer, anchor: Anchor = None):
    salience = 1.0

    if anchor:
        if anchor.name == "obtain_ranged_weapon":
            if getattr(obj, "is_weapon", False):
                salience += 1.0
                if getattr(obj, "is_ranged", False):
                    salience += 1.0

        if anchor.name == "steal" and getattr(obj, "is_valuable", False):
            salience += 1.5

    return salience


def compute_event_salience(event, observer, anchor: Anchor = None):
    salience = 1.0

    if anchor:
        if anchor.name in getattr(event, "tags", []):
            salience += 1.0

        if "violence" in getattr(event, "tags", []) and anchor.name == "violence":
            salience += 0.6

        if hasattr(event, "involves"):
            if event.involves(getattr(observer, "partner", None)):
                salience += 0.7
            if event.involves(getattr(observer, "enemy", None)):
                salience += 0.8

        if "loot" in getattr(event, "tags", []) and anchor.name == "steal":
            salience += 0.6

    return salience


def compute_salience_for_motivation(self, percept, motivation):
        # Use centralized logic
        context = {"observer": self.npc}
        score = compute_salience(percept, motivation.type, context)

        print(f"[SALIENCE] {self.npc.name} sees {percept.get('description', str(percept))} for {motivation.type}: {score:.2f}")
        return score

def compute_salience_for_percept_with_anchor(percept, anchor, observer=None):
    score = 1.0
    if "tags" in percept and anchor.name in percept["tags"]:
        score += 1.3
    if "location" in percept and observer and percept["location"] == getattr(observer.location, "name", None):
        score += 1.4
    return score * anchor.weight


    
#For the future, replace urgent_motivation as anchor with object of this

