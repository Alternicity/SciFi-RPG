import os
import json
import display


class Loyalty:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.loyalties = {}

    def add_loyalty(self, faction_name, value):
        self.loyalties[faction_name] = value

    def display_loyalties(self):
        return self.loyalties

    def save_loyalty(self):
        # Specify the directory to save loyalty data
        base_path = f"data/loyalties/{self.entity_id}"

        # Ensure the directory exists
        os.makedirs(base_path, exist_ok=True)

        # Define the file path for saving the loyalty data
        file_path = os.path.join(base_path, "loyalty_data.json")

        # Save the loyalty data as a JSON file
        with open(file_path, "w") as file:
            json.dump(self.loyalties, file)
        print(f"Loyalty data saved to {file_path}")

    def load_loyalty(self):
        # Specify the directory where loyalty data is saved
        base_path = f"data/loyalties/{self.entity_id}"

        # Define the file path for loading the loyalty data
        file_path = os.path.join(base_path, "loyalty_data.json")

        # Load the loyalty data if the file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.loyalties = json.load(file)
            print(f"Loyalty data loaded from {file_path}")
        else:
            print(f"No loyalty data found for {self.entity_id}")


class LoyaltySystem:
    def __init__(self, region_name):
        self.region_name = region_name
        self.characters = {}

    def add_character(self, character):
        if isinstance(
            character, Character
        ):  # Optional check to ensure it's a Character
            self.characters[character.entity_id] = character
        else:
            print(f"Error: Invalid character passed - {character}")

    def get_loyalty(self, character_id):
        if character_id in self.characters:
            return self.characters[character_id].loyalties
        else:
            print(f"Character with ID {character_id} not found.")
            return None


def test_loyalty_system(character_registry):
    """Test the loyalty system with entity ID creation and loyalty manipulation."""
    loyalty_system = LoyaltySystem("Sample Region")

    # Create or fetch character
    character_registry = list_existing_characters(character_registry) or {}

    if not character_registry:
        print("\nNo existing characters found. You will need to create a new one.")
        entity_id = input(
            "Enter a new entity ID (or press Enter to generate a random one): "
        )
        if not entity_id:
            entity_id = generate_entity_id()
        character = create_character_if_needed(entity_id, character_registry)
        loyalty_system.add_character(character)
    else:
        entity_id = input(
            "\nEnter the entity ID you want to interact with, or press Enter to create a new one: "
        )

        if not entity_id:
            entity_id = generate_entity_id()
            print(f"Generated entity ID: {entity_id}")
            character = create_character_if_needed(entity_id, character_registry)
            loyalty_system.add_character(character)
        else:
            if entity_id in character_registry:
                character = character_registry[entity_id]
                loyalty_system.add_character(character)
            else:
                print(f"Entity ID {entity_id} not found. Creating a new character...")
                character = create_character_if_needed(entity_id, character_registry)
                loyalty_system.add_character(character)

    loyalty = Loyalty(entity_id)

    loyalty.add_loyalty("FactionA", 80)
    loyalty.add_loyalty("FactionB", 60)
    print(f"Current loyalties for {entity_id}: {loyalty.display_loyalties()}")

    loyalty.save_loyalty()
    print(f"Loyalty data for {entity_id} saved.")

    loyalty.load_loyalty()
    print(f"Loyalty data for {entity_id} loaded: {loyalty.display_loyalties()}")
