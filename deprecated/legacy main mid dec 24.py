# Legacy main.py

import random
import string
from characters import Character
from loyalty import Loyalty
from loader import load_data


def generate_entity_id():
    """Generate a random entity ID (a string of 8 characters)."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


def create_character_if_needed(entity_id, character_registry):
    """Create a new character if the entity ID doesn't exist yet."""
    if entity_id not in character_registry:
        print(f"Creating a new character with ID {entity_id}...")

        print("\nPlease select a role for your new character:")
        roles = [
            "Grunt",
            "Captain",
            "Boss",
            "Manager",
            "Employee",
            "CEO",
        ]  # Define available roles
        for idx, role in enumerate(roles, start=1):
            print(f"{idx}. {role}")

        while True:
            try:
                choice = int(input(f"Enter a number (1-{len(roles)}): "))
                if 1 <= choice <= len(roles):
                    chosen_role = roles[choice - 1]
                    break
                else:
                    print("Invalid choice. Please choose a valid role.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        character = Character(
            name=f"Character {entity_id}", entity_id=entity_id, char_role=chosen_role
        )
        character_registry[entity_id] = character
        print(f"Character created with role: {chosen_role}")
        return character
    else:
        print(f"Entity ID {entity_id} already exists.")
        return character_registry[entity_id]


def list_existing_characters(character_registry):
    """Display a list of existing characters and their entity IDs."""
    if not character_registry:
        print("No existing characters.")
        return None

    print("\nExisting characters:")
    for entity_id, character in character_registry.items():
        print(f"ID: {entity_id}, Name: {character.name}")

    return character_registry


def test_loyalty_system(character_registry):
    """Test the loyalty system with entity ID creation and loyalty manipulation."""
    # List existing characters and allow the user to choose one
    character_registry = list_existing_characters(character_registry) or {}

    if not character_registry:
        print("\nNo existing characters found. You will need to create a new one.")
        entity_id = input(
            "Enter a new entity ID (or press Enter to generate a random one): "
        )
        if not entity_id:
            entity_id = generate_entity_id()
        character = create_character_if_needed(entity_id, character_registry)
    else:
        entity_id = input(
            "\nEnter the entity ID you want to interact with, or press Enter to create a new one: "
        )

        if not entity_id:
            entity_id = generate_entity_id()
            print(f"Generated entity ID: {entity_id}")
            character = create_character_if_needed(entity_id, character_registry)
        else:
            if entity_id in character_registry:
                character = character_registry[entity_id]
            else:
                print(f"Entity ID {entity_id} not found. Creating a new character...")
                character = create_character_if_needed(entity_id, character_registry)

    loyalty = Loyalty(entity_id)

    loyalty.add_loyalty("FactionA", 80)
    loyalty.add_loyalty("FactionB", 60)
    print(f"Current loyalties for {entity_id}: {loyalty.display_loyalties()}")

    loyalty.save_loyalty()
    print(f"Loyalty data for {entity_id} saved.")

    loyalty.load_loyalty()
    print(f"Loyalty data for {entity_id} loaded: {loyalty.display_loyalties()}")


def display_factions_data():
    """Load and display factions data."""
    try:
        factions_data = load_data("data/loyalties/factions/factions.json")
        print("\n--- Factions Data ---")

        if not factions_data:
            print("No factions data found.")
        else:
            for faction in factions_data:
                if isinstance(faction, dict):  # Check if the faction is a dictionary
                    print(f"\nFaction Name: {faction.get('name', 'N/A')}")
                    print(f"Faction Type: {faction.get('type', 'N/A')}")
                    print(f"Members: {', '.join(faction.get('members', []))}")
                else:
                    print("Invalid data format in factions list.")

        print("\n---------------------")
    except FileNotFoundError as e:
        print(f"Error loading factions data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def display_state_data():
    """Display the state data in a formatted manner."""
    state_data = load_data("data/loyalties/factions/state.json")

    print("--- State Data ---\n")

    # Extract state information
    state_info = state_data.get("state_name", "N/A")
    capital = state_data.get("capital", "N/A")
    population = state_data.get("population", "N/A")
    economy = state_data.get("economy", {})
    factions = state_data.get("factions", [])

    # Print state info in a clean format
    print(f"State Name: {state_info}")
    print(f"Capital: {capital}")
    print(f"Population: {population}")

    # Print economy information
    print("\nEconomy:")
    if economy:
        industries = economy.get("industries", [])
        gdp = economy.get("gdp", "N/A")
        print(f"  Industries: {', '.join(industries) if industries else 'N/A'}")
        print(f"  GDP: {gdp}")
    else:
        print("  Economy data not available.")

    # Print factions data
    print("\nFactions:")
    if factions:
        for faction in factions:
            name = faction.get("name", "N/A")
            f_type = faction.get("type", "N/A")
            leader = faction.get("leader", "N/A")
            territory = faction.get("territory", "N/A")
            main_product = faction.get("main_product", "N/A")

            print(f"  - {name} (Type: {f_type}):")
            print(f"    Leader: {leader}")
            if f_type == "gang":
                print(f"    Territory: {territory}")
            if f_type == "corporation":
                print(f"    Main Product: {main_product}")
    else:
        print("  No factions found.")


def main():
    print("Welcome to the Test Menu")
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
            test_loyalty_system(character_registry)  # Test loyalty system

        elif choice == "4":
            print("Exiting the test menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
