#Possibly deprecated code, pasted here for now
class Behaviour(Enum):

    def __init__(self, behaviour_type="passive"):
        self.behaviour_type = behaviour_type
        self.allowed_actions = {
            "dead": [],
            "unconscious": [],
            "aggressive": ["attack", "defend"],
            "stealth": ["sneak", "hide"],
            "passive": ["heal", "defend"],
            "murderous": ["attack"],
        }.get(behaviour_type, [])

    def change_behaviour(self, new_behaviour):
        allowed_behaviours = [
            "stealth",
            "aggressive",
            "passive",
            "murderous",
            "unconscious",
            "dead",
        ]
        if new_behaviour in allowed_behaviours:
            self.behaviour_type = new_behaviour
        else:
            raise ValueError(f"Invalid Behaviour: {new_behaviour}")
self.behaviour.change_behaviour("aggressive")  # Set default behaviour
        self.weapons = {
            "pistol": {"isArmed": True, "ammo": 30},
            "tazer": {"isArmed": True, "tazerCharge": 10},

        self.behaviour.change_behaviour("murderous")  # default behaviour
        self.behaviour.change_behaviour("stealth")  # default behaviour
        self.behaviour.change_behaviour("aggressive")  # default behaviour
        self.behaviour.change_behaviour("passive")  # default behaviour
