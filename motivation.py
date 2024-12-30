#possible cruft, pasted here 

class Motivation:
    VALID_MOTIVATIONS = [
        "earn_money",
        f"gain_{Status.LOW.value}",
        f"gain_{Status.MID.value}",
        f"gain_{Status.HIGH.value}",
        f"gain_{Status.ELITE.value}",
        "protect_vip",
        "steal_money",
        "steal_object",
        "escape_danger",
    ]

    def __init__(self, initial_motivation="earn_money"):
        if initial_motivation not in self.VALID_MOTIVATIONS:
            raise ValueError(
                f"Invalid motivation: {initial_motivation}. Valid options are {self.VALID_MOTIVATIONS}"
            )
        self.current = initial_motivation

    def change_motivation(self, new_motivation):
        if new_motivation in self.VALID_MOTIVATIONS:
            print(f"Motivation changed to {new_motivation}")
            self.current = new_motivation
        else:
            print(f"Invalid motivation: {new_motivation}")

    def __init__(self, name, behaviour="passive", motivation="earn_money"):
        self.name = name
        self.behaviour = self.Behaviour(behaviour)
        self.motivation = self.Motivation(motivations)

    def display_character_state(self):
        print(
            f"{self.name}'s behaviour: {self.behaviour.current}, motivation: {aelf.motivation.current}"
        )