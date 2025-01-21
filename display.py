from tabulate import tabulate
import logging
from character_creation import create_characters_as_objects
import loader
import os
from city_utils import regenerate_city_data
from characters import Manager, Civilian, Character
from location import Region
import json

from common import get_project_root, get_file_path
#ALL files use this to get the project root

# Setup logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#This file should prbably contain the mapping dictionary for user facing region names

def display_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n=== Main Menu ===")
        print("1: Create Characters (Game Objects)")
        print("2: Create Characters (Serialized Data)")
        print("3: Load Serialized Characters")
        print("4: Play/Test Game")
        print("5: Regenerate City Data")  # Add option to regenerate city
        print("6: Exit")
        
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                characters = create_characters_as_objects()
                print("\n=== Character Information ===")
                print(list_characters(characters))
            elif choice == 2:
                print("Feature to create and serialize characters is under development.")
            elif choice == 3:
                print("Feature to load serialized characters is under development.")
            elif choice == 4:
                # Start game logic, calling `start_game_menu` from gameplay.py
                selected_character, region = start_game_menu()# variables are the expected return values
                if selected_character and region:
                    return selected_character, region  # Return for gameplay flow
            elif choice == 5:
                regenerate_city_data()  # Call regeneration
            elif choice == 6:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def start_game_menu():
    """Start the game and handle character and region selection."""
    print("Starting game...")

    # Predefined characters to select from
    character_data = [
        {"type": "Manager", "name": "Carolina", "faction": "BlueCorp", "bankCardCash": 500, "fun": 1, "hunger": 3},
        {"type": "Civilian", "name": "Charlie", "faction": "None", "occupation": "Shopkeeper"},
    ]
    characters = [
        Manager(name="Carolina", faction="BlueCorp", bankCardCash=500, fun=1, hunger=3),
        Civilian(name="Charlie", faction="None", occupation="Shopkeeper"),
    ]

    # Step 1: Select character
    selected_character = select_character_menu(characters)
    if not selected_character:
        print("Character selection failed.")
        return None, None

    # Step 2: Select region
    region = select_region_menu()
    if not region:
        print("Region selection failed. Exiting to main menu...")
        return None, None  # Return None if region selection failed
    
    print(f"Selected region: {region.nameForUser}")  # Use the 'nameForUser' attribute

    # Step 3: Use the selected character
    selected_character_data = next(
        (char for char in character_data if char["name"] == selected_character.name), None
    )
    if not selected_character_data:
        print("Selected character data not found.")
        return None, None

    # Step 4: Load character in loader
    loaded_characters = loader.load_characters(selected_character_data)

    return loaded_characters[0], region
    
    # Step 5: Start gameplay
    start_gameplay(selected_character, region)

def select_character_menu(characters):
    """Allow the user to select a character."""
    print("\nCharacter Selection Menu:")
    print("Available Characters:")
    for i, char in enumerate(characters):
        print(f"{i + 1}. {char.name} ({char.faction})")

    try:
        choice = int(input("Enter the number of your choice: ")) - 1
        if 0 <= choice < len(characters):
            selected_character = characters[choice]
            print(f"You selected: {selected_character.name}")
            return selected_character
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

def load_region_mappings():
    region_file = get_file_path("scifiRPG", "data", "Test City", "Locations", "test_city.json")
    print(f"Looking for region file at: {region_file}")  # Debugging print
    
    try:
        with open(region_file, "r") as file:
            data = json.load(file)
            print(f"Loaded region mappings: {data}")  # Debug print
            return data
    except FileNotFoundError:
        print(f"Error loading region mappings: {region_file} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {region_file} contains invalid JSON.")
        return {}

def select_region_menu():
    """Allow the user to select a region."""

    region_mappings = load_region_mappings()
    
    if not region_mappings:  # Check if region_mappings is empty
        print("Error: No region mappings available.")
        return None

    region_list = list(region_mappings.keys())

    print("Available regions:")
    for idx, region in enumerate(region_list, 1):
        print(f"{idx}. {region}")  # Display the region name to the user
    
    try:
        selected_index = int(input("Select a region by number: ")) - 1
        if 0 <= selected_index < len(region_list):
            selected_region = region_list[selected_index]
        # Return the full Region object
            return Region(
                name=selected_region,
                nameForUser=region_mappings[selected_region]
            )
        else:
            print("Invalid region selected. Exiting.")
            return None
    except ValueError:
        print("Invalid input. Exiting.")
        return None

def show_character_details(character):
    """Display character details."""
    print("\nCharacter Details:")
    character_table = [
        ["Name", "Role", "Faction", "Money", "Hunger", "Inventory"],
        [
            character.name,
            getattr(character, "char_role", "N/A"),
            character.faction,
            f"${getattr(character, 'bankCardCash', 0):.2f}",
            getattr(character, "hunger", "N/A"),
            ", ".join(getattr(character, "inventory", [])),
        ],
    ]
    print(tabulate(character_table, headers="firstrow", tablefmt="grid"))
    #add a second row with 'Current location' showing selected characters current_location, current_region

def show_locations_in_region(region, locations):
    """Display locations in the specified region."""
    print(f"\nAvailable Locations in {region}:")
    if not locations:
        print("No locations available in this region.")
        return

def show_shop_inventory(shop):
    """Display inventory of a specific shop."""
    print(f"\nShop: {shop.name}")
    inventory = shop.inventory
    if inventory:
        inventory_table = [
            [item, details.get("price", "N/A"), details.get("quantity", 0)]
            for item, details in inventory.items()
        ]
        print(tabulate(inventory_table, headers=["Item", "Price", "Quantity"], tablefmt="grid"))
    else:
        print("This shop has no items available.")

def display_selected_character_current_region(character, region):
    print(f"{character.name} is in {region.nameForUser}.")