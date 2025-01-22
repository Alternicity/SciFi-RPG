from tabulate import tabulate
import logging
from character_creation import create_characters_as_objects
import loader
import os
from city_utils import regenerate_city_data
from characters import Manager, Civilian, Character
from location import Region
import json
from region_startup import regions_with_wealth
from LoaderRuntime import load_locations_from_yaml

from common import get_project_root, get_file_path, BASE_REGION_DIR, BASE_SHOPS_DIR
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

    # List of region names
    valid_regions = ["North", "East", "West", "South", "Central"]

    region_mappings = {}
    for region in valid_regions:
        # Construct the region file path using BASE_REGION_DIR
        region_file_path = os.path.join(BASE_REGION_DIR, f"{region}.json")
        #print(f"Looking for region file at: {region_file_path}")  # Debugging print
        
        try:
            # Open the respective region file
            with open(region_file_path, "r") as file:
                data = json.load(file)
                region_mappings[region] = data  # Add region mappings to the dictionary
                # Only print brief info about the region here
                print(f"Loaded region data for {region}: {data.get('nameForUser', 'Unknown Region Name')}")

        except FileNotFoundError:
            print(f"Error loading region mappings for {region}: {region_file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error: {region_file_path} contains invalid JSON.")
    
    return region_mappings

def select_region_menu():
    """Allow the user to select a region."""

    region_mappings = load_region_mappings()
    
    if not region_mappings:  # Check if region_mappings is empty
        print("Error: No region mappings available.")
        return None

    # Prepare region data for display
    region_list = [
        [idx + 1, data.get("nameForUser", region), data.get("wealth", "Unknown")]
        for idx, (region, data) in enumerate(region_mappings.items())
    ]

    # Display the regions using tabulate
    print("\nAvailable Regions:")
    print(tabulate(region_list, headers=["#", "Region", "Wealth"], tablefmt="pretty"))

    try:
        # Prompt user for selection
        selected_index = int(input("\nSelect a region by number: ")) - 1

        # Validate the selected index
        if 0 <= selected_index < len(region_list):
            selected_region_key = list(region_mappings.keys())[selected_index]
            selected_region_data = region_mappings[selected_region_key]
            return Region(
                name=selected_region_key,
                nameForUser=selected_region_data["nameForUser"]
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

def show_locations_in_region(region):
    """Display locations in the specified region."""
    locations_data = load_locations_from_yaml(region)
    if not locations_data:
        print(f"No locations found in {region}.")
        return
    
    print(f"Locations in {region}:")
    for location in locations_data:
        print(f"- {location['name']} (Type: {location['type']}, Security Level: {location['security_level']})")

    # Prepare the data for tabulation: list of location names
    location_data = [[loc['name']] for loc in locations_data]
    
    # Tabulate the data
    print(tabulate(location_data, headers=["Location Name"], tablefmt="pretty"))


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