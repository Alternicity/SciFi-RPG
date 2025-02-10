# gameplay.py
from region_utils import get_all_regions
#remove all object creation from this file and dont let it back in
from menu_utils import get_menu_choice
from characterActions import move_character, visit_location
from display import (
    show_character_details,
    display_selected_character_current_region,
    display_character_location,
    show_region_choices,
    display_filtered_character_summary,
)
from motivation import check_needs


def gameplay(character, region):
    """Manage gameplay flow with character interaction and region data."""

    # Ensure character whereabouts are displayed properly
    show_character_details(character)
    display_selected_character_current_region(character, region)

    # Show any pressing needs/motivations
    check_needs(character, is_player=character.is_player)

    # Display locations in the region
    if hasattr(region, 'locations'):
        from display import show_locations_in_region
        show_locations_in_region(region, region.locations)
    else:
        print(f"No locations found in {region.name}.")

    # Main Gameplay Loop
    while True:
        print("\n=== Gameplay Menu ===")
        display_character_location(character)  # Ensure proper whereabouts are shown

        options = {
            "1": ("Visit Location", visit_location),
            "2": ("Move to another Region", move_region),
            "3": ("Display Characters Summary", view_characters),
            "4": ("Exit Gameplay", exit_gameplay),
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


def view_characters(character, region):
    """Displays filtered character summaries."""
    display_filtered_character_summary()


def exit_gameplay(character, region):
    """Exits the gameplay loop."""
    print("\nExiting gameplay.")
    exit()