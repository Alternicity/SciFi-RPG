#game.py
#Call gameplay(character, region). Player centric flow, not sim flow
from menu_utils import select_character_menu

from game_logic import gameplay
from character_creation_funcs import player_character_options
#from create import all_regions

def game(all_regions):
    selected_character, region = select_character_menu()  # Retrieve character and region
    if selected_character:
        gameplay(selected_character, region, all_regions)  # Start gameplay with the selected character
    else:
        print("No character selected. Returning to main menu.")


if __name__ == "__main__":
    game()

