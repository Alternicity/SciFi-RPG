#characters.py
import random
from enum import Enum, auto
from inventory import Inventory
from status import Status
from InWorldObjects import ObjectInWorld, Wallet

from base_classes import Character, Location, Faction


#Method overriding is used sparingly (e.g., issue_directive in 
# Boss and CEO). Consider leveraging polymorphism more to reduce 
# role-specific conditionals.
class Boss(Character):
    is_concrete = True
    def __init__(self, name, faction, position="A Boss", loyalties=None, **kwargs):
        
        # Default loyalty setup for Boss
        default_loyalties = {
            faction: 100,  # Full loyalty to their own faction
            "Law": 10,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        super().__init__(
            name, faction=faction, status="ELITE", loyalties=default_loyalties, **kwargs
        )
        self.directives = []  # High-level orders issued to Captains/Managers
        
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        
        def __repr__(self):
            # Use Character's consistent representation and add faction info
            return super().__repr__() + f", Faction: {self.faction}"


    def issue_directive(self, directive):
        print(f"{self.name} issues directive: {directive}")
        self.directives = []  # List of high-level directives

class CEO(Character):
    def __init__(self, name, faction, position="A CEO", loyalties=None, **kwargs):
        
        # Default loyalty setup for CEO
        default_loyalties = {
            faction: 100,  # Full loyalty to their own faction
            "Law": 40,  # Disdain of the law, unless its useful 
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        # Extract inventory safely from kwargs
        inventory = kwargs.pop("inventory", [])

        # Ensure required attributes are explicitly passed to Character
        super().__init__(
            name, faction=faction, status="ELITE", loyalties=default_loyalties, **kwargs # Pass remaining keyword arguments safely
        )
        self.directives = []  # List of high-level directives
        self.inventory = inventory
        
        def __repr__(self):
            """Ensure correct string representation"""
        return f"{super().__repr__()}, Faction: {self.faction}"

    def issue_directive(self, directive):
        print(f"{self.name} (CEO) issues directive: {directive}")
        self.directives.append(directive)

class Captain(Character):
    is_concrete = True
    def __init__(self, name, faction, position="A Captain", loyalties=None, **kwargs):
        
        # Default loyalty setup for Captain
        default_loyalties = {
            faction: 60,  #loyalty to their own faction
            "Law": 10,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name, faction=faction, status=Status.HIGH, loyalties=default_loyalties, **kwargs
        )
        
        # Ensure inventory is a new list instance per character
        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []

    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"

class Manager(Character):
    is_concrete = True
    def __init__(self, name, faction="None", bankCardCash=500, position="Manager", loyalties=None, fun=1, hunger=1, **kwargs):
        
        # Default loyalty setup for Manager
        default_loyalties = {
            faction: 50 if faction else 0,  # Avoid issues if faction is None
            "Law": 40,
        }
        # Merge defaults with provided loyalties safely
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name, faction=faction, bankCardCash=bankCardCash, status=Status.HIGH, loyalties=default_loyalties, fun=fun,
            hunger=hunger, **kwargs
        )
        self.position = position
        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []

    def __repr__(self):
            # Use Character's consistent representation and add faction info
            return super().__repr__() + f", Faction: {self.faction}"
    
class Subordinate(Character):
    is_concrete = False
    def __init__(self, name, faction, strength, agility, intelligence, luck, psy, toughness, morale, race, position="A subordinate", loyalties=None, **kwargs):
        default_loyalties = {
            faction: 20 if faction else 0,  # Avoid issues if faction is None
            "Law": 20,  # Meh, whatever
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})

        super().__init__(name, faction=faction,  strength=strength, agility=agility, intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, morale=morale, race=race, loyalties=default_loyalties, **kwargs)
        self.tasks = []# Explicitly initialize task list

        # Ensure inventory is correctly initialized
        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []
        

class Employee(Subordinate):
    is_concrete = True
    def __init__(self, name, faction,  strength=9, agility=8, intelligence=8, luck=9, psy=1, toughness=7, morale=5, race="Terran", position="An employee", loyalties=None, **kwargs):
        
        # Default loyalty setup for Employee
        default_loyalties = {
            faction: 15 if faction else 0,  # Avoid issues if faction is None
            "Law": 15,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name, faction=faction, strength=strength, agility=agility, intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, morale=morale, race=race, position=position, status=Status.LOW, loyalties=default_loyalties, **kwargs
        )
        
        # Ensure inventory is correctly initialized
        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []
        
    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"

class CorporateSecurity(Subordinate):
    is_concrete = True
    def __init__(self, name, faction, strength=12, agility =10, intelligence=8, luck=9, psy=1, toughness=13, morale=11, race="Terran", position="Security Guard", loyalties=None, **kwargs):
        
        # Default loyalty setup for CorporateSecurity
        default_loyalties = {
            faction: 50 if faction else 0,  # Avoid issues if faction is None
            "Law": 10,  # Not cops, just security
        }
        # Merge defaults with provided loyalties safely
        default_loyalties.update(loyalties or {})

        super().__init__(
            name, faction=faction, strength=strength, agility=agility, 
            intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, 
            morale=morale, race=race, position=position, 
            loyalties=default_loyalties, **kwargs
        )
        
        self.pistolIsLoaded = True
        self.pistolCurrentAmmo = 15
        self.tazerCharge = 10
        self.targetIsInMelee = False
        self.cash = 10
        self.bankCardCash = 100

        # Ensure inventory is correctly initialized
        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []
        
    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"

class CorporateAssasin(CorporateSecurity):
    is_concrete = True
    def __init__(self, name, faction,  strength=12, agility=15, intelligence=15, toughness=13, morale=13, race="Terran", position="Unknown", loyalties=None, **kwargs):
        
        # Default loyalty setup for CorporateAssasin
        default_loyalties = {
            faction: 10 if faction else 0,  # Avoid issues if faction is None
            "Law": 0,  # No trust in the law
        }
        # Merge defaults with provided loyalties safely
        default_loyalties.update(loyalties or {})

        super().__init__(
            name, faction=faction, strength=strength, agility=agility, 
            intelligence=intelligence, luck=0, psy=0, toughness=toughness, 
            morale=morale, race=race, position=position, 
            loyalties=default_loyalties, **kwargs
        )
        
        # Assassin-specific weapon attributes
        self.rifleIsLoaded = True
        self.rifleCurrentAmmo = 15

        # Override base class financial stats
        self.cash = 400
        self.bankCardCash = 1000

        # Adjusted health based on toughness
        self.health = 120 + toughness

        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []  # List to store items in the character's inventory

    def __repr__(self):
        """Ensures a consistent representation and includes faction information."""
        return super().__repr__() + f", Position: {self.position}, Health: {self.health}"

class GangMember(Subordinate):
    is_concrete = True
    def __init__(self, name, faction, strength=12, agility=11, intelligence=7, 
                 luck=9, psy=2, toughness=14, morale=12, race="Terran", 
                 position="Gangster", loyalties=None, **kwargs):
    # Default loyalty setup for GangMember
        default_loyalties = {
            faction: 15 if faction else 0,  # Ensure faction exists
            "Law": 0,  # No trust in law enforcement
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})   
        
        super().__init__(
            name, faction=faction, strength=strength, agility=agility, 
            intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, 
            morale=morale, race=race, position=position, 
            loyalties=default_loyalties, **kwargs
        )
        
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.targetIsInMelee = False
        self.isAggressive = False

        self.cash = 50
        self.bankCardCash = 20

        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []
        
    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"

class RiotCop(Character):
    is_concrete = True
    def __init__(self, name, start_region, faction="The State", 
                 position="Pig", toughness=14, loyalties=None, fun=0, hunger=0, **kwargs):
        
        # Find a PoliceStation in the region
        from location import PoliceStation
        police_stations = [loc for loc in start_region.locations if isinstance(loc, PoliceStation)]
        start_location = police_stations[0] if police_stations else None  # Pick first available or None

    # Default loyalty setup for RiotCop
        default_loyalties = {
            faction: 80,  # High loyalty to their own faction
            "Law": 70,  # Law-abiding mindset
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})   
        
        super().__init__(
            name, start_region, start_location, faction=faction,
            fun=fun, hunger=hunger, strength=15, agility=4, intelligence=5, 
            luck=0, psy=0, toughness=toughness, morale=8, race="Terran", 
            loyalties=default_loyalties, position=position, **kwargs
        )
        
        # Weapon & Combat Attributes
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.targetIsInMelee = False
        self.isAggressive = True
        self.targetIsInMelee = False

        # Armor & Finances
        
        self.isArmored = True
        self.armorValue = 30
        self.cash = 50
        self.bankCardCash = 300

        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []  # List to store items in the character's inventory

    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"

class Civilian(Character):
    is_concrete = True
    def __init__(self, name, start_location, strength=12, agility=10, intelligence=10, luck=0, psy=0, toughness=3, morale=2, position="Normie", race="Terran", loyalties=None, **kwargs):
    

   # Default loyalty setup for Civilian
        default_loyalties = {
            "Law": 45,  # Neutral stance on law
        }
        # Merge defaults with provided loyalties if given
        loyalties = kwargs.pop("loyalties", None)  # Extract if present
        if loyalties:
            default_loyalties.update(loyalties)

        kwargs["loyalties"] = default_loyalties  # Inject updated loyalties
        kwargs.setdefault("faction", Faction)  # Avoids multiple faction values issue

        super().__init__(
            name, start_location=start_location, strength=strength, agility=agility, intelligence=intelligence, 
            luck=luck, psy=psy, toughness=toughness, morale=morale, position=position, race=race, 
            **kwargs
        )

        # Weapon & Combat Attributes
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False

        self.cash = 50
        self.bankCardCash = 50
        # Inventory Initialization
        self.inventory = kwargs.get("inventory", [])
    
    def __repr__(self):
        """Ensures a consistent representation and includes faction and position."""
        return super().__repr__() + f", Position: {self.position}, Faction: {self.faction}"

class VIP(Civilian):
    is_concrete = True
    def __init__(self, name, start_location, start_region, bankCardCash=10000, position="Mayor", loyalties=None,
        influence=0, strength=18, agility=10, intelligence=15, 
        luck=0, psy=0, toughness=5, morale=7, race="Terran", fun=0, hunger=0, **kwargs):
        kwargs.setdefault("faction", "The State")  # Set default only if not provided

        # Find a MunicipalBuilding in the region
        from location import MunicipalBuilding
        municipal_buildings = [loc for loc in start_region.locations if isinstance(loc, MunicipalBuilding)]
        start_location = municipal_buildings[0] if municipal_buildings else None  # Pick first available or None


        # Default loyalty setup for VIP
        default_loyalties = {
            Faction: 90,  # loyalty to their own faction
            "Law": 75,  # I have a nice life, so, yeah
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)

        # Ensure `loyalties` is properly passed
        kwargs["loyalties"] = default_loyalties
        
        # Pass correct arguments to `Civilian.__init__()`
        super().__init__(
            name,
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            psy=psy,
            toughness=toughness,
            morale=morale,
            start_location=start_location,
            start_region=start_region,
            position=position,  # Ensure position is passed correctly
            race=race,
            **kwargs # faction is already in kwargs
        )
        
        self.influence = influence
        self.targetIsInMelee = False
        self.cash = 500
        self.bankCardCash = bankCardCash  # Redundant but ensures it's explicitly set for VIP
        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        self.position = position
        self.start_region = start_region  # Keep track of initial region
        self.start_location = start_location  # Keep track of starting building


    def __repr__(self):
        return super().__repr__() + f", Position: {self.position}, Faction: {self.faction}"

    
class Child(Civilian):
    is_concrete = True
    def __init__(self, name, faction="None", parent=None, bankCardCash=0, position="Minor", loyalties=None,
        influence=0, strength=3, agility=10, intelligence=5, 
        luck=0, psy=0, toughness=5, morale=1, race="Terran", fun=2, hunger=2, **kwargs):
        
        # Default loyalty setup for Child
        default_loyalties = {
            parent: 90,  # loyalty to their own faction
            "Law": 30,  # Don't steal!
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name,
            faction=faction,
            fun=fun,
            hunger=hunger,
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
            bankCardCash=bankCardCash,
            **kwargs
        )
        
        self.parent = parent if isinstance(parent, Character) and parent.race == race else None
        self.race = race
        self.influence = influence
        self.targetIsInMelee = False
        self.cash = 500
        self.bankCardCash = bankCardCash  
        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        self.position = position

    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"

    def update_parent(self, new_parent):
        """
        Updates the parent attribute.

        :param new_parent: A new parent (Character object) or None.
        """
        if new_parent is None or (isinstance(new_parent, Character) and new_parent.race == self.race):
            self.parent = new_parent
        else:
            raise ValueError("New parent must be a Character of the same race or None.")

    def orphan(self):
        """Sets the parent attribute to 'Orphan'."""
        self.parent = "Orphan"


class Influencer(Civilian):
    is_concrete = True
    def __init__(self, name, faction="None", bankCardCash=1000, position="Grifter", loyalties=None,
        influence=8, strength=10, agility=10, intelligence=15, 
        luck=0, psy=0, toughness=5, morale=2, race="Terran", fun=2, hunger=0, **kwargs):
        
        # Default loyalty setup for Influencer
        default_loyalties = {
            faction: 10,  # loyalty to their own faction, if any
            "Law": 15,  # Just, whatever
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name,
            faction=faction,
            fun=fun,
            hunger=hunger,
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
            bankCardCash=bankCardCash,
            **kwargs
        )
        
        self.influence = influence
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.tazerCharge = 0
        self.cash = 1000
        self.bankCardCash = bankCardCash  
        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        self.position = position

    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"
        
class Babe(Civilian):
    is_concrete = True
    def __init__(self, name, faction="None", partner=None, bankCardCash=1000, position="Variously Attached", loyalties=None,
        influence=7, strength=7, agility=10, intelligence=10, 
        luck=0, psy=0, charisma=14, toughness=4, morale=0, race="Terran", fun=2, hunger=2, **kwargs):
        
        # Default loyalty setup for Babe
        default_loyalties = {
            partner: 4,  # loyalty if you can call it that
            "Law": 15,  # Just, whatever
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name,
            faction=faction,
            fun=fun,
            partner=partner,
            hunger=hunger,
            position=position,  # Ensure position is passed correctly
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            psy=psy,
            charisma=charisma,
            toughness=toughness,
            morale=morale,
            race=race,
            loyalties=default_loyalties,
            bankCardCash=bankCardCash,
            **kwargs
        )
        
        self.influence = influence
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.targetIsInMelee = False
        self.tazerCharge = 0
        self.cash = 1000
        self.bankCardCash = bankCardCash  
        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
        self.position = position
        self.partner = Character

    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"
    
    def influence(self, target):
    #TMP
        from characterActions import influence
        return influence(self, target)

    def flirt(self, target):
        """Calls the generic flirt action."""
        from characterActions import flirt
        return flirt(self, target)

    def charm(self, target):
        """Calls the generic charm action."""
        from characterActions import charm
        return charm(self, target)

    def dump(self):
        """Ends the relationship."""
        self.remove_partner()
        print(f"{self.name} has dumped their partner.")

class Detective(Character): #Subordinate? Of the state?
    is_concrete = True
    def __init__(self, name, start_region, faction="The State", bankCardCash=800, position="Cop", toughness=13, loyalties=None, fun=0, hunger=0, **kwargs):

    # Find a PoliceStation in the region
        from location import PoliceStation
        police_stations = [loc for loc in start_region.locations if isinstance(loc, PoliceStation)]
        start_location = police_stations[0] if police_stations else None  # Pick first available or None

    # Default loyalty setup for Detective
        default_loyalties = {
            faction: 80,  # loyalty to their own faction
            "Law": 90,  # It's the law, no on should be above it
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})   
        
        super().__init__(
            name,
            start_region,
            start_location,
            faction=faction,
            fun=fun,
            hunger=hunger,
            strength=15,
            agility=4,
            intelligence=5,
            luck=0,
            psy=0,
            toughness=toughness,
            morale=8,
            race="Terran",
            loyalties=default_loyalties,
            **kwargs
        )
        
        # Weapon & Combat Attributes
        self.pistolIsLoaded = False
        self.pistolCurrentAmmo = 0
        self.tazerCharge = 0
        self.targetIsInMelee = False
        self.isAggressive = True
        self.targetIsInMelee = False

        # Armor & Finances
        
        self.isArmored = True
        self.armorValue = 30
        self.cash = 50
        self.bankCardCash = 300

        self.inventory = kwargs.get("inventory", []) if "inventory" in kwargs else []  # List to store items in the character's inventory


    def __repr__(self):
        # Use Character's consistent representation and add faction info
        return super().__repr__() + f", Faction: {self.faction}"   
        
class Taxman(Character):
    is_concrete = True
    def __init__(self, name, faction="State", bankCardCash=1000, position="Tax Official", loyalties=None, fun=-1, hunger=0, **kwargs):
        
        # Default loyalty setup for Manager
        default_loyalties = {
            faction: 50,  # Somewhat loyal to faction
            "Law": 40,
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name, faction=faction, bankCardCash=bankCardCash, status=Status.HIGH, loyalties=default_loyalties, fun=fun,
            hunger=hunger, **kwargs
        )
        self.position = position
        self.bankCardCash = bankCardCash
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
    
    # figure out how specific charcters store their specific actions, here or in that file or both

    def __repr__(self):
            # Use Character's consistent representation and add faction info
            return super().__repr__() + f", Faction: {self.faction}"
    
class Accountant(Character):
    is_concrete = True
    def __init__(self, name, faction="None", bankCardCash=1000, position="Accountant", loyalties=None, fun=0, hunger=0, **kwargs):
        
        # Default loyalty setup for Manager
        default_loyalties = {
            faction: 70,  # Somewhat loyal to faction
            "Law": 20,
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        super().__init__(
            name, faction=faction, bankCardCash=bankCardCash, status=Status.HIGH, loyalties=default_loyalties, fun=fun,
            hunger=hunger, **kwargs
        )
        self.position = position
        self.bankCardCash = bankCardCash
        self.inventory = kwargs.get("inventory", [])  # List to store items in the character's inventory
    

    def __repr__(self):
            # Use Character's consistent representation and add faction info
            return super().__repr__() + f", Faction: {self.faction}"