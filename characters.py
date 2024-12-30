#characters.py
import random
from enum import Enum, auto
from inventory import Inventory
from common import Status
from InWorldObjects import ObjectInWorld, Wallet


class Character:

    # Declared at the class level rather than in init bc it is shared by all
    # instances of the class. Saves memory - not redefined every time you instantiate
    # Defining it as a class attribute communicates that this is a property of the class, not a mutable property of individual objects.
    VALID_SEXES = ("male", "female")  # Class-level constant
    VALID_RACES = ("Terran", "Martian")  # Class-level constant

    # Instance attributes
    def __init__(
        self,
        name,
        char_role,
        entity_id,
        faction=None,
        strength=10,
        agility=10,
        intelligence=10,
        luck=10,
        psy=10,
        toughness=10,
        morale=10,
        race="Terran",
        sex="male",
        status=None,
        loyalty=0,
        cash=0,
        bank_card_cash=0,
        fun=0,
        hunger=0,
        **kwargs,
    ):
        # Your initialization code
        self.current_location = None  # Tracks the character's location
        self.shift = 'day'  # Can be 'day' or 'night'
        self.is_working = False  # Tracks if the character is working
        self.name = name
        self.char_role = "default_role"
        self.faction = faction
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.luck = luck
        self.psy = psy
        self.toughness = toughness
        self.morale = morale
        self.race = race
        self.sex = sex
        self.entity_id = None
        self.status = status  # Add status here
        self.motivations = kwargs.get(
            "motivations", []
        )  # Use kwargs safely to add extra attributes
        # validation
        if sex not in self.VALID_SEXES:
            raise ValueError(
                f"Invalid sex: {sex}. Valid options are {self.VALID_SEXES}"
            )
        # variables to begin with lowercase letter, unlike Classes
        if race not in self.VALID_RACES:
            raise ValueError(
                f"Invalid race: {race}. Valid options are {self.VALID_RACES}"
            )

        self.faction = faction
        self.weapon = None
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.toughness = toughness
        self.morale = morale
        self.health = 100 + toughness
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.isArmored = False  # characters must aquire armor
        self.armorValue = 0

        self.wallet = Wallet(cash=50, bank_card_cash=100)  # Initialize with some default values
        self.inventory = []   # List to store items in the character's inventory
        

        self.char_role = char_role
        self.entity_id = entity_id
        self.status = status  # LOW, MID, HIGH, ELITE
        self.loyalty = kwargs.get("loyalty", 100)  # Out of 100
        self.inventory = kwargs.get("inventory", [])

    def __repr__(self):
        return f"{self.name} ({self.char_role}, {self.faction})"

    def get_total_money(self):
        """Return the total money available (cash + bank card)."""
        return self.wallet.total_balance()


    def calculate_item_cost(self, item):
        """
        Determine the cost of an item based on its legality.
        """
        if not hasattr(item, "legality"):
            raise ValueError("The item must have a 'legality' attribute.")
        return item.value if item.legality == True else item.blackmarket_value



    def buy(self, item, use_bank_card=False):
        amount = self.calculate_item_cost(item)

        # Check legality, which is now a boolean (True/False)
        if item.legality is True:
            self.make_normal_purchase(amount, use_bank_card)
        elif item.legality is False:
            self.make_black_market_purchase(amount)
        else:
            raise ValueError(f"Unknown legality type: {item.legality}")







    def make_black_market_purchase(self, amount):
        """Make a purchase on the black market (only cash can be used)."""
        if self.wallet.spend_cash(amount):
            print(f"Black market purchase of {amount} successful.")
        else:
            print(f"Not enough cash for black market purchase.")

    def make_normal_purchase(self, amount, use_bank_card=False):
        """Make a normal purchase, either using cash or bank card."""
        if use_bank_card:
            if self.wallet.spend_bank_card_cash(amount):
                print(f"Purchase of {amount} using bank card successful.")
            else:
                print(f"Not enough bank card balance for purchase.")
        else:
            if self.wallet.spend_cash(amount):
                print(f"Purchase of {amount} using cash successful.")
            else:
                print(f"Not enough cash for purchase.")

    def pick_up_cashwad(self, cashwad):
        """Pick up a CashWad and add the value to the wallet."""
        print(f"Picked up a CashWad worth {cashwad.get_value()} cash.")
        cashwad.add_to_wallet(self.wallet)

    def print_wallet(self):
        """Print the wallet's current balance (for debugging purposes)."""
        print(f"Cash in wallet: {self.wallet.cash}")
        print(f"Bank card balance: {self.wallet.bank_card_cash}")



# Specialized Roles
class Boss(Character):
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, char_role="Boss", faction=faction, status=Status.ELITE, **kwargs
        )
        self.directives = []  # High-level orders issued to Captains/Managers

    def issue_directive(self, directive):
        print(f"{self.name} issues directive: {directive}")
        self.directives = []  # List of high-level directives


class CEO(Character):
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, char_role="CEO", faction=faction, status=Status.ELITE, **kwargs
        )
        self.directives = []  # List of high-level directives

    def issue_directive(self, directive):
        print(f"{self.name} (CEO) issues directive: {directive}")
        self.directives.append(directive)


class Leader(Character):
    # Base class for manager and captain
    def __init__(self, name, faction, **kwargs):
        super().__init__(name, faction=faction, **kwargs)  # Don't pass char_role
        self.task_list = []

    def add_task(self, task):
        print(f"{self.name} adds task: '{task}' to their task list.")
        self.task_list.append(task)

    def delegate_task(self, task, subordinates):
        # Convert task names to lowercase for case-insensitive matching
        # Use task.lower() to make the incoming task name lowercase.

        task_lower = task.lower()
        task_list_lower = [t.lower() for t in self.task_list]

        if task_lower not in task_list_lower:
            print(
                f"{self.name} cannot delegate task '{task}' because it's not in their task list."
            )
            return

        # Find the actual task name to remove from the task list
        task_actual = next(t for t in self.task_list if t.lower() == task_lower)

        for subordinate in subordinates:
            print(f"{self.name} delegates task '{task_actual}' to {subordinate.name}")
            subordinate.receive_task(task_actual)

        self.task_list.remove(task_actual)
        print(
            f"Task '{task_actual}' has been delegated amd removed from the task list."
        )


class Captain(Leader):
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, faction=faction, char_role="Captain", status=Status.HIGH, **kwargs
        )


class Manager(Leader):
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, faction=faction, char_role="Manager", status=Status.HIGH, **kwargs
        )


class Subordinate(Character):
    def __init__(self, name, faction, **kwargs):
        super().__init__(name, faction=faction, **kwargs)
        self.tasks = []

    def receive_task(self, task):
        self.tasks.append(task)
        print(f"{self.name} is now handling task: '{task}'.")


class Employee(Subordinate):
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, char_role="Employee", faction=faction, status=Status.LOW, **kwargs
        )


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

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"{self.name} equipped {weapon.name}")

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

    def can_perform_action(self, action_type):
        """
        Checks if an action is allowed based on the current behaviour.
        :param action_type: Action to check.
        :return: True if the action is allowed, False otherwise.
        """
        return action_type in self.allowed_actions.get(self.behaviour_type, [])

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


def show_inventory(self):
    # Delegate to the inventory instance
    print(f"{self.name}'s inventory:")
    self.inventory.display_items()


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

# characters.py

def list_existing_characters(character_registry):
    """Display a list of existing characters and their entity IDs."""
    if not character_registry:
        print("No existing characters.")
        return None
    
    for character in character_registry:
        print(f"Character ID: {character.entity_id}, Name: {character.name}")
    
    return character_registry


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


class CorporateSecurity(Character):
    # A character that may or may not be aggressive
    def __init__(self, name):
        super().__init__(
            name,
            "CorporateSecurity",
            strength=15,
            agility=10,
            intelligence=5,
            luck=0,
            psy=0,
            toughness=5,
            morale=5,
            race="human",
        )

        self.behaviour.change_behaviour("aggressive")  # Set default behaviour
        self.weapons = {
            "pistol": {"isArmed": True, "ammo": 30},
            "tazer": {"isArmed": True, "tazerCharge": 10},
        }

        self.pistolIsLoaded = True
        self.pistolCurrentAmmo = 15
        self.tazerCharge = 10
        self.targetIsInMelee = False
        self.cash = 10
        self.bankCardCash = 100


class CorporateAssasin(CorporateSecurity):
    # A character that may or may not be aggressive
    def __init__(self, name):
        super().__init__(
            name,
            "CorporateAssasin",
            strength=12,
            agility=13,
            intelligence=10,
            luck=0,
            psy=0,
            toughness=5,
            morale=5,
            race="human",
        )

        self.behaviour.change_behaviour("murderous")  # default behaviour

        self.weapons = {
            "rifle": {"isArmed": True, "ammo": 30},
            "pistol": {"isArmed": True, "ammo": 30},
            "dagger": {"isArmedWithDagger": True, "isBlooded": False},
        }

        self.rifleIsLoaded = True
        self.rifleCurrentAmmo = 15
        self.pistolIsLoaded = True
        self.pistolCurrentAmmo = 15
        self.targetIsInMelee = False
        self.cash = 400
        self.bankCardCash = 1000
        self.health = 120 + toughness


class GangMember(Character):
    # A charactrer that may or may not be aggressive
    def __init__(self, name):
        super().__init__(
            name,
            "GangMember",
            strength=12,
            agility=13,
            intelligence=5,
            luck=0,
            psy=0,
            toughness=8,
            morale=3,
            race="human",
        )

        self.behaviour.change_behaviour("stealth")  # default behaviour

        self.weapons = {
            "pistol": {"isArmed": False, "ammo": 0},
            "tazer": {"isArmed": False, "tazerCharge": 0},
            "dagger": {"isArmedWithDagger": True, "isBlooded": False},
            "electroBaton": {"isArmed": False, "electroBatonCharge": 0},
        }

        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.targetIsInMelee = False
        self.gangMembership = Blue
        self.isAggressive = False
        self.cash = 50
        self.bankCardCash = 20


class RiotCop(Character):
    # An aggressive, armored character who attacks, initially, with a melee weapon
    def __init__(self, name):
        super().__init__(
            name,
            "RiotCop",
            strength=15,
            agility=4,
            intelligence=5,
            luck=0,
            psy=0,
            toughness=8,
            morale=8,
            race="human",
        )

        self.behaviour.change_behaviour("aggressive")  # default behaviour

        self.weapons = {
            "pistol": {"isArmed": False, "ammo": 0},
            "tazer": {"isArmed": False, "tazerCharge": 0},
            "electroBaton": {"isArmed": True, "electroBatonCharge": 30},
        }

        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.targetIsInMelee = False
        self.isAggressive = True
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.isArmored = True
        self.armorValue = 30
        self.cash = 50
        self.bankCardCash = 300


class Civilian(Character):
    # A character that may or may not be aggressive
    def __init__(self, name):
        super().__init__(
            name,
            "Civilian",
            strength=12,
            agility=10,
            intelligence=10,
            luck=0,
            psy=0,
            toughness=3,
            morale=2,
            race="human",
        )

        self.behaviour.change_behaviour("passive")  # default behaviour

        self.weapons = {
            "pistol": {"isArmed": False, "ammo": 0},
            "dagger": {"isArmedWithDagger": False, "isBlooded": False},
        }

        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.cash = 50
        self.bankCardCash = 50


class VIP(Civilian):
    # A character that may or may not be aggressive
    def __init__(self, name):
        super().__init__(
            name,
            "VIP",
            strength=18,
            agility=10,
            intelligence=15,
            luck=0,
            psy=0,
            toughness=5,
            morale=7,
            race="human",
        )

        self.behaviour.change_behaviour("passive")  # default behaviour

        self.weapons = {
            "pistol": {"isArmed": False, "ammo": 0},
            "tazer": {"isArmed": False, "tazerCharge": 0},
        }

        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.tazerCharge = 0
        self.cash = 50
        self.bankCardCash = 10000
        self.health = 120 + toughness

def create_character_if_needed(entity_id, character_registry):
    """Create or fetch a character based on entity ID."""
    if entity_id is None:
        entity_id = generate_entity_id()

    if entity_id not in character_registry:
        print(f"Creating a new character with ID {entity_id}...")
        chosen_role = select_role(
            ["Grunt", "Captain", "Boss", "Manager", "Employee", "CEO"]
        )
        character = Character(
            name=f"Character {entity_id}", entity_id=entity_id, char_role=chosen_role
        )
        character_registry[entity_id] = character
        print(f"Character created with role: {chosen_role}")
    else:
        print(f"Entity ID {entity_id} already exists.")
        character = character_registry[entity_id]

    # Debugging the registry update

    def debug_character(char):
        print(f"DEBUG: {char.name} - Money: {char.wallet}, Fun: {char.fun}, Hunger: {char.hunger}")

        print(f"Updated Character Registry: {character_registry}")  # <-- Add this
    return character
