#world.scenarios.economy.assign_corporation_ownership.py
from location.locations import Factory, Powerplant
import random
from create.create_game_state import get_game_state
game_state = get_game_state()

def assign_corporation_ownership():
    #print("[DEBUG] assign_corporation_ownership called")

    game_state = get_game_state()

    corporations = game_state.corporations

    factories = [
        loc for loc in game_state.all_locations
        if isinstance(loc, Factory)
    ]

    powerplants = [
        loc for loc in game_state.all_locations
        if isinstance(loc, Powerplant)
    ]

    for location in factories + powerplants:

        corp = random.choice(corporations)

        from economy.economy_helpers import assign_location_owner

        assign_location_owner(
            location,
            corp
        )
        #notes Corporations have an HQ, with a region, this might be useful here
        #Parks, Libraries, MunicipalBuilding, can be excluded from corporate ownership
        #ApartmentBlock, Farm and House locations - 50% of them can be corporate owned
        
        
        """ Step B — THEN worker assignment

        After ownership exists:

        for corp in game_state.corporations:
            assign_corporate_workers(corp) """

