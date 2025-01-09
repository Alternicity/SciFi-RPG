import logging
import json
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG, WARNING, ERROR as needed
    format="%(levelname)s:%(message)s"
)

def create_characters_as_objects():
    logging.info("About to create characters, create_characters_as_objects, create.py")
    characters = [
        RiotCop(name="John", faction="The State"),
        CorporateAssasin(name="Jane", faction="BlueCorp"),
    ]
    logging.info(f"Created characters: {characters}")
    return characters

def create_and_serialize_characters():
    characters = [
        RiotCop(name="John", faction="The State"),
        CorporateAssasin(name="Jane", faction="BlueCorp"),
    ]
    with open("characters.json", "w") as f:
        json.dump([char.__dict__ for char in characters], f, indent=4)
    logging.info("Characters serialized to characters.json")

def create_object(data):#Might still be useful, but need updating
    """
    Factory function to create an object dynamically based on its type.

    Args:
        data (dict): Data representing the object.

    Returns:
        An instance of the appropriate class.

    Raises:
        ValueError: If the object type is unsupported or required attributes are missing.
    """
    obj_type = data.get("type")
    if obj_type is None:
        raise ValueError("Missing 'type' in data.")

    logger.info(f"Creating object of type {obj_type} with data: {data}.")

    if obj_type == "gang":
        return create_gang(data)
    elif obj_type == "corporation":
        return create_corporation(data)
    elif obj_type == "weapon":
        return create_weapon(data)
    elif obj_type == "item":
        return create_item(data)
    else:
        raise ValueError(f"Unsupported type: {obj_type}")