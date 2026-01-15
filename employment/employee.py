#employment.employee.py
from dataclasses import dataclass, field
from typing import List, Callable, Optional, TYPE_CHECKING, Literal
from employment.roles import EmployeeRole

if TYPE_CHECKING:
    from base.location import Location
    from base.character import Character

@dataclass
class EmployeeProfile:
    
    shift_start: int = 9
    shift_end: int = 17
    workplace: Optional["Location"] = None
    role: Optional[EmployeeRole] = None
    shift: str = "day"  # day/night

    #hmmm
    role: Literal["front_of_house", "back_of_house", "management", "labor"]

    # Runtime state (ephemeral, not serialized)
    is_on_shift: bool = False
    just_got_off_shift: bool = False
    #set/reset them only inside update_employee_presence

    def on_duty(self, hour: int) -> bool:
        if self.shift == "day":
            return self.shift_start <= hour < self.shift_end
        else:
            return hour >= self.shift_start or hour < self.shift_end

