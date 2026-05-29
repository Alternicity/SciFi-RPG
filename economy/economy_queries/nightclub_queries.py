#economy.economy_queries.nightclub_queries.py

from location.locations import Nightclub
from employment.roles import (
    BARTENDER,
    BOUNCER,
    DJ,
    CLUB_MANAGER
)

def get_nightclub_economy_data(club):

    employees = getattr(
        club,
        "employees_there",
        []
    )

    bartenders = [
        e for e in employees
        if (
            hasattr(e, "employment")
            and e.employment
            and e.employment.role == BARTENDER
        )
    ]

    bouncers = [
        e for e in employees
        if (
            hasattr(e, "employment")
            and e.employment
            and e.employment.role == BOUNCER
        )
    ]

    djs = [
        e for e in employees
        if (
            hasattr(e, "employment")
            and e.employment
            and e.employment.role == DJ
        )
    ]

    managers = [
        e for e in employees
        if (
            hasattr(e, "employment")
            and e.employment
            and e.employment.role == CLUB_MANAGER
        )
    ]

    return {

        "employees": len(employees),

        "bartenders": len(bartenders),

        "bouncers": len(bouncers),

        "djs": len(djs),

        "managers": len(managers),

        "fun": getattr(club, "fun", 0),

        "upkeep": getattr(club, "upkeep", 0),

        "security_level": (
            club.security.level
            if getattr(club, "security", None)
            else 0
        ),
    }