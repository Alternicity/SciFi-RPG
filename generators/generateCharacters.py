import sys
import os
import json
import random
import string

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from common import Status
from characters import Character, Boss, Captain, Manager, Employee, Civilian, VIP, CorporateSecurity, RiotCop, GangMember
#By appending ROOT_DIR to sys.path before the imports,
#Python knows to look in the root directory for the common.py and characters.py files.

# Directory to save character data
OUTPUT_DIR = r"C:\Users\Stuart\Python Scripts\scifi RPG\data\Test City\Characters"
DEFAULT_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "characters.json")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_entity_id():
    """Generate a random entity ID (a string of 8 characters)."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))

def generate_character_data(character):
    # Generate an entity ID if not already present
    if not character.entity_id:
        character.entity_id = generate_entity_id()

    logging.debug(f"Serializing character: {character.name}, {type(character).__name__}")
    # Ensure all attributes are serialized properly

    """Convert character object to a dictionary for JSON serialization."""
    return {
        "name": character.name,
        "role": character.char_role,
        "faction": character.faction,
        "entity_id": character.entity_id,
        "strength": character.strength,
        "agility": character.agility,
        "intelligence": character.intelligence,
        "luck": character.luck,
        "psy": character.psy,
        "toughness": character.toughness,
        "morale": character.morale,
        "health": character.health,
        "race": character.race,
        "sex": character.sex,
        "loyalty": character.loyalty,
        "inventory": [str(item) for item in character.inventory],  # Convert inventory items to strings
        "wallet": {
            "cash": character.wallet.cash,
            "bank_card_cash": character.wallet.bank_card_cash,
        },
    }

def save_characters(characters, output_file=DEFAULT_OUTPUT_FILE):
    """
    Save a list of characters to a JSON file.
    Args:
        characters (list): List of Character instances.
        output_file (str): Path to the output JSON file.
    """
    serialized_characters = [generate_character_data(char) for char in characters]
    with open(output_file, 'w') as f:
        json.dump(serialized_characters, f, indent=4)
    print(f"Characters saved to: {output_file}")

def main():
    # Example: Create some characters and save them
    characters = [
        Boss(name="Big Boss", faction="Blue Gang"),
        Captain(name="Blue Captain", faction="Blue Gang"),
        Employee(name="Corporate Employee", faction="Blue Corporation"),
        VIP(name="VIP", faction="Elite Corporation"),
        RiotCop(name="Cop One"),
    ]

    # Save the characters to the JSON file
    save_characters(characters)

if __name__ == "__main__":
    main()
