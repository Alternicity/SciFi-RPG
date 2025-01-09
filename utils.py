import logging
import os
import json
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
#from main.py
def ensure_file_exists(file_path, default_data=None):
    """
    Ensure the specified file exists. If it doesn't, create it with the provided default data.
    Args:
        file_path (str): The path of the file to check.
        default_data (dict or list): The default data to write if the file doesn't exist.
    """
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directories exist
        with open(file_path, 'w') as f:
            json.dump(default_data or [], f, indent=4)  # Write valid JSON default data
        print(f"Created new file at: {file_path}")

def load_characters_from_file(file_path):
    """
    Load character data from a JSON file.
    Args:
        file_path (str): The path to the character JSON file.
    Returns:
        list: A list of character data.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)  # Attempt to parse JSON
            if not isinstance(data, list):
                raise ValueError("Invalid data structure: Expected a list of characters.")
            logging.debug(f"Loaded character data: {data}")
            return data
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in {file_path}. Resetting to default.")
        ensure_file_exists(file_path, default_data=[])  # Reset file with default content
        return []  # Return an empty list
    except Exception as e:
        logging.error(f"Failed to load characters: {e}")
        #here call generate_and_save_characters()
        return []  # Return an empty list if an unexpected error occurs

def generate_and_save_characters(file_path, num_characters=5):
    """
    Generate characters and save them to the specified file.
    Args:
        file_path (str): The path to the character JSON file.
        num_characters (int): Number of characters to generate.
    """
    # Generate a list of Character objects
    try:
        characters = [
            Boss(name="Big Boss", faction="Blue Gang"),
            Captain(name="Blue Captain", faction="Blue Gang"),
            Employee(name="Corporate Employee", faction="Blue Corporation"),
            VIP(name="VIP", faction="Elite Corporation"),
            RiotCop(name="Cop One"),
        ]
    except Exception as e:
        logging.error(f"Error while generating characters: {e}")
    #logging.debug(f"Serializing character: {character.name}, {type(character).__name__}")

def load_characters_and_generate_if_empty(file_path):
    """
    Load characters from the JSON file. If empty, generate and save new characters.
    Args:
        file_path (str): Path to the character JSON file.
    Returns:
        list: List of characters.
    """
    characters = load_characters_from_file(file_path)
    if not characters:
        logging.info("No characters found. Generating new characters...")
        generate_and_save_characters(file_path)
        characters = load_characters_from_file(file_path)  # Reload after generation
    return characters
#The following functions are old and some of their functionality now resides in the generator files
def create_gang(data): #functional overlap with generateGangs.py, though might still be useful for single gang creation
    """Create a Gang object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Gang.")
    return Gang(name=data["name"], affiliation=data.get("affiliation", "unknown"))

def create_corporation(data): ##functional overlap with generateCorps.py, though might still be useful for single corporation creation
    """Create a Corporation object."""
    if "name" not in data:
        raise ValueError("Missing required attribute 'name' for Corporation.")
    return Corporation(name=data["name"])

def create_weapon(data): #Might still be useful, but need updating
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

def create_item(data): #Might still be useful, but need updating
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



    def list_existing_characters(character_registry):
        """Display a list of existing characters and their entity IDs."""
        if not character_registry:
            print("No existing characters.")
            return None
    
    for character in character_registry:
        print(f"Character ID: {character.entity_id}, Name: {character.name}")
    
    return character_registry