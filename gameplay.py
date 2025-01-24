# gameplay.py
from display import show_character_details, show_locations_in_region, display_selected_character_current_region
from loader import initialize_shops
from dataclasses import dataclass, field
from location import CorporateStore, Shop
from LoaderRuntime import load_locations_from_yaml
from create import create_locations, associate_locations_with_region
from common import get_project_root, get_file_path
from region_utils import get_all_regions
#ALL files use this to get the project root

def gameplay(character, region):
    """Manage gameplay flow with character interaction and region data."""

    """ # Ensure region are objects with a 'name' attribute
    if not hasattr(character, 'name'):
        raise ValueError("Both character and region must be objects with a 'name' attribute.")
     """
    # Set the character's initial location
    character.update_location(region, None)  # No specific location initially

    # Create locations for the region
    locations = create_locations(region.name)
    region = associate_locations_with_region(region, locations)
    
    show_character_details(character)
    #show any pressing neeeds/motivations, ie "Character_name is hungry"

    # Use nameForUser for user-facing messages, and `name` for programmatic references
    print(f"\n{character.name} is in the {region.nameForUser} region.")
    #This needs to be dealt with by display.py
    
# Call display function for locations - dynamic, yaml
    # Retrieve locations from the region object
    if hasattr(region, 'locations'):
        locations = region.locations  # Access the locations attribute of the region
        show_locations_in_region(region, locations)  # Pass locations to the display function
    else:
        print(f"No locations found in {region.nameForUser}.")

    # Gameplay loop
    while True:
        print("\n=== Gameplay Menu ===")
        print(f"Current Region: {character.get_current_region().nameForUser}")
        print(f"Current Location: {character.get_current_location().name if character.get_current_location() else 'In transit'}")

        action = input("Choose action: (1) Visit Location (2) Move to other region (3) Display character's current region (4) Exit: ")

        if action == "1":
            print("\nChoose a location to visit:")
            for idx, location in enumerate(region.locations, start=1):#Use display.py here
                print(f"({idx}) {location.name}")
            try:
                choice = int(input("Select a location by number: ")) - 1
                if 0 <= choice < len(region.locations):
                    selected_location = region.locations[choice]
                    print(f"Character {character.name} enters {selected_location.name}.")
                    #update that character's current_location
                    # eventually update region and locations current_characters lists

                    # Check if the location is a Shop or CorporateStore
                    if isinstance(selected_location, (Shop, CorporateStore)):
                        if isinstance(selected_location, Shop):
                            from display import show_shop_inventory
                            show_shop_inventory(selected_location)
                        elif isinstance(selected_location, CorporateStore):
                            print(f"{selected_location.name} is a corporate store. Items are issued based on status.")
                    else:
                        print(f"{selected_location.name} is not a vendor.")
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif action == "2":
            print("\nMoving to another region...")
            # List available regions
            regions = get_all_regions()  # Implement this function to return a list of Region objects
            for i, reg in enumerate(regions, start=1):
                print(f"{i}. {reg.nameForUser}")

            try:
                choice = int(input("Select a region by number: ")) - 1
                if 0 <= choice < len(regions):
                    selected_region = regions[choice]
                    character.update_location(selected_region, None)  # Reset location within the region
                    print(f"{character.name} has moved to {selected_region.nameForUser}.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")

        elif action == "3":
            # Display the current region and location
            print(f"\n{character.name} is currently in {character.get_current_region().nameForUser}.")
            if character.get_current_location():
                print(f"Current Location: {character.get_current_location().name}")

            #instead, use:
            display_selected_character_current_region(character, region)
            #check this works correctly


        elif action == "4":
            print("\nExiting gameplay.")
            break

        else:
            print("\nInvalid choice. Please try again.")
