#Possibly deprecated code, pasted here for now
from enum import Enum, auto

class Behaviour(Enum):
    DEAD = "dead"
    UNCONSCIOUS = "unconscious"
    PASSIVE = "passive"
    AGGRESSIVE = "aggressive"
    STEALTH = "stealth"
    MURDEROUS = "murderous"
    FLIRTY = "flirty"
    SELLING = "selling"
    DEFAULT = "default"

# Define allowed behaviors for each state
ALLOWED_BEHAVIOURS = {
    Behaviour.DEAD: [],
    Behaviour.UNCONSCIOUS: [],
    Behaviour.DEFAULT: ["earn", "enjoy"],
}

def get_allowed_behaviours(behaviour):
    """Returns the allowed behaviours for a given behaviour type."""
    return ALLOWED_BEHAVIOURS.get(behaviour, [])

def set_default_behaviour():
    """Returns a default set of behaviours."""
    return {Behaviour.DEFAULT}

class BehaviourManager:
    """Manages character behaviours."""

    def __init__(self, behaviour=Behaviour.DEFAULT):
        self.behaviour_type = behaviour

    def change_behaviour(self, new_behaviour):
        """Change the character's behaviour if it's valid."""
        if not isinstance(new_behaviour, Behaviour):
            raise ValueError(f"Invalid Behaviour: {new_behaviour}")
        self.behaviour_type = new_behaviour




    