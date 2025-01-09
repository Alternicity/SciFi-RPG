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
        entity_id,
        char_role="Civilian",
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
        loyalties=None,  # Default is None; initializes as a dictionary later        cash=0,
        bank_card_cash=0,
        fun=0,
        hunger=0,
        **kwargs,
    ):
        
        # Generate entity_id if not provided
        entity_id = entity_id or f"{char_role.upper()}-{hash(name)}"

        #initialization code
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
        self.entity_id = entity_id or f"{char_role.upper()}-{hash(name)}"
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
        # Validate that faction is provided
        if not self.faction:
            raise ValueError("Faction must be specified for a character.")
        self.weapon = None
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.toughness = toughness
        self.morale = morale
        self.health = 100 + toughness
        self.wallet = Wallet(cash=50, bank_card_cash=100)  # Initialize with some default values
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory        self.char_role = char_role
        self.status = status  # LOW, MID, HIGH, ELITE
        self.inventory = kwargs.get("inventory", [])
        # Initialize loyalties as a dictionary
        self.loyalties = loyalties or {}
    def __repr__(self):
        return f"{self.name} ({self.char_role}, {self.faction})"
    def get_loyalty(self, group):
        """
        Get the loyalty level to a specific group. Returns 0 if the group is not in the dictionary.
        """
        return self.loyalties.get(group, 0)

    def update_loyalty(self, group, amount):
        """
        Update the loyalty to a specific group. If the group is not in the dictionary, add it.
        """
        self.loyalties[group] = self.loyalties.get(group, 0) + amount
        #if loyalty goes <0 a treachery event might be triggered

#Method overriding is used sparingly (e.g., issue_directive in 
# Boss and CEO). Consider leveraging polymorphism more to reduce 
# role-specific conditionals.
class Boss(Character):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Crime Boss", loyalties=None, **kwargs):
        
        # Default loyalty setup for Boss
        default_loyalties = {
            faction: 100,  # Full loyalty to their own faction
            "Law": 10,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(
            name, faction=faction, entity_id=entity_id, char_role=char_role, status="ELITE", loyalties=default_loyalties, **kwargs
        )
        self.directives = []  # High-level orders issued to Captains/Managers
        
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        


    def issue_directive(self, directive):
        print(f"{self.name} issues directive: {directive}")
        self.directives = []  # List of high-level directives

class CEO(Character):
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="CEO", loyalties=None, **kwargs):
        
        # Default loyalty setup for CEO
        default_loyalties = {
            faction: 100,  # Full loyalty to their own faction
            "Law": 40,  # Disdain of the law, unless its useful 
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(
            name, faction=faction, entity_id=entity_id, char_role="CEO", status=Status.ELITE, loyalties=default_loyalties, **kwargs
        )
        self.directives = []  # List of high-level directives
        
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

    def issue_directive(self, directive):
        print(f"{self.name} (CEO) issues directive: {directive}")
        self.directives.append(directive)

class Captain(Character):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Ganger", loyalties=None, **kwargs):
        
        # Default loyalty setup for Captain
        default_loyalties = {
            faction: 60,  #loyalty to their own faction
            "Law": 10,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(
            name, faction=faction, entity_id=entity_id, char_role="Captain", status=Status.HIGH, loyalties=default_loyalties, **kwargs
        )
        
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class Manager(Character):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Manager", loyalties=None, **kwargs):
        
        # Default loyalty setup for Manager
        default_loyalties = {
            faction: 50,  # Somewhat loyal to faction
            "Law": 40,
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(
            name, faction=faction, entity_id=entity_id, char_role="Manager", status=Status.HIGH, loyalties=default_loyalties, **kwargs
        )
        
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class Subordinate(Character):
    is_concrete = False
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Varies", loyalties=None, **kwargs):
        
        # Default loyalty setup for Subordinate
        default_loyalties = {
            faction: 20,
            "Law": 20,  # Meh, whatever
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(name, faction=faction, entity_id=entity_id, char_role=char_role, loyalties=default_loyalties, **kwargs)
        self.tasks = []
        
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class Employee(Subordinate):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Employee", loyalties=None, **kwargs):
        
        # Default loyalty setup for Employee
        default_loyalties = {
            faction: 15,
            "Law": 15,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(
            name, faction=faction, entity_id=entity_id, char_role="Employee", status=Status.LOW, loyalties=default_loyalties, **kwargs
        )
        
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class CorporateSecurity(Subordinate):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Security", loyalties=None, **kwargs):
        
        # Default loyalty setup for CorporateSecurity
        default_loyalties = {
            faction: 50,  # Full loyalty to their own faction
            "Law": 10,  # We are not cops
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)

        super().__init__(
            name,
            faction=faction,
            entity_id=entity_id, 
            char_role=char_role,
            strength=15,
            agility=10,
            intelligence=5,
            luck=0,
            psy=0,
            toughness=5,
            morale=5,
            race="Terran",
            loyalties=default_loyalties,
            **kwargs
        )
        
        self.pistolIsLoaded = True
        self.pistolCurrentAmmo = 15
        self.tazerCharge = 10
        self.targetIsInMelee = False
        self.cash = 10
        self.bankCardCash = 100
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class CorporateAssasin(CorporateSecurity):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Unknown", char_role="Assassin", loyalties=None, **kwargs):
        
        # Default loyalty setup for CorporateAssasin
        default_loyalties = {
            faction: 10,  # Where's the money?
            "Law": 0,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)

        super().__init__(
            name,
            faction=faction,
            entity_id=entity_id, 
            char_role=char_role,
            strength=12,
            agility=13,
            intelligence=10,
            luck=0,
            psy=0,
            toughness=5,
            morale=5,
            race="Terran",
            loyalties=default_loyalties,
            **kwargs
        )
        
        self.rifleIsLoaded = True
        self.rifleCurrentAmmo = 15
        self.pistolIsLoaded = True
        self.pistolCurrentAmmo = 15
        self.targetIsInMelee = False
        self.cash = 400
        self.bankCardCash = 1000
        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class GangMember(Subordinate):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Ganger", loyalties=None, **kwargs):

    # Default loyalty setup for GangMember
        default_loyalties = {
            faction: 15,  # loyalty to their own faction
            "Law": 0,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)   
        
        super().__init__(
            name,
            faction=faction,
            entity_id=entity_id, 
            char_role=char_role,
            strength=12,
            agility=13,
            intelligence=5,
            luck=0,
            psy=0,
            toughness=8,
            morale=3,
            race="Terran",
            loyalties=default_loyalties,
            **kwargs
        )
        
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.targetIsInMelee = False
        self.gangMembership = Blue
        self.isAggressive = False
        self.cash = 50
        self.bankCardCash = 20
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class RiotCop(Character): #Subordinate? Of the state?
    is_concrete = True
    def __init__(self, name, faction="The State", entity_id=None, position="Civilian", char_role="Cop", loyalties=None, **kwargs):

    # Default loyalty setup for RiotCop
        default_loyalties = {
            faction: 80,  # loyalty to their own faction
            "Law": 70,  # It's the law, and it pays me
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)   
        
        super().__init__(
            name,
            faction=faction,
            entity_id=entity_id, 
            char_role=char_role,
            strength=15,
            agility=4,
            intelligence=5,
            luck=0,
            psy=0,
            toughness=8,
            morale=8,
            race="Terran",
            loyalties=default_loyalties,
            **kwargs
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
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class Civilian(Character):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Civilian", char_role="Civilian", loyalties=None, strength=12, agility=10, intelligence=10, luck=0, psy=0, toughness=3, morale=2, race="Terran", **kwargs):

    # Default loyalty setup for Civilian
        default_loyalties = {
            faction: 0,  # no faction
            "Law": 45,  # We need someone to control the gangs
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)

        super().__init__(
            name,
            faction=faction,
            entity_id=entity_id, 
            char_role=char_role,
            position=position,  # Ensure position is passed to the Character constructor
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            psy=psy,
            toughness=toughness,
            morale=morale,
            race=race,
            loyalties=default_loyalties,
            **kwargs
        )
        
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.cash = 50
        self.bankCardCash = 50
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

class VIP(Civilian):
    is_concrete = True
    def __init__(self, name, faction, entity_id=None, position="Mayor", char_role="Civilian", loyalties=None,
        influence=0, strength=18, agility=10, intelligence=15, 
        luck=0, psy=0, toughness=5, morale=7, race="Terran", **kwargs):
        
        # Default loyalty setup for VIP
        default_loyalties = {
            faction: 90,  # loyalty to their own faction
            "Law": 75,  # I have a nice life, so, yeah
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(
            name,
            faction=faction,
            entity_id=entity_id, 
            char_role=char_role,
            position=position,  # Ensure position is passed correctly
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            psy=psy,
            toughness=toughness,
            morale=morale,
            race=race,
            loyalties=default_loyalties,
            **kwargs
        )
        
        self.influence = influence
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.tazerCharge = 0
        self.cash = 500
        self.bankCardCash = 10000
        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        

def create_character_if_needed(entity_id, character_registry):
    """Create or fetch a character based on entity ID."""
    if entity_id is None:
        entity_id = generate_entity_id()

    if entity_id not in character_registry:
        print(f"Creating a new character with ID {entity_id}...")
        chosen_role = select_role(
            ["Captain", "Boss", "Manager", "Employee", "CEO"]
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
