import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_gang(data):
    """Create a Gang object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Gang.")
    return Gang(name=data["name"], affiliation=data.get("affiliation", "unknown"))

def create_corporation(data):
    """Create a Corporation object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Corporation.")
    return Corporation(name=data["name"])

def create_weapon(data):
    """Create a Weapon object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Weapon.")
    return Weapon(
        name=data["name"],
        damage=data.get("damage", 0),
        ammo=data.get("ammo", 0),
        range_limit=data.get("range_limit", 0),
        toughness=data.get("toughness", "normal"),
        size=data.get("size", "pocket_sized"),
    )

def create_item(data):
    """Create an ObjectInWorld object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Item.")
    return ObjectInWorld(
        name=data["name"],
        toughness=data.get("toughness", "normal"),
        damage_points=data.get("damage_points", 0),
        legality=data.get("legality", True),
        legitimate_value=data.get("value", 0),
        blackmarket_value=data.get("blackmarket_value", 0),
        size=data.get("size", "pocket_sized"),
    )

def create_object(data):
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