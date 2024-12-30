import random
import yaml
import json
import sys
import os
import string

# Add the 'generators' folder to the system path
script_dir = os.path.dirname(__file__)  # Get the directory of the current script
generators_dir = os.path.join(script_dir, "generators")
sys.path.append(generators_dir)

# Import the necessary modules after adding paths
from loyalty import Loyalty, LoyaltySystem, test_loyalty_system
from loader import load_data
from characters import Character
from characters import list_existing_characters
from region_menu import generate_region_menu


def main_menu():
    """Display the main menu and handle user choices."""
    character_registry = {}  # or load from file/database

    while True:
        print("\nMain Menu:")
        print("1. Generate Region")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            generate_region_menu()
        #elif choice == "2":
            #test_loyalty_system(character_registry)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


def generate_entity_id():
    """Generate a random entity ID (a string of 8 characters)."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


def select_role(roles):
    print("\nPlease select a role for your new character:")
    for idx, role in enumerate(roles, start=1):
        print(f"{idx}. {role}")

    while True:
        try:
            choice = int(input(f"Enter a number (1-{len(roles)}): "))
            if 1 <= choice <= len(roles):
                return roles[choice - 1]
            else:
                print("Invalid choice. Please choose a valid role.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def create_character_if_needed(entity_id, character_registry):
    """Create or fetch a character based on entity ID."""
    if entity_id is None:
        entity_id = generate_entity_id()

    if entity_id not in character_registry:
        print(f"Creating a new character with ID {entity_id}...")
        chosen_role = select_role(
            ["Grunt", "Captain", "Boss", "Manager", "Employee", "CEO"]
        )
        character = Character(
            name=f"Character {entity_id}", entity_id=entity_id, char_role=chosen_role
        )
        character_registry[entity_id] = character
        print(f"Character created with role: {chosen_role}")
    else:
        print(f"Entity ID {entity_id} already exists.")
        character = character_registry[entity_id]
    return character


    print("\nExisting characters:")
    for entity_id, character in character_registry.items():
        print(f"ID: {entity_id}, Name: {character.name}")

    return character_registry


def main():
    print("Welcome to the Test Menu")
    character_registry = {}
    while True:
        print("\nChoose an option:")
        print("1. Display all factions data")
        print("2. Display state data")
        print("3. Test loyalty system (create, update, save, load)")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_factions_data()  # Call the function to display factions data

        elif choice == "2":
            display_state_data()  # Call the function to display state data
        elif choice == "3":
            # Call the function to create or fetch a character
            entity_id = input("Enter entity ID (or leave blank to generate one): ")
            entity_id = entity_id if entity_id else None
            create_character_if_needed(entity_id, character_registry)
            test_loyalty_system(character_registry)

        elif choice == "4":
            print("Exiting the test menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def test_loyalty_system(character_registry):
    """Test function to display existing characters."""
    print(f"Character Registry: {character_registry}")  # Debugging line
    character_registry = list_existing_characters(character_registry) or {}

if __name__ == "__main__":
    main_menu()
