#salience.py
#this file must surely become more sophisticated as it is 
#all if, elif statements that wont scale well

#Centralize all salience into salience.py, with specific helpers for object types.
from typing import Optional

from weapons import Pistol

def compute_salience(obj, anchor: str, context=None) -> float:
    """
    Stateless global router. Should NOT access self.npc directly.
    If needed, NPC should be passed via context["npc"] or context["observer"].
    """
    from location import Location
    from characters import Character
    from events import Event

    observer = context.get("observer") if context else None

    if isinstance(obj, Location):
        return compute_location_salience(obj, observer, anchor)
    elif isinstance(obj, Character):
        return compute_character_salience(obj, observer, anchor)
    elif isinstance(obj, Event):
        return compute_event_salience(obj, observer, anchor)
    else:
        return compute_object_salience(obj, observer, anchor)

#Ensure observer.enemies and faction.enemies use a consistent structure for reliable checking.

def compute_character_salience(character, observer, anchor=None):
    """
    Computes how attention-grabbing another character is to the observer.
    """
    salience = 1.0

    if character is observer:
        return 0  # Don't self-evaluate

    if getattr(character, "bloodstained", False):
        salience += 0.4

    if getattr(character, "is_visibly_wounded", False):
        salience += 0.3

    # Motivation-aware evaluation
    if anchor == "violence":
        salience += 0.5

    # If observer has history or relationship with character
    if hasattr(observer, "enemies") and character in observer.enemies:
        salience += 0.6
    if hasattr(observer, "friends") and character in observer.friends:
        salience += 0.3

    return salience


def compute_location_salience(location, observer, anchor):
    salience = 1.0

    if anchor == "rob":
        if getattr(location, "robbable", False):
            salience += 1.3
        if location.security and location.security.level > 1:
            salience -= 0.4

    if getattr(location, "contains_weapons", False):
        salience += 1.0

    return salience

def compute_object_salience(obj, observer, anchor):
    salience = 1.0

    if anchor == "obtain_ranged_weapon" and getattr(obj, "is_weapon", False):
        if getattr(obj, "is_ranged", False):
            salience += 2.0
        else:
            salience += 1.0

    if anchor == "steal" and getattr(obj, "is_valuable", False):
        salience += 1.5

    return salience

def compute_event_salience(event, observer, anchor=None):
    """
    Computes how attention-worthy an event is to the observer.
    """
    salience = 1.0

    # Match anchor to event tags
    if anchor in getattr(event, "tags", []):
        salience += 1.0

    if "violence" in getattr(event, "tags", []) and anchor == "violence":
        salience += 0.6

    if hasattr(event, "involves"):
        if event.involves(getattr(observer, "partner", None)):
            salience += 0.7
        if event.involves(getattr(observer, "enemy", None)):
            salience += 0.8

    if "loot" in getattr(event, "tags", []) and anchor == "steal":
        salience += 0.6

    return salience

