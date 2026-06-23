#economy.workforce.staffing.py
import random
from utils import employ_npc
from characters import Child, SpecialChild
from employment.roles import EmployeeRole, BARTENDER, BOUNCER, DJ, CLUB_MANAGER
from create.create_game_state import get_game_state
game_state = get_game_state()
from character_components.economic_profile import EconomicProfile
from employment.employment_helpers import is_employed

def assign_staff_to_club(
    club,
    candidates,
    staffing
):

    random.shuffle(candidates)

    for role, count in staffing:

        for _ in range(count):

            if not candidates:
                return

            worker = candidates.pop()

            worker.location = club
            worker.region = club.region

            employ_npc(
                worker,
                club,
                role,
                shift="night",
                shift_start=1,
                shift_end=5
            )
            if hasattr(club.owner, "active_workers"):

                if worker not in club.owner.active_workers:
                    club.owner.active_workers.append(worker)

                if (
                    hasattr(club.owner, "available_workers")
                    
                    and worker in club.owner.available_workers
                ):
                    club.owner.available_workers.remove(worker)
                    
            if worker not in club.employees_there:
                club.employees_there.append(worker)

def staff_from_corporation_pool(club, owner):
    staffing = [
        (BARTENDER, 2),
        (BOUNCER, 1),
        (DJ, 1),
        (CLUB_MANAGER, 1),
    ]

    #useful
    #print ("from staff_from_corporation_pool")
    #print(owner.name, len(owner.available_workers))

    candidates = [
        npc for npc in owner.available_workers
        if not isinstance(npc, (Child, SpecialChild))
    ]

    # fallback to civilians if corporation exhausted
    if len(candidates) < 5:

        extra = [
            npc for npc in game_state.civilians
            if not is_employed(npc)
        ]

        candidates.extend(extra)

    assign_staff_to_club(
        club,
        candidates,
        staffing
    )

def staff_from_gang_and_civilians(club, owner):

    civilian_candidates = []
    gang_candidates = []

    service_staffing = [
        (BARTENDER, 2),
        (DJ, 1),
        (CLUB_MANAGER, 1),
    ]

    security_staffing = [
        (BOUNCER, 1),
    ]

    gs = get_game_state()
    
    # Exclude scenario/debug NPCs from general staffing
    protected_npcs = set(gs.debug_npcs.values())

    civilian_candidates = [
        npc for npc in gs.civilians
        if not is_employed(npc)
        and npc not in protected_npcs
    ]

    gang_candidates = [
        npc for npc in owner.members
        if not is_employed(npc)
    ]

    assign_staff_to_club(
        club,
        civilian_candidates,
        [
            (BARTENDER, 2),
            (DJ, 1),
        ]
    )

    assign_staff_to_club(
        club,
        gang_candidates,
        [
            (BOUNCER, 1),
            (CLUB_MANAGER, 1),
        ]
    )

    #manager can be a GangCaptain
    #bouncers can be GangMembers


def staff_from_civilians(club):
    pass

#I need to ensure some npcs of class Babe are created