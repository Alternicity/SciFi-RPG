#economy.nightclib_helpers.py

from location.locations import Nightclub
from create.create_game_state import get_game_state

def get_all_nightclubs():

    game_state = get_game_state()

    return [
        loc for loc in game_state.all_locations
        if isinstance(loc, Nightclub)
    ]