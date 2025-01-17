from tabulate import tabulate
from characters import Character
import logging
import time
from utils import list_characters
from character_creation import create_characters_as_objects
from loader import load_shops
#import loader
import os
# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def display_menu():
    """
    Displays the main menu and handles user choices.
    """
    characters = []  # Initialize as an empty list for later use

    while True:
        print("\n=== Main Menu ===")
        print("1: Create Characters (Game Objects)")
        print("2: Create Characters (Serialized Data)")
        print("3: Load Serialized Characters")
        print("4: Play/Test Game")
        print("5: Exit")

        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
            if choice == 1:
                # Create characters as objects
                characters = create_characters_as_objects()  # Now doesn't require list_characters
                print("\n=== Character Information ===")
                print(list_characters(characters))  # Call list_characters separately
            elif choice == 2:
                # Placeholder for serialization feature
                print("Feature to create and serialize characters is under development.")
            elif choice == 3:
                # Placeholder for loading serialized data
                print("Feature to load serialized characters is under development.")
            elif choice == 4:
                # Placeholder for game/test logic
                if characters:
                    print("Starting game with current characters...")
                else:
                    print("No characters created yet. Please create characters first.")
            elif choice == 5:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            time.sleep(1)

def select_character_menu(characters):
    """
    Displays a list of characters for the user to select.
    """
    print("\nCharacter Selection Menu:")
    print("Available Characters:")
    for index, character in enumerate(characters, 1):
        print(f"{index}. {character.name}")  # Assuming 'name' is an attribute of the character object

    try:
        choice = int(input("Select a character by number: "))
        selected_character = characters[choice - 1]  # Adjust for 0-based indexing
        return selected_character
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None
       
def select_region_menu():
    region_list = ["North", "East", "West", "South", "Central"]
    
    # Display available regions with numbers
    print("Available regions:")
    for idx, region in enumerate(region_list, 1):
        print(f"{idx}. {region}")
    
    # Get user input as a number
    try:
        selected_index = int(input("Select a region by number: ")) - 1
        if 0 <= selected_index < len(region_list):
            selected_region = region_list[selected_index]
            return selected_region
        else:
            print("Invalid region selected. Exiting.")
            return ""
    except ValueError:
        print("Invalid input. Exiting.")
        return ""

def show_character_details(character):
    """
    Display details of the selected character.
    
    Args:
        character (Character): An instance of the Character class or its subclasses.
    """
    print("\nCharacter Details:")
    character_table = [
        ["Name", character.name],
        ["Role", getattr(character, "char_role", "N/A")],  # Use getattr to handle missing attributes
        ["Faction", character.faction],
        ["Money", f"${getattr(character, 'bankCardCash', 0):.2f}"],
        ["Hunger", getattr(character, "hunger", "N/A")],
        ["Inventory", ", ".join(getattr(character, "inventory", []))]
    ]

    print(tabulate(character_table, headers=["Attribute", "Value"], tablefmt="grid"))
    print()

def show_shops_in_region(region):
    """Display the list of shops for the given region."""
    logger.debug("Entered function XYZ")
    print(f"Region passed to show_shops_in_region: {region}")  # Debug print
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug("About to call load_shops from loader.py")
    shops = load_shops(region) #like this because from "loader import load_shops"
    
    if not shops:
        print(f"No shops found in {region} region.")
        return
    
    print(f"Shops in {region} region:")
    for shop in shops:
        print(f"- {shop.name}")
        print(f"Type: {shop.__class__.__name__}")
        print(f"Security Level: {shop.security['level']}")
        show_shop_inventory(shop)


def show_shop_inventory(shop):
    """
    Display the inventory of a specific shop.
    
    Args:
        shop (Shop): The shop object or dictionary.
    """
    print(f"\nShop: {shop.name if hasattr(shop, 'name') else shop.get('name', 'Unknown Shop')}")
    inventory = shop.inventory if hasattr(shop, 'inventory') else shop.get("inventory", {})
    if inventory:
        inventory_table = [
            [item, details.get("price", "N/A"), details.get("quantity", 0)]
            for item, details in inventory.items()
        ]
        print(tabulate(inventory_table, headers=["Item", "Price", "Quantity"], tablefmt="grid"))
    else:
        print("This shop has no items available.")


if __name__ == "__main__":
    characters = []  # Initialize characters list
    display_menu(characters)
