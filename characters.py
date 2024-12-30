#characters.py
import random
from enum import Enum, auto
from inventory import Inventory
from common import Status
from InWorldObjects import ObjectInWorld, Wallet

#There are repeated assignments (e.g., self.pistolIsLoaded in
#  RiotCop) and unused parameters (e.g., **kwargs in some 
# subclasses). Reviewing and cleaning these up would enhance 
# clarity.
class Character:

    VALID_SEXES = ("male", "female")  # Class-level constant
    VALID_RACES = ("Terran", "Martian")  # Class-level constant
    
    #common attributes (e.g., name, age, health) remain in the base class
    is_concrete = False
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
        self.wallet = Wallet(cash=50, bank_card_cash=100)  # Initialize with some default values
        self.inventory = []   # List to store items in the character's inventory
        self.char_role = char_role
        self.entity_id = entity_id
        self.status = status  # LOW, MID, HIGH, ELITE
        self.loyalty = kwargs.get("loyalty", 100)  # Out of 100
        self.inventory = kwargs.get("inventory", [])

    def __repr__(self):
        return f"{self.name} ({self.char_role}, {self.faction})"


#Method overriding is used sparingly (e.g., issue_directive in 
# Boss and CEO). Consider leveraging polymorphism more to reduce 
# role-specific conditionals.
class Boss(Character):
    is_concrete = True
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

class Captain(SubLeader):
    is_concrete = True
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, faction=faction, char_role="Captain", status=Status.HIGH, **kwargs
        )

class Manager(SubLeader):
    is_concrete = True
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, faction=faction, char_role="Manager", status=Status.HIGH, **kwargs
        )

class Subordinate(Character):
    is_concrete = False
    def __init__(self, name, faction, **kwargs):
        super().__init__(name, faction=faction, **kwargs)
        self.tasks = []

class Employee(Subordinate):
    is_concrete = True
    def __init__(self, name, faction, **kwargs):
        super().__init__(
            name, char_role="Employee", faction=faction, status=Status.LOW, **kwargs
        )

#A lot of logic removed with Class Grunt, see deprecated folder

#There are repeated assignments (e.g., self.pistolIsLoaded in
#  RiotCop) and unused parameters (e.g., **kwargs in some
#  subclasses). Reviewing and cleaning these up would enhance
#  clarity.


class CorporateSecurity(Subordinate):
    is_concrete = True
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

        self.pistolIsLoaded = True
        self.pistolCurrentAmmo = 15
        self.tazerCharge = 10
        self.targetIsInMelee = False
        self.cash = 10
        self.bankCardCash = 100


class CorporateAssasin(CorporateSecurity):
    is_concrete = True
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

        self.rifleIsLoaded = True
        self.rifleCurrentAmmo = 15
        self.pistolIsLoaded = True
        self.pistolCurrentAmmo = 15
        self.targetIsInMelee = False
        self.cash = 400
        self.bankCardCash = 1000
        self.health = 120 + toughness


class GangMember(Subordinate):
    is_concrete = True
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

        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.targetIsInMelee = False
        self.gangMembership = Blue
        self.isAggressive = False
        self.cash = 50
        self.bankCardCash = 20


class RiotCop(Character): #Subordintate? Of the state?
    is_concrete = True
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
    is_concrete = True
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

        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.cash = 50
        self.bankCardCash = 50


class VIP(Civilian):
    is_concrete = True
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
