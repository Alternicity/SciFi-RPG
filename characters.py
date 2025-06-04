#characters.py
import random
from enum import Enum, auto
from inventory import Inventory
from status import StatusLevel, CharacterStatus, FactionStatus
from InWorldObjects import ObjectInWorld, Wallet
from wallet import generate_wallet
from base_classes import Character, Location, Faction
from ai_gang import GangMemberAI, GangCaptainAI, BossAI, gang_observation_logic

#Method overriding is used sparingly (e.g., issue_directive in 
# Boss and CEO). Consider leveraging polymorphism more to reduce 
# role-specific conditionals.
class Boss(Character):
    is_concrete = True
    default_motivations = [
        ("influence", 4),
        ("gain_elite", 6),
        ("decrease_hostilities", 4),
        ("sow_dissent", 4)
    ]

    def __init__(self, name, race, sex, region, location, faction, position="A Boss", loyalties=None, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()
        
        # Criminal domain — true identity
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.HIGH, position))

        # Placeholder domains — public perception
        status.set_status("public", FactionStatus(StatusLevel.MID, "Community Leader"))
        status.set_status("corporate", FactionStatus(StatusLevel.NONE, None))
        status.set_status("state", FactionStatus(StatusLevel.LOW, "Watched"))

        # Ensure primary domain is set correctly
        kwargs["primary_status_domain"] = "criminal"

        # Default loyalty setup for Boss
        default_loyalties = {
            faction: 100,  # Full loyalty to their own faction
            "Law": 10,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)

        wallet = kwargs.pop("wallet", generate_wallet("Boss"))
        super().__init__(
            name=name, race=race, sex=sex, faction=faction,  region=region,
            location=location,  status=status, wallet=wallet, loyalties=default_loyalties, motivations=motivations or self.default_motivations, **kwargs
        )
        self.directives = []  # High-level orders issued to Captains/Managers
        self.primary_status_domain = "criminal"
        self.inventory = kwargs.get("inventory", Inventory(owner=self))
  # List to store items in the character's inventory
        
    def handle_observation(self, region):
        gang_observation_logic(self, region)
    
    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
    def issue_directive(self, directive):
        print(f"{self.name} issues directive: {directive}")
        self.directives = []  # List of high-level directives

class CEO(Character):
    default_motivations = [
        ("earn_money", 5),
        ("gain_elite", 6),
        ("influence", 4),
        ("decrease_hostilities", 3)
    ]

    def __init__(self, name, race, sex, region, location, faction, position="A CEO", loyalties=None, status=None, motivations=None, **kwargs):
        

        # Default loyalty setup for CEO
        default_loyalties = {
            faction: 100,  # Full loyalty to their own faction
            "Law": 40,  # Disdain of the law, unless its useful 
        }
        # Merge defaults with provided loyalties
        if loyalties:
            default_loyalties.update(loyalties)
        
        # Initialize status if not provided
        if status is None:
            status = CharacterStatus()

        # Corporate domain — primary
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.HIGH, position))

        # Placeholder domains
        status.set_status("public", FactionStatus(StatusLevel.MID, "Entrepreneur"))
        status.set_status("criminal", FactionStatus(StatusLevel.LOW, "Suspicious"))
        status.set_status("state", FactionStatus(StatusLevel.MID, "Influential Lobbyist"))

        # Set primary status domain explicitly
        kwargs["primary_status_domain"] = "corporate"

        # Extract inventory safely from kwargs
        inventory = kwargs.pop("inventory", [])
        wallet = kwargs.pop("wallet", generate_wallet("CEO"))
        # Call parent constructor
        super().__init__(
            name=name, race=race, sex=sex, faction=faction, region=region,
            location=location, status=status, wallet=wallet, loyalties=default_loyalties, motivations=motivations or self.default_motivations, **kwargs # Pass remaining keyword arguments safely
        )
        self.directives = []  # List of high-level directives
        self.inventory = kwargs.get("inventory", Inventory(owner=self))

        
    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    def issue_directive(self, directive):
        print(f"{self.name} (CEO) issues directive: {directive}")
        self.directives.append(directive)
    
    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
class Captain(Character):
    is_concrete = True
    default_motivations = [
        ("follow_orders", 2),
        ("patrol", 3),
        ("gain_mid", 4),
        ("find_safety", 3)
    ]

    def __init__(self, name, race, sex, region, location, faction, position="Captain", loyalties=None, status=None, motivations=None, **kwargs):
        
        
        if status is None:
            status = CharacterStatus()

        # Set primary criminal status
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.MID, position))

        # Add placeholder domains
        status.set_status("public", FactionStatus(StatusLevel.LOW, "Troublemaker"))
        status.set_status("corporate", FactionStatus(StatusLevel.NONE, None))
        status.set_status("state", FactionStatus(StatusLevel.LOW, "Monitored"))

        # Inject primary domain
        kwargs["primary_status_domain"] = "criminal"

        # Default loyalty setup for Captain
        default_loyalties = {
            faction: 60,  #loyalty to their own faction
            "Law": 10,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        wallet = kwargs.pop("wallet", generate_wallet("Captain"))
        super().__init__(
            name=name, race=race, sex=sex, faction=faction,  region=region,
            location=location, status=status, wallet=wallet, loyalties=default_loyalties, motivations=motivations or self.default_motivations, **kwargs
        )

    def handle_observation(self, region):
        gang_observation_logic(self, region)

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"

class Manager(Character):
    is_concrete = True
    default_motivations = [
        ("earn_money", 5),
        ("gain_mid", 4),
        ("virtue_signal", 1)
    ]

    def __init__(self, name, race, sex, region, location, faction="None", position="Manager", loyalties=None, fun=1, hunger=1, status=None, motivations=None, **kwargs):
        

        random_cash = random.randint(400, 1000)
        wallet = kwargs.pop("wallet", generate_wallet("Manager"))

        if status is None:
            status = CharacterStatus()
            status.set_status("corporate", FactionStatus(StatusLevel.MID, position))
            status.set_status("public", FactionStatus(StatusLevel.LOW, "Corporate Drone"))
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, None))
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Permitted"))

        # Safe default for faction
        self.faction = faction

        # Setup default loyalties
        default_loyalties = {}
        if faction:
            default_loyalties[faction] = 50
        default_loyalties["Law"] = 40
        if loyalties:
            default_loyalties.update(loyalties)
        
         # Inject primary status domain
        kwargs["primary_status_domain"] = "corporate"

        super().__init__(
            name=name, race=race, sex=sex, faction=faction,  region=region,
            location=location, wallet=wallet, status=status, loyalties=default_loyalties, fun=fun,
            hunger=hunger, motivations=motivations or self.default_motivations, **kwargs
        )
        self.position = position
        
        # HQ logic (acts like __post_init__)
        self.HQ = None
        if self.faction and hasattr(self.faction, "HQ") and self.faction.HQ:
            self.HQ = self.faction.HQ
            self.location = self.HQ
            #print(f"Manager {self.name} starts at: {self.HQ.name} + has {self.wallet.bankCardCash}")
        else:
            print(f"⚠️ Manager {self.name} has no HQ assigned!")
        
    def whereabouts(self):
        region_name = self.region.name if hasattr(self.region, "name") else str(self.region)
        location_name = getattr(self.location, "name", str(self.location))
        sublocation = getattr(self, "sublocation", None)

        return f"{region_name}, {location_name}" + (f", {sublocation}" if sublocation else "")

    def default_skills(self):
        base = super().default_skills()
        base.update({
            "organize_employees": 12,
            "observation": 10,
            "appease": 12,
            "persuade": 12,
            "complain": 13,
        })
        return base

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"
    
class Subordinate(Character):
    is_concrete = False
    default_motivations = [("earn_money", 2)]
    def __init__(self, name, race, sex, faction, strength, agility, intelligence, luck, psy, toughness, morale, position="Subordinate", loyalties=None, status=None, ai=None, motivations=None, **kwargs):
        
        
        """ if race is None:
            race = "Terran" """
        if status is None:
            status = CharacterStatus()
            status.set_status(faction.name, FactionStatus(StatusLevel.LOW, position))
        
        default_loyalties = {
            faction: 20 if faction else 0,  # Avoid issues if faction is None
            "Law": 20,  # Meh, whatever
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})

        super().__init__(name, race=race, sex=sex, faction=faction,  strength=strength, agility=agility, intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, morale=morale,  loyalties=loyalties, position=position,
                         status=status, ai=ai, motivations=motivations or self.default_motivations, **kwargs)
        self.tasks = []# Explicitly initialize task list
        

class Employee(Subordinate):
    is_concrete = True
    default_motivations = [("earn_money", 5)]

    def __init__(self, name, race, sex, region, location, faction,  strength=9, agility=8, intelligence=8, luck=9, psy=1, toughness=7, morale=5, position="An employee", loyalties=None, motivations=None, status=None, **kwargs):
        

        # Default loyalty setup for Employee
        default_loyalties = {
            faction: 15 if faction else 0,  # Avoid issues if faction is None
            "Law": 15,  # Distrust of the law by default
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})

        kwargs["primary_status_domain"] = "corporate"

        if status is None:
            status = CharacterStatus()
            status.set_status("corporate", FactionStatus(StatusLevel.LOW, position))
            status.set_status("public", FactionStatus(StatusLevel.LOW, "Employee"))
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, None))
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Registered"))
            
        wallet = kwargs.pop("wallet", generate_wallet("CorporateSecurity"))
        super().__init__(
            name=name, race=race, sex=sex, faction=faction,  region=region,
            location=location, strength=strength, agility=agility, intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, morale=morale, position=position, status=status, wallet=wallet, loyalties=default_loyalties, motivations=motivations or self.default_motivations, **kwargs
        )
        
    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"

    
class CorporateSecurity(Subordinate):
    is_concrete = True
    default_motivations = [
        ("protect_vip", 4),
        ("patrol", 3),
        ("gain_mid", 4),
        ("find_safety", 3)
    ]
    def __init__(self, name, race, sex, region, location, faction, strength=12, agility =10, intelligence=8, luck=9, psy=1, toughness=13, morale=11, position="Security Guard", loyalties=None, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()
            status.set_status("corporate", FactionStatus(StatusLevel.MID, position))
            status.set_status("public", FactionStatus(StatusLevel.LOW, "Security Guard"))
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, None))
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Licensed"))

        # Default loyalty setup for CorporateSecurity
        default_loyalties = {
            faction: 50 if faction else 0,  # Avoid issues if faction is None
            "Law": 10,  # Not cops, just security
        }
        # Merge defaults with provided loyalties safely
        default_loyalties.update(loyalties or {})

        kwargs["primary_status_domain"] = "corporate"
        wallet = kwargs.pop("wallet", generate_wallet("CorporateSecurity"))
        super().__init__(
            name=name, race=race, sex=sex, faction=faction,  region=region,
            location=location, strength=strength, agility=agility, 
            intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, 
            morale=morale, wallet=wallet, position=position, 
            loyalties=default_loyalties, status=status, motivations=motivations or self.default_motivations, **kwargs
        )
        
        
        
        self.targetIsInMelee = False

        """ self.cash = 10
        self.bankCardCash = 100 """
        
    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
class CorporateAssasin(CorporateSecurity):
    is_concrete = True
    default_motivations = [
        ("steal_object", 3),
        ("steal_money", 3),
        ("gain_high", 5),
        ("find_safety", 4),
        ("escape_danger", 6)
    ]
    def __init__(self, name, race, sex, region, location, faction,  strength=12, agility=15, intelligence=15, toughness=13, morale=13, position="Unknown", loyalties=None, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()
            # Internal factions and corp value
            status.set_status("corporate", FactionStatus(StatusLevel.HIGH, "Elite Asset"))
            status.set_status("discretion", FactionStatus(StatusLevel.HIGH, "Ghostlike"))
            status.set_status("efficiency", FactionStatus(StatusLevel.HIGH, "Perfect Record"))

            # No public or criminal status
            status.set_status("public", FactionStatus(StatusLevel.NONE, None))
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, None))
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Licensed Ghost"))

        kwargs["primary_status_domain"] = "corporate"

        # Default loyalty setup for CorporateAssasin
        default_loyalties = {
            faction: 10 if faction else 0,  # Avoid issues if faction is None
            "Law": 0,  # No trust in the law
        }
        # Merge defaults with provided loyalties safely
        default_loyalties.update(loyalties or {})
        wallet = kwargs.pop("wallet", generate_wallet("CorporateAssasin"))
        super().__init__(
            name=name, race=race, sex=sex,  region=region,
            location=location, faction=faction, strength=strength, agility=agility, 
            intelligence=intelligence, luck=0, psy=0, toughness=toughness, 
            morale=morale, wallet=wallet, position=position, 
            loyalties=default_loyalties, status=status, motivations=motivations or self.default_motivations, **kwargs
        )
        
        # Assassin-specific weapon attributes
        self.rifleIsLoaded = True
        self.rifleCurrentAmmo = 15

        # Override base class financial stats
        """ self.cash = 400
        self.bankCardCash = 1000 """

        # Adjusted health based on toughness
        self.health = 120 + toughness

          # List to store items in the character's inventory
        def default_skills(self):
            base = super().default_skills()
            base.update({
                "stealth": 15,
                "melee_attack": 15,
                "melee_defend": 13,
                "dodge": 13,
                "infiltration": 14,
            })
            return base
        
    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"
    
    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
class GangMember(Subordinate):
    is_concrete = True
    default_motivations = [("idle", 1)]

    def __init__(self, name, race, sex, region, location, faction, strength=12, agility=11, intelligence=7, 
                luck=9, psy=2, toughness=14, morale=12,
                position="Gangster", loyalties=None, status=None, motivations=None, **kwargs):
        

         # Ensure status has a "criminal" domain, regardless of what Subordinate set
        if status is None:
            status = CharacterStatus()

        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.LOW, position))
        # Add public and state domains with neutral or default perception
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.LOW, "Street Thug"))
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Suspect"))

        # Always set the primary domain explicitly
        kwargs["primary_status_domain"] = "criminal"

        wallet = kwargs.pop("wallet", generate_wallet("GangMember"))

    # Default loyalty setup for GangMember
        default_loyalties = {}
        if faction:
            default_loyalties[faction] = 15
        default_loyalties["Law"] = 0
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        ai = GangMemberAI(self)
        super().__init__(
            name=name, race=race, sex=sex, faction=faction,  region=region,
            location=location, wallet=wallet, strength=strength, agility=agility, 
            intelligence=intelligence, luck=luck, psy=psy, toughness=toughness, 
            morale=morale, position=position, 
            loyalties=default_loyalties, status=status, ai=ai, motivations=motivations or self.default_motivations, **kwargs
        )
        
        # Enforce the primary domain (in case Character didn't get it from kwargs)
        self.primary_status_domain = "criminal"
        
        
        self.targetIsInMelee = False
        self.isAggressive = False
        #self.ai = GangMemberAI(self)
        #deprecated?

        """ self.cash = 50
        self.bankCardCash = 20 """

    def handle_observation(self, region):
        gang_observation_logic(self, region)

    def default_skills(self):
        base = super().default_skills()
        base.update({
            "stealth": 8,
            "melee_attack": 11,
            "melee_defend": 10,
            "dodge": 7,
            "threaten": 7,
        })
        return base
        
    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"
    
    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
class RiotCop(Character):
    is_concrete = True
    default_motivations = [
        ("patrol", 4),
        ("gain_mid", 4),
        ("virtue_signal", 2),
        ("find_safety", 3)
    ]
    def __init__(self, name, race, sex, region, location,  faction="The State", 
                 position="Pig", toughness=14, loyalties=None, fun=0, hunger=0, status=None, motivations=None, **kwargs):
        

    # Default loyalty setup for RiotCop
        default_loyalties = {
            faction: 80,  # High loyalty to their own faction
            "Law": 70,  # Law-abiding mindset
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})   
        
        if status is None:
            status = CharacterStatus()

        # Set state domain (primary authority)
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.MID, position))

        # Public perception varies (default to neutral)
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.LOW, "Enforcer"))

        # Criminal perception — threat/enemy
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.HIGH, "Enemy of the Street"))
        
        # Explicitly define primary domain
        kwargs["primary_status_domain"] = "state"
        wallet = kwargs.pop("wallet", generate_wallet("RiotCop"))
        super().__init__(
            name=name, race=race, sex=sex, region=region,
            location=location, faction=faction,
            fun=fun, hunger=hunger, strength=15, agility=4, intelligence=5, 
            luck=0, psy=0, toughness=toughness, morale=8, 
            loyalties=default_loyalties, wallet=wallet, status=status, position=position, motivations=motivations or self.default_motivations, **kwargs
        )
        
        # Weapon & Combat Attributes
        
        
        
        self.targetIsInMelee = False
        self.isAggressive = True
        self.targetIsInMelee = False

        # Armor & Finances
        
        self.isArmored = True
        self.armorValue = 30

        """ self.cash = 50
        self.bankCardCash = 300 """

          # List to store items in the character's inventory

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"

class Civilian(Character):
    default_motivations = [("have_fun", 2), ("earn_money", 4)]
    is_concrete = True # but it is also an intermediarz class for VIP

    def __init__(self, name, race, sex, region, location, strength=12, agility=10, intelligence=10, luck=0, psy=0, toughness=3, morale=2, position="Normie", loyalties=None, status=None, motivations=None, **kwargs):
        #print(f"Civilian created: {name}, Region: {region}, Location: {location}")
        
        
        if status is None:
            status = CharacterStatus()

        # Primary domain — public
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.LOW, position))

        # Placeholder domains
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.NONE, "Unknown"))
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.NONE, "Unaffiliated"))
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, "Uninvolved"))

        kwargs["primary_status_domain"] = "public"

        

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
        # Explicitly define primary domain
        
        wallet = kwargs.pop("wallet", generate_wallet("Civilian"))

        #You should not hardcode status in Civilian, because it serves multiple roles, intermediary and concrete
        super().__init__(
            name=name, race=race, sex=sex, region=region, location=location, strength=strength, agility=agility, intelligence=intelligence, 
            luck=luck, psy=psy, toughness=toughness, morale=morale, wallet=wallet, position=position, status=status, motivations=motivations or self.default_motivations,
            **kwargs
        )

        # Weapon & Combat Attributes
        
        
        self.targetIsInMelee = False
        self.location
        self.region
        self.is_employee = False

        """ self.cash = 50
        self.bankCardCash = 50 """

        # Inventory Initialization
        self.inventory = kwargs.get("inventory", Inventory(owner=self))

    
    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
class VIP(Civilian):
    is_concrete = True

    default_motivations = [
        ("gain_high", 6),
        ("have_fun", 3),
        ("influence", 3),
        ("virtue_signal", 1)
    ]

    def __init__(self, name, race, sex, region, location, position="VIP", loyalties=None,
        influence=0, strength=18, agility=10, intelligence=15, 
        luck=0, psy=0, toughness=5, morale=7, fun=0, hunger=0, status=None, motivations=None, **kwargs):
        

        if region is None:
            raise ValueError(f"Error: VIP {name} is being created with region=None! Check faction.region!")
        if not region.locations:
            print(f"Warning: Region {region.name} has no locations at VIP creation!")


        kwargs.setdefault("faction", "The State")  # Set default only if not provided
        #print(f"Initializing VIP: {name}, Region: {region}, Location: {location}")  # Debugging

        # Find a MunicipalBuilding in the region
        from location import MunicipalBuilding

        municipal_buildings = [loc for loc in region.locations if isinstance(loc, MunicipalBuilding)]
        location = municipal_buildings[0] if municipal_buildings else None  # Pick first available or None

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
        if status is None:
            status = CharacterStatus()

        # Elevate state status
        status.set_status("state", FactionStatus(StatusLevel.HIGH, position))

        # Adjust public visibility if needed
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.MID, "Recognized Figure"))

        # Corporate and criminal placeholders if needed
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.NONE, "Not Affiliated"))
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, "Unassociated"))

        kwargs["primary_status_domain"] = "state"
        wallet = kwargs.pop("wallet", generate_wallet("VIP"))
        super().__init__(
            name=name,
            race=race,
            sex=sex,
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            psy=psy,
            toughness=toughness,
            morale=morale,
            region=region,
            location=location,
            position=position,
            status=status,
            wallet=wallet,
            motivations=motivations or self.default_motivations,
            **kwargs # faction is already in kwargs
        )
        
        self.influence = influence
        self.targetIsInMelee = False

        """ self.cash = 500
        self.bankCardCash = bankCardCash  # Redundant but ensures it's explicitly set for VIP """

        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", Inventory(owner=self))
  # List to store items in the character's inventory
        self.position = position
        self.region = region  # Keep track of initial region
        self.location = location  # Is this being set properly?

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    
class Child(Civilian):
    is_concrete = True

    default_motivations = [("have_fun", 4), ("find_safety", 3)]

    def __init__(self, name, race, sex, region, location, faction="None", parent=None, bankCardCash=0, position="Minor", loyalties=None,
        influence=0, strength=3, agility=10, intelligence=5, 
        luck=0, psy=0, toughness=5, morale=1, fun=2, hunger=2, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()

        # Public: children are known or noticed
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.LOW, position))

        # State: tracked by civil systems (schooling, orphanages, etc.)
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Registered Minor"))

        # Placeholders
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.NONE, "None"))
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, "None"))

        kwargs["primary_status_domain"] = "public"

        # Default loyalty setup for Child
        default_loyalties = {
            parent: 90,  # loyalty to their own faction
            "Law": 30,  # Don't steal!
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})

        wallet = kwargs.pop("wallet", generate_wallet("Child"))
        super().__init__(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=region,
            location=location,
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
            loyalties=default_loyalties,
            wallet=wallet,
            status=status,
            motivations=motivations or self.default_motivations,
            **kwargs
        )
        
        self.parent = parent if isinstance(parent, Character) and parent.race == race else None
        self.influence = influence
        self.targetIsInMelee = False

        """ self.cash = 500
        self.bankCardCash = bankCardCash """ 

        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", Inventory(owner=self))
  # List to store items in the character's inventory
        self.position = position

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
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

    default_motivations = [
        ("increase_popularity", 4),
        ("virtue_signal", 3),
        ("gain_mid", 3),
        ("influence", 3),
        ("have_fun", 2)
    ]

    def __init__(self, name, race, sex, region, location, faction="None", position="Grifter", loyalties=None,
        influence=8, strength=10, agility=10, intelligence=15, 
        luck=0, psy=0, toughness=5, morale=2, fun=2, hunger=0, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()

        # Public domain – primary: high visibility
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.MID, position))

        # Corporate – potential sponsor deals
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.LOW, "Sponsor Affiliate"))

        # State – either monitored, favored, or ignored
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Monitored"))

        # Criminal – potential black market deals or shady activities
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, "None"))

        kwargs["primary_status_domain"] = "public"

        # Default loyalty setup for Influencer
        default_loyalties = {
            faction: 10,  # loyalty to their own faction, if any
            "Law": 15,  # Just, whatever
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})

        wallet = kwargs.pop("wallet", generate_wallet("Influencer"))
        super().__init__(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=region,
            location=location,
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
            loyalties=default_loyalties,
            wallet=wallet,
            status=status,
            motivations=motivations or self.default_motivations,
            **kwargs
        )
        
        self.influence = influence
        
        
        self.targetIsInMelee = False
        

        """ self.cash = 1000
        self.bankCardCash = bankCardCash """  

        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", Inventory(owner=self))
  # List to store items in the character's inventory
        self.position = position

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"

class Babe(Civilian):
    is_concrete = True

    default_motivations = [
        ("find_partner", 3),
        ("switch_partner", 3),
        ("gain_mid", 2),
        ("have_fun", 3),
        ("earn_money", 2)
    ]

    def __init__(self, name, race, sex, region, location, faction="None", partner=None, position="Variously Attached", loyalties=None,
        influence=7, strength=7, agility=10, intelligence=10, 
        luck=0, psy=0, charisma=14, toughness=4, morale=0, fun=2, hunger=2, status=None, preferred_actions=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()

        # Public admiration
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.MID, position))

        # Corporate – possibly trophy relationships
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.LOW, "Trophy Partner"))

        # State – usually low, unless scandal emerges
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.LOW, "Unremarkable"))

        # Criminal – some may connect to gangs
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, "None"))

        kwargs["primary_status_domain"] = "public"

        # Default loyalty setup for Babe
        default_loyalties = {
            partner: 4,  # loyalty if you can call it that
            "Law": 15,  # Just, whatever
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        wallet = kwargs.pop("wallet", generate_wallet("Babe"))
        super().__init__(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=region,
            preferred_actions=preferred_actions,
            location=location,
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
            loyalties=default_loyalties,
            wallet=wallet,
            status=status,
            motivations=motivations or self.default_motivations,
            **kwargs
        )
        
        self.influence = influence
        
        
        self.targetIsInMelee = False
        

        """ self.cash = 1000
        self.bankCardCash = bankCardCash  """

        self.health = 120 + toughness
        self.inventory = kwargs.get("inventory", Inventory(owner=self))
  # List to store items in the character's inventory
        self.position = position
        self.partner = Character

        self.base_preferred_actions = {
            self.flirt: "powerful man"
        }

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"
    
    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"

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

    default_motivations = [
        ("patrol", 4),
        ("investigate_crime", 5),  # add support in your FSM or GOAP
        ("decrease_hostilities", 3),
        ("snitch", 2),
        ("find_safety", 4)
    ]

    def __init__(self, name, race, sex, region, location, faction="The State", position="Cop", toughness=13, loyalties=None, fun=0, hunger=0, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()

        # Primary domain is 'state'
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.MID, position))

        # Public perception — varies by behavior
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.MID, "Investigator"))

        # Criminal domain — ambiguous, especially if corrupt
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.NONE, "None"))

        # Corporate — possibly if embedded in corp-police units
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.LOW, "Unknown"))

        kwargs["primary_status_domain"] = "state"

        start_location = None  # Ensure start_location is always defined
        
    # Default loyalty setup for Detective
        default_loyalties = {
            faction: 80,  # loyalty to their own faction
            "Law": 90,  # It's the law, no on should be above it
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})

        wallet = kwargs.pop("wallet", generate_wallet("dealer"))
        super().__init__(
            name=name,
            race=race,
            sex=sex,
            region=region,
            location=location,
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
            wallet=wallet,
            loyalties=default_loyalties,
            status=status,
            motivations=motivations or self.default_motivations,
            **kwargs
        )
        
        # Weapon & Combat Attributes
        
        
        
        self.targetIsInMelee = False
        self.isAggressive = True
        self.targetIsInMelee = False

        # Armor & Finances
        
        self.isArmored = True
        self.armorValue = 30

        """ self.cash = 50
        self.bankCardCash = 300 """

          # List to store items in the character's inventory

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}" 
        
        #Separates the raw data from the computed property – 
                                                    #whereabouts is computed dynamically using multiple attributes
                                                    #  (region, location, sublocation).

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"
        
class Taxman(Character):

    is_concrete = True

    default_motivations = [
        ("earn_money", 3),
        ("virtue_signal", 2),
        ("influence", 2),
        ("find_safety", 3)
    ]

    def __init__(self, name, race, sex, region, location, faction="State", position="Tax Official", preferred_actions=None, loyalties=None, fun=-1, hunger=0, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()

        # Primary status in the state domain
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.MID, position))

        # Public view — often negative
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.LOW, "Taxman"))

        # Criminals see them as a threat
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.LOW, "Target"))

        # Corporate sees them with suspicion or bureaucracy
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.LOW, "Auditor"))

        kwargs["primary_status_domain"] = "state"

        default_loyalties = {
            faction: 50,  # Somewhat loyal to faction
            "Law": 40,
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        wallet = kwargs.pop("wallet", generate_wallet("dealer"))
        super().__init__(
            name=name, race=race, sex=sex, region=region,
            location=location, faction=faction, wallet=wallet, loyalties=default_loyalties, fun=fun,
            hunger=hunger, preferred_actions=preferred_actions, status=status, motivations=motivations or self.default_motivations, **kwargs
        )
        self.base_preferred_actions = {
            self.squeeze_taxes: "corporation"
        }

        self.position = position

        # self.bankCardCash = bankCardCash

        self.inventory = kwargs.get("inventory", Inventory(owner=self))
  # List to store items in the character's inventory
    
    # figure out how specific charcters store their specific actions, here or in that file or both
    def squeeze_taxes(self, target):
        print(f"{self.name} squeezes taxes from {target}!")

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"
    

    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"

class Accountant(Character):
    is_concrete = True

    default_motivations = [
        ("earn_money", 4),
        ("find_safety", 3),
        ("influence", 2)
    ]

    def __init__(self, name, race, sex, region, location, faction="None", position="Accountant", loyalties=None, fun=0, hunger=0, status=None, motivations=None, **kwargs):
        

        if status is None:
            status = CharacterStatus()

        # Primary corporate domain
        if "corporate" not in status.status_by_domain:
            status.set_status("corporate", FactionStatus(StatusLevel.MID, position))

        # Public view: neutral or suspicious
        if "public" not in status.status_by_domain:
            status.set_status("public", FactionStatus(StatusLevel.LOW, "Corporate Pencil Pusher"))

        # Criminal view: target or utility
        if "criminal" not in status.status_by_domain:
            status.set_status("criminal", FactionStatus(StatusLevel.LOW, "Possible Asset"))

        # State view: neutral to mid respect
        if "state" not in status.status_by_domain:
            status.set_status("state", FactionStatus(StatusLevel.MID, "Finance Worker"))

        kwargs["primary_status_domain"] = "corporate"
        
        default_loyalties = {
            faction: 70,  # Somewhat loyal to faction
            "Law": 20,
        }
        # Merge defaults with provided loyalties
        default_loyalties.update(loyalties or {})
        
        wallet = kwargs.pop("wallet", generate_wallet("dealer"))
        super().__init__(
            name=name, race=race, sex=sex, faction=faction, region=region,
            location=location, wallet=wallet, loyalties=default_loyalties, fun=fun,
            hunger=hunger, status=status, motivations=motivations or self.default_motivations, **kwargs
        )
        self.position = position

        self.inventory = kwargs.get("inventory", Inventory(owner=self))
  # List to store items in the character's inventory
    

    def __repr__(self):
        base = super().__repr__()  # Will call Character.__repr__
        return f"{base}, Faction: {self.faction or 'None'}"

    
    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"