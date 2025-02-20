#game.py
#Call gameplay(character, region)
from menu_utils import select_character_menu, main_menu
from loader import load_region_data
from gameplay import gameplay
from character_creation_funcs import player_character_options
from create import all_regions
def game():
    """Main game loop."""

    while True:
        choice = main_menu()

        if choice == 1:
            selected_character, selected_region = character_and_region_selection(all_regions)
            if selected_character and selected_region:
                gameplay(selected_character, selected_region)
            else:
                print("Returning to main menu.")
        
        elif choice == 6:
            print("Exiting game.")
            break

def character_and_region_selection(all_regions):
    """Handles both character and region selection in one function."""
    print("Starting game...")

    selected_character = select_character_menu(player_character_options(all_regions))
    if not selected_character:
        return None, None
    
    from display import select_region_menu
    selected_region = select_region_menu(load_region_data())
    return selected_character, selected_region

if __name__ == "__main__":
    game()

