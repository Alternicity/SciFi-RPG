
def calculate_intimidation_score(character, wildcard_bonus=0):
    """
    Calculates how intimidating a character is, for use in actions like robbery or threats.
    Returns an integer between (roughly) 1 and 100.
    """
    # Base from attributes (scale average of 4 stats to 1–20)
    core_attributes = [
        character.get_attribute("strength"),
        character.get_attribute("charisma"),
        character.get_attribute("toughness"),
        character.get_attribute("intelligence")
    ]
    attribute_score = sum(core_attributes) / len(core_attributes)

    # Criminal status factor: assumes status is an Enum or object with numeric severity
    try:
        criminal_modifier = int(character.status.get("criminal", 0))  # get int or use 0
    except:
        criminal_modifier = 0

    # Weapon intimidation bonus
    weapon_bonus = 0
    if hasattr(character, "inventory"):
        for item in character.inventory.items:
            if hasattr(item, "intimidation"):
                weapon_bonus = max(weapon_bonus, item.intimidation)  # Take scariest item

    # Final intimidation score
    intimidation_score = attribute_score + criminal_modifier + weapon_bonus + wildcard_bonus

    # Optionally clamp to 1–100 for balance
    return max(1, min(intimidation_score, 100))

def calculate_resistance_score(character, wildcard_bonus=0):
    """
    Calculates how resistant a character is to intimidation or coercion.
    Includes morale, loyalty, mental toughness, etc.
    Returns an integer between 1 and 100.
    """

    # Core attributes: intelligence and toughness are key to resisting
    core_attributes = [
        character.get_attribute("intelligence"),
        character.get_attribute("toughness"),
    ]
    base_resistance = sum(core_attributes) / len(core_attributes)

    # Loyalty factor: assumes loyalty is a quantized integer 0–10
    loyalty_value = 0
    if hasattr(character, "loyalty"):
        loyalty_value = int(character.loyalty.get_overall_loyalty())  # or .value if it's a property

    # Morale: optional — for now, default to 5 if not tracked
    morale = getattr(character, "morale", 5)

    # Add up resistance score
    resistance_score = base_resistance + loyalty_value + morale + wildcard_bonus

    # Clamp result
    return max(1, min(resistance_score, 100))


def attack_function(character):
    print(f"{character.name} attacks!")

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
        if weapon and weapon["isArmed"]: #isArmed does not appear ubiquitous
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

def defend_function():
     pass

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

def CombatEvent():
    pass
    #When a combat begins, an event is triggered
    #When a combat is over, and aftermath event is triggered

def combatAftermath():
    pass
    #this event might atract medics, news crews, crowds and lawyers

#this table for compatibilty with characterActions.py 
combat_actions = {
    "Attack": attack_function,
    "Defend": defend_function
}