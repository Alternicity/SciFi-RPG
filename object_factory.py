import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Registry of type mappings
OBJECT_TYPE_REGISTRY = {
    "weapon": Weapon,
    "item": ObjectInWorld,
    "gadget": ObjectInWorld,
    "container": ObjectInWorld,
    # Add other object types here
}

def create_weapon(data):
    """Create a Weapon object."""
    if "name" not in data or "damage" not in data:
        raise ValueError("Missing required attributes for Weapon.")
    return Weapon(
        name=data["name"],
        damage=data["damage"],
        ammo=data.get("ammo", 0),
        toughness=data["toughness"],
        damage_points=data.get("damage_points", 0),
        legality=data.get("legality", True),
        value=data["value"],
        blackmarket_value=data.get("blackmarket_value", 0),
        size=data["size"],
        range_limit=data.get("range_limit", 50),
    )

def create_item(data):
    """Create an ObjectInWorld object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Item.")
    return ObjectInWorld(
        name=data["name"],
        toughness=data["toughness"],
        damage_points=data.get("damage_points", 0),
        legality=data.get("legality", True),
        value=data["value"],
        blackmarket_value=data.get("blackmarket_value", 0),
        size=data["size"],
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
    obj_type = data.get("obj_type")
    if obj_type is None:
        raise ValueError("Missing 'obj_type' in data.")

    logger.info(f"Creating object of type {obj_type} with data: {data}.")

    if obj_type in OBJECT_TYPE_REGISTRY:
        return OBJECT_TYPE_REGISTRY[obj_type](**data)
    else:
        raise ValueError(f"Unknown obj_type: {obj_type}")