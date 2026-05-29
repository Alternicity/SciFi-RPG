#character_components.economic_profile.py
from base.character import Character
from base.location import Location
from employment.roles import EmployeeRole
from dataclasses import dataclass


@dataclass
class EconomicProfile:
    """ workplace: "Location" = None
    role: "EmployeeRole" = None """

    employer = None
    daily_income: int = 0
    savings: int = 0

    spending_rate: float = 1.0

    partner = None

    debt: int = 0

    socioeconomic_class: str = "working"

    
