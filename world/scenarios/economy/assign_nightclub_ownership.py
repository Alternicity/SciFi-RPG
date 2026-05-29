#world.scenarios.economy.assign_nightclub_ownership.py

import random
from location.locations import Nightclub
from create.create_game_state import get_game_state

def assign_nightclub_ownership():

    game_state = get_game_state()

    clubs = [
        loc for loc in game_state.all_locations
        if isinstance(loc, Nightclub)
    ]

    corps = game_state.corporations
    gangs = game_state.gangs

    for club in clubs:

        roll = random.random()

        if roll < 0.4:
            owner = random.choice(corps)

        elif roll < 0.7:
            owner = random.choice(gangs)

        else:
            owner = random.choice(game_state.all_characters)#Except class Child or SpecialChild
        from economy.economy_helpers import assign_location_owner
        assign_location_owner(club, owner)

        if hasattr(owner, "owned_locations"):

            if club not in owner.owned_locations:
                owner.owned_locations.append(club)