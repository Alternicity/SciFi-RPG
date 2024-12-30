class Grunt(Subordinate):
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, char_role="Grunt", faction=faction, motivation="earn money", status=Status.LOW, **kwargs
        )

    def setBehaviour(self, new_behaviour):
        if new_behaviour in self.VALID_BEHAVIOURS:
            print(f"{self.name} changes behaviour to {new_behaviour}")
            self.behaviour = new_behaviour
        else:
            print(f"Invalid behavior: {new_behaviour}")

    def decide_action(self):
        """
        Decide the next action based on behaviour and motivation.
        """

        if self.behaviour == "dead":
            return "No action - character is dead"

        if self.motivation == "earn money":
            if self.behaviour == "passive":
                return "Looks for a job or collects money"
            elif self.behaviour == "aggressive":
                return "Demands money from others or loots"
        elif self.behaviour == "protect_vip":
            if self.behaviour in ["stealth", "aggressive"]:
                return "Guards or hides near the VIP."
        elif self.motivation == "steal_money":
            if self.behaviour == "stealth":
                return "Attempts to pickpocket"
            elif self.behaviour == "aggressive":
                return "Initiates a robbery"

        return "No valid action found"

    

    def display_stats(self):
        print(f"Name: {self.name}")
        print(f"Sex: {self.sex}")
        print(f"Race: {self.race}")
        print(f"Role: {self.char_role}")
        print(f"Strength: {self.strength}")
        print(f"Agility: {self.agility}")
        print(f"Intelligence: {self.intelligence}")
        print(f"Health: {self.health}")
        print(f"Psy: {self.psy}")
        print(f"Toughness: {self.toughness}")
        print(f"Morale: {self.morale}")
        print(f"ArmourValue: {self.armorValue}")
        print(f"Behaviour: {self.behaviour}")

    

    def can_perform_action(self, action_type):
        """
        Checks if an action is allowed based on the current behaviour.
        :param action_type: Action to check.
        :return: True if the action is allowed, False otherwise.
        """
        return action_type in self.allowed_actions.get(self.behaviour_type, [])

    


def show_inventory(self):
    # Delegate to the inventory instance
    print(f"{self.name}'s inventory:")
    self.inventory.display_items()