#salience.py
#Centralize all salience into salience.py, with specific helpers for object types.
import time
from anchor_utils import Anchor
from events import Event
from anchor_utils import create_anchor_from_motivation

""" Optional Improvements (Later)
If compute_salience() fails often (e.g. for unexpected objects), consider:
Adding type guards or preprocessing origin_obj
Skipping percepts with "type": "unknown" or "origin": None
When motivations mature further, you may replace motivation objects entirely with
anchors passed down from higher-level decision-making or goal generation. """

def compute_salience(obj, observer, anchor=None):
    from base_classes import Character, Location

    # Optional: warn if anchor is None in test mode
    if anchor is None and getattr(observer, "is_test_observer", False):
        label = getattr(obj, "name", str(obj))
        print(f"[SALIENCE COMPUTE] No anchor provided. Defaulting salience to 1 for: {label}")
        if isinstance(obj, dict):
            print(f"[WARNING] compute_salience() received a dict instead of an object.")
            import traceback
            traceback.print_stack(limit=3)

    # Dispatch to specific salience calculator
    if isinstance(obj, Character):
        return compute_character_salience(obj, observer, anchor)
    elif isinstance(obj, Location):
        return compute_location_salience(obj, observer, anchor)
    elif isinstance(obj, Event):
        return compute_event_salience(obj, observer, anchor)
    else:
        return compute_object_salience(obj, observer, anchor)

def generic_tag_salience_boost(obj, anchor):
    score = 0.0
    if hasattr(obj, "tags") and anchor:
        obj_tags = set(obj.tags or [])
        anchor_tags = set(anchor.tags or [])
        matches = obj_tags & anchor_tags
        if matches:
            score += 1.2 + 0.1 * len(matches)
    return score

def compute_character_salience(obj, observer, anchor: Anchor = None):
    character = obj  # Optional alias for clarity
    if character is observer:#character marked as not defined
        return 0  # Ignore self

    salience = 1.0
    salience += generic_tag_salience_boost(obj, anchor)
    if getattr(character, "bloodstained", False):#character marked as not defined
        salience += 0.4

    if getattr(character, "is_visibly_wounded", False):#character marked as not defined
        salience += 0.3

    if anchor:
        if anchor.name == "violence":
            salience += 0.5
        if "enemy" in anchor.tags and hasattr(observer, "enemies") and character in observer.enemies:
            salience += 0.6
        if "friend" in anchor.tags and hasattr(observer, "friends") and character in observer.friends:
            salience += 0.3

    return salience

def compute_location_salience(obj, observer, anchor: Anchor = None):
    location = obj  # Optional alias for clarity
    salience = 1.0
    salience += generic_tag_salience_boost(obj, anchor)#obj marked as not defined
    if anchor:
        if anchor.name in ["rob", "steal"]:
            if getattr(location, "robbable", False):
                salience += 1.3
            if hasattr(location, "security") and getattr(location.security, "level", 0) > 1:

                salience -= 0.4

        if anchor.name in ["obtain_weapon", "obtain_ranged_weapon"] and getattr(location, "contains_weapons", False):
            salience += 1.0

    return salience


def compute_object_salience(obj, observer, anchor: Anchor = None):
    salience = 1.0
    salience += generic_tag_salience_boost(obj, anchor)
    if anchor:
        if anchor.name == "obtain_ranged_weapon":
            if getattr(obj, "is_weapon", False):
                salience += 1.0
                if getattr(obj, "is_ranged", False):
                    salience += 1.0

        if anchor.name == "steal" and getattr(obj, "is_valuable", False):
            salience += 1.5

    return salience

def compute_event_salience(obj, observer, anchor: Anchor = None):
    event = obj  # Optional alias for clarity
    salience = 1.0
    salience += generic_tag_salience_boost(obj, anchor)
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
    anchor = create_anchor_from_motivation(motivation)
    # I skipped adding generic_tag_salience_boost() here as I wonder if some circular
    #effect might result from that.
    score = compute_salience(percept, self.observer, anchor)
    print(f"[SALIENCE] {self.observer.name} sees {percept.get('description', str(percept))} for {motivation.type}: {score:.2f}")
    return score

def compute_salience_for_percept_with_anchor(obj, anchor, observer=None):
    percept = obj  # Optional alias for clarity
    score = 1.0
    salience += generic_tag_salience_boost(obj, anchor)
    if "tags" in percept and anchor.name in percept["tags"]:
        score += 1.3
    if "location" in percept and observer and percept["location"] == getattr(observer.location, "name", None):
        score += 1.4
    return round(1.0 + (score - 1.0) * anchor.weight, 2)


    
#For the future, replace urgent_motivation as anchor with object of this

