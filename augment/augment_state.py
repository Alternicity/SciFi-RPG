#augment.augment_state.py

from create.create_game_state import get_game_state
game_state = get_game_state()

def augment_municipal_buildings():

    state = game_state.state

    if not state:
        return

    state.government_buildings.clear()

    for municipal in game_state.municipal_buildings.values():#values bc we are addressing a dictionary

        state.government_buildings.append(municipal)