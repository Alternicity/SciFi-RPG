#game.py
#Handle character creation and region selection.
#Call gameplay(character, region)


from menu_utils import select_character_menu

from loader import load_region_data
from gameplay import gameplay
from loader import load_region_data
from character_creation_funcs import player_character_options
def game():
    """Main game loop."""
    while True:
        choice = main_menu()  # Get user choice

        if choice == 1:
            # Start character & region selection
            selected_character, selected_region = character_and_region_selection()
            if selected_character and selected_region:
                gameplay(selected_character, selected_region)
            else:
                print("Returning to main menu.")
        
        elif choice == 6:
            print("Exiting game.")
            break

#deprecated?
def character_and_region_selection():
    """Handles both character and region selection in one function."""
    print("Starting game...")

    selected_character = select_character_menu(player_character_options())
    if not selected_character:
        return None, None
    
    from display import select_region_menu
    selected_region = select_region_menu(load_region_data())
    return selected_character, selected_region  # Return even if None (handled in game())



if __name__ == "__main__":
    game()

