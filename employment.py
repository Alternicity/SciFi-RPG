# employment.py
from dataclasses import dataclass, field
from typing import List, Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from location import Location
    from base_classes import Character

@dataclass
class EmployeeRole:
    name: str
    responsibilities: List[str] = field(default_factory=list)
    priority: int = 5  # 1=critical, 10=low urgency

    def get_tasks(self, npc: "Character", workplace: "Location") -> List[str]:
        """Return list of tasks NPC should perform this tick."""
        return self.responsibilities
