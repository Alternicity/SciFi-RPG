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
from create import create_all_regions, create_region
from common import get_project_root, get_file_path, BASE_REGION_DIR, BASE_SHOPS_DIR

# Setup logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n=== Main Menu ===")
        print("1: Create Characters (Game Objects)")
        print("2: Create Characters (Serialized Data)")
        print("3: Load Serialized Characters")
        print("4: Play/Test Game")
        print("5: Regenerate City Data")
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
                # Start game logic, calling `character_and_region_selection` 
                selected_character, region = character_and_region_selection()  # Expecting returned variables here

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

def character_and_region_selection():
    """Start the game and handle character and region selection."""
    print("Starting game...")

    # Predefined characters to select from character_creation.py
    characters = create_characters_as_objects()

    # Step 1: Select character
    selected_character = select_character_menu(characters)
    if not selected_character:
        print("Character selection failed.")
        return None, None
    
    # Step 2: Load regions as Region objects
    region_names = ["Central", "East", "North", "South", "West"]
    regions = []
    for name in region_names:
        try:
            region = create_region(name)  # create_region loads the JSON and instantiates a Region
            regions.append(region)
        except Exception as e:
            print(f"Error loading region '{name}': {e}")

    if not regions:
        print("No regions available. Exiting game.")
        return selected_character, None

    # Step 3: Select region
    selected_region = select_region_menu(regions)
    if not selected_region:
        print("Region selection failed.")
        return selected_character, None

    return selected_character, selected_region
    
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

def select_region_menu(regions):
    """Display a menu to select a region."""
    table = [
        [i + 1, region.nameForUser, f"({region.name})"] for i, region in enumerate(regions)
    ]
    print(tabulate(table, headers=["#", "Region", "Code"], tablefmt="grid"))

    try:
        choice = int(input("Select a region by number: ")) - 1
        if 0 <= choice < len(regions):
            selected_region = regions[choice]
            print(f"Selected region: {selected_region.nameForUser}")
            return selected_region
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
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
    #locations_data = load_locations_from_yaml(region)

    if not locations:
        print(f"No locations found in {region.nameForUser}.")
        return
    
    # Prepare the data for tabulation
    table_data = []
    for location in locations:
        # Extract relevant fields
        name = getattr(location, "name", "Unknown Name")
        condition = getattr(location, "condition", "Unknown Condition")
        fun = getattr(location, "fun", "N/A")
        security_level = getattr(location.security, "level", "N/A") if hasattr(location, "security") else "N/A"

        # Add to table data
        table_data.append([name, condition, fun, security_level])

    # Display the table
    headers = ["Name", "Condition", "Fun", "Security Level"]
    print(tabulate(table_data, headers=headers, tablefmt="grid")) #try also tablefmt="pretty"

#Shop:
def show_shop_inventory(shop):
    """Display the inventory of a shop in a tabulated format."""
    if not shop.inventory:
        print(f"{shop.name} has no items available.")
        return

    # Prepare the data for tabulation
    table_data = []
    for item, details in shop.inventory.items():
        table_data.append([item, details.get("price", "N/A"), details.get("quantity", 0)])

    # Display the table
    headers = ["Item", "Price", "Quantity"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def display_selected_character_current_region(character, region):
    print(f"{character.name} is in {region.nameForUser}.")