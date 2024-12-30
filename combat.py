def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"{self.name} equipped {weapon.name}")

        def is_alive(self):
        return self.health > 0 and self.behaviour != "dead"

    def take_damage(self, damage):

        # Calculate reduced damage based on toughness, armor, and prevent received
        # damage from being negative, due to armor, acccidentally healing character
        receivedDamage = max(0, damage - (self.toughness / 4) - self.armorValue)
        self.health -= receivedDamage

        # Don't let health go below zero
        if self.health < 0:
            self.health = 0

            if self.armorValue > 0:
                self.armorValue -= self.armorValue - receivedDamage / 4

                if self.armorValue <= 0:
                    self.armorValue = 0
                    self.isArmored = False

def attack(self, target):
        if self.weapon:
            damage = self.weapon.use()
            target.take_damage(damage)
        else:
            print(f"{self.name} has no weapon equipped")
        if weapon and weapon["isArmed"]:
            print(f"{self.name} attacks {target.name} with {weapon_name}.")
            damage = random.randint(10, 20)  # Example damage calculation
            self.deplete_weapon_resource(weapon)

            # delete the following?
            if "ammo" in weapon:  # Handle ammo for ranged weapons
                weapon["ammo"] -= 1
                if weapon["ammo"] <= 0:
                    weapon["isArmed"] = False
                    print(
                        f"{self.name}'s {weapon.get('name', 'weapon')} is out of ammo."
                    )
                    # Use get to avoid errors if name is missing from weapon

            if "charge" in weapon:  # Handle charge for energy weapons
                weapon["charge"] -= 1
                if weapon["charge"] <= 0:
                    weapon["isArmed"] = False
                    print(
                        f"{self.name}'s {weapon.get('name', 'weapon')} is out of charge."
                    )


def deplete_weapon_resource(self, weapon):
    if "ammo" in weapon:
        weapon["ammo"] -= 1
        if weapon["ammo"] <= 0:
            weapon["isArmed"] = False
            print(f"{self.name}'s weapon is out of ammo")
    elif "charge" in weapon:
        weapon["charge"] -= 1
        if weapon["charge"] <= 0:
            weapon["isArmed"] = False
            print(f"{self.name}'s weapon is out of charge")


def Die(self):
    print(f"{self.name} has died")