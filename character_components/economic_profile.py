#character_components.economic_profile.py
from base.character import Character
from base.location import Location
from employment.roles import EmployeeRole
from dataclasses import dataclass


@dataclass
class EconomicProfile:
    workplace: "Location" = None
    role: "EmployeeRole" = None

    # Future fields (earnings, consumption, debt, spending patterns)
    income_per_day: int = 0
    spending_rate: float = 1.0
    partner: "Character" = None   # For household wealth analysis

    def is_employed(self):
        return self.workplace is not None
