import os
import json
from characters import Character, Boss, Captain, Manager, Employee, Civilian, VIP, CorporateSecurity, RiotCop, GangMember
from common import Status

# Directory to save character data
OUTPUT_DIR = r"C:\Users\Stuart\Python Scripts\scifi RPG\data\Test City\Characters"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_character_data(character):
    """Convert character object to a dictionary for JSON serialization."""
    return {
        "name": character.name,
        "role": character.char_role,
        "faction": character.faction,
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

def save_character(character, output_dir=OUTPUT_DIR):
    """Save a character to a JSON file."""
    filepath = os.path.join(output_dir, f"{character.name}.json")
    with open(filepath, 'w') as f:
        json.dump(generate_character_data(character), f, indent=4)
    print(f"Character saved: {filepath}")

def main():
    # Example: Create some characters and save them
    characters = [
        Boss(name="Big Boss", faction="Blue Gang"),
        Captain(name="Blue Captain", faction="Blue Gang"),
        Employee(name="Corporate Employee", faction="Blue Corporation"),
        VIP(name="VIP", faction="Elite Corporation"),
        RiotCop(name="Cop One"),
    ]

    for char in characters:
        save_character(char)

if __name__ == "__main__":
    main()
