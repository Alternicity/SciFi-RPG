# gameplay.py
from display import show_character_details, show_locations_in_region, display_selected_character_current_region
from loader import initialize_shops
from dataclasses import dataclass, field

from common import get_project_root, get_file_path
#ALL files use this to get the project root

def gameplay(character, region):
    """Manage gameplay flow with character interaction and region data."""

    # Ensure region are objects with a 'name' attribute
    if not hasattr(character, 'name'):
        raise ValueError("Both character and region must be objects with a 'name' attribute.")
    
    print(f"Entering gameplay with {character.name} in {region.nameForUser}.")

    # Show character details and any immediate needs/motivations
    show_character_details(character)
    print("\nYou can also view the full character profile for more details.")
    #show any pressing neeeds/motivations, ie "Character_name is hungry"

    # Use nameForUser for user-facing messages, and `name` for programmatic references

    print(f"\n{character.name} is in the {region.nameForUser} region.")
    print("You can buy and sell items here.")

    if region.locations:
        print("Locations in this region:")
        for location in region.locations:
            print(f"- {location.name}")
    else:
        print("This region has no locations yet.")

    # Gameplay loop
    while True:
        print("\n=== Gameplay Menu ===")
        action = input("Choose action: (1) Visit Location (2) Move to other region (3) Display character's current region (4) Exit: ")

        if action == "1":
            print("\nChoose a location to visit:")
            # Display available locations (shops for now)
            for idx, shop in enumerate(shops, start=1):
                print(f"({idx}) {shop.name}")
            try:
                choice = int(input("Select a location by number: ")) - 1
                if 0 <= choice < len(shops):
                    selected_shop = shops[choice]
                    print(f"Character {character.name} enters {selected_shop.name}.")
                    # Add character to location's list of visitors
                    # Present buy/sell/action menu
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif action == "2":
            print("\nMoving to another region...")
            # Add traveling logic here
            #print(f"Entering region: {region.nameForUser}")

        elif action =="3":
            # Assuming `selected_character` and `current_region` are defined elsewhere
            display_selected_character_current_region(selected_character, current_region)

        elif action == "4":
            print("\nExiting gameplay.")
            break

        else:
            print("\nInvalid choice. Please try again.")
