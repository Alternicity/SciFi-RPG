#employment/employee.py
from dataclasses import dataclass, field
from typing import List, Callable, Optional, TYPE_CHECKING
from employment.roles import EmployeeRole



if TYPE_CHECKING:
    from base.location import Location
    from base.charcater import Character

@dataclass
class EmployeeProfile:
    workplace: Optional["Location"] = None
    role: Optional[EmployeeRole] = None
    shift: str = "day"  # day/night
    is_on_shift: bool = False

    def on_duty(self, tick) -> bool:
        return (self.shift == "day" and 6 <= tick <= 18) or \
               (self.shift == "night" and (tick > 18 or tick < 6))