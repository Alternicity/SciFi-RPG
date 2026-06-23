#economy.economy_helpers.py
from location.locations import Factory, Powerplant, Nightclub
from faction import Corporation, Gang
from characters import Civilian
from economy.economy import Ownership
import random
from create.create_game_state import get_game_state
from utils import determine_owner_type
from employment.roles import (BARTENDER, BOUNCER, DJ, CLUB_MANAGER)
from utils import employ_npc
from economy.workforce.staffing import staff_from_civilians, staff_from_corporation_pool, staff_from_gang_and_civilians
game_state = get_game_state()


def get_region_powerplant(region):

    return next(
        (
            loc for loc in region.locations
            if isinstance(loc, Powerplant)
        ),
        None
    )

def get_region_factories(region):

    return [
        loc for loc in region.locations
        if isinstance(loc, Factory)
    ]

def pick_available_civilian(all_characters, exclude=None):
    #Does this giard against employing test npcs?
    exclude = exclude or set()

    civilians = [
        c for c in all_characters
        if isinstance(c, Civilian)
        and c not in exclude
        and not is_employed(c)
    ]

    if not civilians:
        
        return None

    return random.choice(civilians)#this might need to exclude the TC2 test npcs as they are civilians
    #however I think locations get created before TC2 Civilian assignment

def is_employed(npc):

    return (
        hasattr(npc, "employment")
        and npc.employment is not None
        and npc.employment.workplace is not None
    )

# economy.economy_helpers.py

def seed_corporation_workers():

    game_state = get_game_state()

    for corp in game_state.corporations:

        corp.available_workers = []

        for worker in corp.employees:

            if not is_economy_eligible(worker):
                continue

            if (
                worker.employment is None
                or worker.employment.workplace is None
            ):
                corp.available_workers.append(worker)

def seed_nightclub_workers():#hmm see also staffing.py

    game_state = get_game_state()

    clubs = [
        loc for loc in game_state.all_locations
        if isinstance(loc, Nightclub)
    ]

    for club in clubs:

        owner = club.owner

        if isinstance(owner, Corporation):

            staff_from_corporation_pool(
                club,
                owner
            )

        elif isinstance(owner, Gang):

            staff_from_gang_and_civilians(
                club,
                owner
            )

        else:

            staff_from_civilians(
                club
            )



def assign_location_owner(location, owner):
    #Never construct Ownership outside this helper again
    location.owner = owner

    location.ownership = Ownership(
        owner_type=determine_owner_type(owner),
        owner_ref=owner
    )

    if hasattr(owner, "owned_locations"):

        if location not in owner.owned_locations:
            owner.owned_locations.append(location)

def get_available_workers(workers):

    return [
        w for w in workers
        if is_economy_eligible(w)
    ]

def is_economy_eligible(worker):

    return (
        worker is not None
        and getattr(worker, "is_employee", False)

        and not getattr(worker, "is_scenario_npc", False)
    )
    #possible expansions:
    """ and not getattr(worker, "is_prisoner", False)
    and not getattr(worker, "is_retired", False) """