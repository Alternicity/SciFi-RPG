# gameplay.py
from region_utils import get_all_regions
#remove all object creation from this file and dont let it back in
from menu_utils import get_menu_choice
from characterActions import move_character, visit_location
from display import (
    show_character_details,
    display_selected_character_current_region,
    display_filtered_character_summary,
)
from motivation import MotivationManager


def gameplay(character, region):
    """Manage gameplay flow with character interaction and region data."""

    # Ensure character whereabouts are displayed properly
    show_character_details(character)
    display_selected_character_current_region(character, region)

    # Update motivations before displaying
    character.motivation_manager.update_motivations()

    # Get the most urgent motivations
    urgent_motivations = character.motivation_manager.get_urgent_motivations()

    # Show pressing needs/motivations
    if urgent_motivations:
        motivation_list = ", ".join(urgent_motivations)
        if character.is_player:
            print(f"You feel the urge to: {motivation_list}.")
        else:
            print(f"{character.name} feels the urge to: {motivation_list}.")

    # Display locations in the region
    if hasattr(region, 'locations'):
        from display import show_locations_in_region
        show_locations_in_region(region, region.locations)
    else:
        print(f"No locations found in {region.name}.")

    # Main Gameplay Loop
    while True:
        print("\n=== Gameplay Menu ===")
        from display import display_character_whereabouts
        display_character_whereabouts(character)  # Ensure proper whereabouts are shown

        options = {
            "1": ("Visit Location", visit_location),
            "2": ("Move to another Region", move_region),
            "3": ("Display Characters Summary", view_characters),
            "4": ("Exit Gameplay", exit_gameplay),
            "5": ("Display Civilians"),
            "6": ("Display Employees"),
            "8": ("Display Corporations"),
            "9": ("Display Gangs"),


            
        }

        action = get_menu_choice(options)
        if action:
            action(character, region)


def move_region(character, region=None):
    """Handles moving a character to another region."""
    selected_region = show_region_choices(get_all_regions())

    if selected_region:
        move_character(character, selected_region)
        print(f"{character.name} has moved to {selected_region.name}.")

def show_region_choices(get_all_regions):
        #show regions the character can move to
        #maybe build a map. cannot move to diametrically opposed region without passing through Downtown, ie
        #she cant go directly from north to south region, OR if doing this, a message displays
        #"passing through Downtown (Central) on the way to destinationRegion" Here a Downtown percept or event might be triggered
    pass

def view_characters(character, region):
    """Displays filtered character summaries."""
    display_filtered_character_summary()


def exit_gameplay(character, region):
    """Exits the gameplay loop."""
    print("\nExiting gameplay.")
    exit()