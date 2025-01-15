from dataclasses import dataclass, field
from typing import List

@dataclass
class Security:
    level: int = 0  # Overall security level (e.g., 1-10 scale)
    guards: List[str] = field(default_factory=list)  # List of guard types (e.g., "Basic Guard", "Elite Guard")
    difficulty_to_break_in: int = 0  # Numerical representation of difficulty (e.g., higher is harder)
    surveillance: bool = False  # Whether the location has surveillance cameras
    alarm_system: bool = False  # Whether the location has an alarm system
