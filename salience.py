#salience.py

def compute_salience(obj, observer):
    """
    Routes to the appropriate salience function based on the type of object.
    """
    from location import Location
    from characters import Character
    from events import Event  # if you have such a class

    if isinstance(obj, Location):
        return compute_location_salience(obj, observer)
    elif isinstance(obj, Character):
        return obj.compute_salience(observer)
    elif isinstance(obj, Event):  # Optional: Event class
        return compute_event_salience(obj, observer)
    else:
        return compute_object_salience(obj, observer)


def compute_character_salience(character, observer):
    salience = 1
    if character.bloodstained:
        salience += 5
    if character.is_visibly_wounded:
        salience += 10
    if observer and "violence" in getattr(observer, "motivations", []): #use tags?
        salience += 2
    # more conditions...
    return salience


def compute_location_salience(location, observer):
    salience = 1

    if hasattr(location, "faction") and location.faction in observer.enemies:
        salience += 5

    if location.security and location.security.level > 1:
        salience += 3

    if getattr(location, "contains_weapons", False):
        salience += 4

    return salience

def compute_object_salience(obj, observer):
    salience = 1

    if getattr(obj, "is_weapon", False):
        salience += 5

    if getattr(obj, "is_valuable", False):
        salience += 4

    if getattr(obj, "faction", None) in observer.enemies:
        salience += 3

    return salience

def compute_event_salience(event, observer):
    salience = 1

    if "violence" in event.tags and "violence" in observer.motivations:
        salience += 4

    if event.involves(observer.partner) or event.involves(observer.enemy):
        salience += 5

    if "loot" in event.tags:
        salience += 2

    return salience

