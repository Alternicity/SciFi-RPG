#TheKindMan.py
from base.character import Character
from status import CharacterStatus, StatusLevel, FactionStatus
from wallet import generate_wallet
from inventory import Inventory
from weapons import Knife, Pistol
from objects.InWorldObjects import Wallet
from motivation.motivation_presets import MotivationPresets

class Alter(Character):
    default_motivations = [
        ("protect_Luna", 10),
        ("earn_money", 8),
        ("gain_elite", 7),
        ("gain_independence", 7),
        ("create", 9)
    ]

    def __init__(self, name, race, sex, region, location, faction, position="IndyDev", loyalties=None, status=None, motivations=None, **kwargs):
        

        # Default loyalty setup for CEO
        default_loyalties = {
            "Luna": 100,  # Disdain of the law, unless its useful 
            "IRL sons": 100,
            "IRL friends": 80
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
        status.set_status("state", FactionStatus(StatusLevel.LOW, "Influential Lobbyist"))

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

    def get_percept_data(self, observer=None):
        data = super().get_percept_data(observer)
        data["description"] = f"{self.name}, the CEO Leader of {self.faction.name}"
        data["tags"].extend(["corporation", "leader"])
        return data

    def issue_directive(self, directive):
        print(f"{self.name} (CEO) issues directive: {directive}")
        self.directives.append(directive)
    
    @property
    def whereabouts(self):
        
        return f"{self.region}, {self.location}" if not hasattr(self, "sublocation") else f"{self.region}, {self.location}, {self.sublocation}"
    
#instantiation for character_creation_funcs
{
        "class": Alter,
        "name": "U7s",
        "sex": "male",
        "race": "English",
        "faction_name": "Factionless",
        "region_name": "southville",
        "location_name": "None",

        
        "wallet": Wallet(bankCardCash=50),
        "preferred_actions": {"Feed": 1, "Teach": 2, "Protect": 2, "Create": 2 },
        "motivations": MotivationPresets.for_class("GangMember"),
        "custom_skills": {"stealth": 20, "observation": 20},
        "primary_status_domain": "corporate",
        "status_data": {
            "public": {"level": StatusLevel.LOW, "title": "Indy"},
            "criminal": {"level": StatusLevel.LOW, "title": "Alone"}
    },
},

#instantiation for createCivilians
# Create Luna
""" status = CharacterStatus()
status.set_status("public", FactionStatus(StatusLevel.LOW, "Orphan"))
name = "U7s"
sex = "Male"
race = "English"
faction = factionless
location = get_house_location(all_locations)  # implement this helper

motivations=MotivationPresets.for_class("Alter"), 

U7s = Alter(
    name="U7s",
    race="English",
    sex="Male",
    faction=factionless,
    region=factionless.region,
    location=location,
    motivations=motivations,
    status=status,
    intelligence=20,  # Override default
    strength=18,
    agility=18,
    fun=16,
    hunger=1,
    position="Codex Avatar",
    notable_features=["long brown hair", "calm demeanor"],
    appearance={"clothing": "smart but flawed"},
    self_esteem=15,
        )
U7s.skills.update({
    "explore_math": 16,
    "use_advanced_python_features": 20,
    "persuasion": 20,
}) """