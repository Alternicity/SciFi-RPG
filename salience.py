#salience.py
#Centralize all salience into salience.py, with specific helpers for object types.
import time
from events import Event
from anchor_utils import Anchor, create_anchor_from_motivation
from debug_utils import debug_print

""" Optional Improvements (Later)
If compute_salience() fails often (e.g. for unexpected objects), consider:
Adding type guards or preprocessing origin_obj
Skipping percepts with "type": "unknown" or "origin": None
When motivations mature further, you may replace motivation objects entirely with
anchors passed down from higher-level decision-making or goal generation. """

def compute_generic_salience(obj, observer, anchor=None):
    """
    Legacy fallback for objects or thoughts without custom salience logic.
    Uses tags, urgency, and anchor relevance if available.
    """
    base = getattr(obj, "urgency", 1)
    tags = getattr(obj, "tags", [])
    anchor_tags = getattr(anchor, "tags", []) if anchor else []

    # Simple tag overlap weighting
    overlap = len(set(tags) & set(anchor_tags)) if anchor_tags else 0
    score = base + overlap * 2

    if observer.is_test_npc:
        debug_print(observer, f"Using generic fallback for {type(obj).__name__}: {score:.2f}", category="salience")

    # Cap score range
    return min(score, 10)


def compute_salience(obj, observer, anchor=None):
    import inspect
    stack = inspect.stack()
    caller_info = f"{stack[1].function} @ {stack[1].filename}:{stack[1].lineno}"

    try:
        if anchor:
            return anchor.compute_salience_for(obj, observer)
        return getattr(obj, "salience", 0.5)

    except Exception as e:
        if getattr(observer, "is_test_npc", False):
            print(f"[ERROR] {type(anchor).__name__} failed: {e} | from {caller_info} | obj={type(obj).__name__}")
        return 0.0

    finally:
        return
    #trace for above. Replace the return with this
        """ if getattr(observer, "is_test_npc", False) or getattr(observer, "is_test_observer", False):
            label = getattr(obj, "name", str(obj))
            obj_type = type(obj).__name__
            anchor_name = type(anchor).__name__ if anchor else "None"
            npc=observer
            debug_print(
                npc,
                f"[SALIENCE TRACE] obj={obj_type}('{label}'), anchor={anchor_name}, from {caller_info}",
                category="salience"
            ) """

def normalize_salience(value):
    return value if isinstance(value, (int, float)) else 0.0

def generic_tag_salience_boost(obj, anchor):
    score = 0.0
    if hasattr(obj, "tags") and anchor:
        obj_tags = set(obj.tags or [])
        anchor_tags = set(anchor.tags or [])
        matches = obj_tags & anchor_tags
        if matches:
            score += 1.2 + 0.1 * len(matches)
    return score

def compute_character_salience(obj, observer, anchor=None):
    # ignore self
    if obj is observer:
        return 0.0

    salience = 1.0

    # tag-based adjustments
    salience += generic_tag_salience_boost(obj, anchor)

    if getattr(obj, "bloodstained", False):
        salience += 0.4
    if getattr(obj, "is_visibly_wounded", False):
        salience += 0.3

    # anchor-aware adjustments
    if anchor:
        if "enemy" in getattr(anchor, "tags", []) and hasattr(observer, "enemies") and obj in observer.enemies:
            salience += 0.6
        if "friend" in getattr(anchor, "tags", []) and hasattr(observer, "friends") and obj in observer.friends:
            salience += 0.3

    # simple, safe trace
    if getattr(observer, "is_test_npc", False):
        print(
            f"[TRACE] compute_character_salience obj={obj} anchor={type(anchor).__name__ if anchor else 'None'}"
        )

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
    anchor = create_anchor_from_motivation(motivation)#This module is just helper, fallback functions
    #salience is preferably calculated inside anchors
    #this function might even be a candidate for deletion
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

