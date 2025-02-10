import logging
import random
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, GangMember, Child, Influencer,
                           Babe, Detective, Accountant, Taxman)
import os
import csv
import random
from loader import load_names_from_csv
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def generate_name(race, gender):
    """
    Generates a random full name based on the race and gender.
    """
    from common import BASE_CHARACTERNAMES_DIR
    if race is None:
        race = "Martian"  # Default race if None is passed

    filepath = os.path.join(BASE_CHARACTERNAMES_DIR, f"{race}Names.txt")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Name file for race '{race}' not found: {filepath}")
    
    male_names, female_names, family_names = load_names_from_csv(filepath)
    
    if gender.lower() == "male":
        first_name = random.choice(male_names) if male_names else "Unknown"
    elif gender.lower() == "female":
        first_name = random.choice(female_names) if female_names else "Unknown"
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    last_name = random.choice(family_names) if family_names else "Unknown"
    
    return f"{first_name} {last_name}"

def generate_faction_characters(faction, all_regions):

    """
    Generates characters for a given faction with appropriate race distribution and assigns valid locations.
    
    Gangs: Homogeneous race selection.
    Corporations: Can be mixed (for now, default to homogeneous until rules are clearer).
    """

    from base_classes import Character
    faction_type = faction.type  # Assuming factions have a type attribute ('gang', 'corporation', or 'state')
    valid_races = list(Character.VALID_RACES)

    # Choose a dominant race for the faction
    faction_race = random.choice(valid_races) if faction_type == "gang" else None

    # Handle faction location logic properly
    from faction import State # Ensure this is necessary
    from location import MunicipalBuilding, Location, PoliceStation

    """Creates initial characters for a faction based on its type."""
    characters = []

    # Determine faction locations
    if isinstance(faction, State):  
        locations = [loc for region in all_regions for loc in region.locations if isinstance(loc, MunicipalBuilding)]
    elif hasattr(faction, "region") and faction.region:
        locations = [loc for loc in faction.region.locations if isinstance(loc, MunicipalBuilding)]
    else:
        locations = []  # No valid locations if there's no region

    #gangs are racially homogenous
    if faction.type == "Gang":
        characters.append(Boss(name=generate_name(faction_race, random.choice(["Male", "Female"])), race=faction_race, faction=faction, start_region=faction.region, start_location=None, initial_motivations=["gain_high"]))
        #possibly use faction=faction.name
        
        for _ in range(random.randint(2, 3)):
            characters.append(Captain(name=generate_name(faction_race, random.choice(["Male", "Female"])), race=faction_race, faction=faction, start_region=faction.region, start_location=None, initial_motivations=["gain_high"]))
            #possibly use faction=faction.name

        for _ in range(random.randint(5, 10)):
            characters.append(GangMember(name=generate_name(faction_race, random.choice(["Male", "Female"])), race=faction_race, faction=faction, start_region=faction.region, start_location=None, initial_motivations=["gain_mid"]))
    
    elif faction_type == "Corporation":
        characters.append(CEO(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region, start_location=None, initial_motivations=["increase_popularity"]))

        for _ in range(random.randint(2, 3)):
            characters.append(Manager(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region, start_location=None, initial_motivations=["influence"]))
        
        for _ in range(random.randint(5, 10)):
            characters.append(Employee(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region, start_location=None, initial_motivations=["earn_money"]))
        
        for _ in range(random.randint(3, 5)):
            characters.append(CorporateSecurity(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region, start_location=None, initial_motivations=["patrol"]))
        
        for _ in range(random.randint(1, 3)):
            characters.append(Accountant(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region, start_location=None, initial_motivations=["reduce taxes"]))

    elif faction_type == "The State":
        characters.append(VIP(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region or faction.region,  
            start_location=MunicipalBuilding,  
            initial_motivations=["gain_elite"]))

        for _ in range(random.randint(2, 3)):
            characters.append(Manager(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region or faction.region,  
                start_location=MunicipalBuilding,  
                initial_motivations=["influence"]))

        for _ in range(random.randint(5, 10)):
            characters.append(Employee(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region or faction.region,  
                start_location=MunicipalBuilding,  
                initial_motivations=["influence"]))

        for _ in range(random.randint(3, 5)):
            characters.append(RiotCop(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region or faction.region,  
                start_location=PoliceStation,  
                initial_motivations=["influence"]))
            
        for _ in range(random.randint(2, 4)):
            characters.append(Taxman(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region or faction.region,  
                start_location=MunicipalBuilding,  
                initial_motivations=["influence"]))

        for _ in range(random.randint(1, 3)):
            characters.append(Detective(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, start_region=faction.region or faction.region,  
                start_location=PoliceStation,  
                initial_motivations=["influence"]))

    return characters

# Define location categories (if 'type' is not present in the Location class)
WORKPLACES = {"Shop", "CorporateStore", "MechanicalRepairWorkshop", "ElectricalRepairWorkshop",
              "Factory", "Nightclub", "Mine", "Powerplant", "Airport", "Port", "Cafe",
              "Warehouse", "ResearchLab", "Museum", "Library", "SportsCentre", "Holotheatre"}
PUBLIC_PLACES = {"Museum", "Library", "SportsCentre", "Holotheatre", "Park", "VacantLot"}
RESIDENTIAL = {"ApartmentBlock", "House"}

def create_civilian_population(locations, num_civilians=100, num_employees=50):
    """Generate civilians and employees, assigning them to logical locations."""
    civilians = []

    # Categorize locations
    homes = [loc for loc in locations if loc.__class__.__name__ in RESIDENTIAL]
    workplaces = [loc for loc in locations if loc.__class__.__name__ in WORKPLACES]
    public_spaces = [loc for loc in locations if loc.__class__.__name__ in PUBLIC_PLACES]

    # Generate civilians
    for _ in range(num_civilians):
        race = random.choice(["Terran", "Martian", "Venusian", "Japanese", "German"])  # Expand as needed
        gender = random.choice(["male", "female"])
        name = generate_name(race, gender)  # Implement this function to read CSVs

        home = random.choice(homes) if homes else None
        public_place = random.choice(public_spaces) if public_spaces else None

        civilian = Civilian(
            name=name,
            start_location=home if home else public_place,
            race=race,
            initial_motivations=["earn_money", "have_fun", "find_partner"]
        )
        civilians.append(civilian)

    # Generate employees
    for _ in range(num_employees):
        race = random.choice(["Terran", "Martian", "Venusian", "Japanese", "German"])
        gender = random.choice(["male", "female"])
        name = generate_name(race, gender)

        home = random.choice(homes) if homes else None
        workplace = random.choice(workplaces) if workplaces else None

        employee = Employee(
            name=name,
            faction=None,  # Employees can be assigned to corporations later
            race=race,
            start_location=workplace if workplace else home,
            initial_motivations=["earn_money", "gain_mid", "patrol"]
        )
        civilians.append(employee)

    return civilians

def create_all_characters(factions, locations, all_regions):
    #Generates all characters for the game and displays summary.
    all_characters = []
    
    for faction in factions:
        all_characters.extend(generate_faction_characters(faction, all_regions))

    all_characters.extend(create_civilian_population(locations))
    
    return all_characters

def player_character_options() -> list:
        #a temporary function to offer limited player character object creation for intial game mechanic testing
        #a more robust selection system will be implemented later.
    characters = [
        #VIP(name="Jurgen", bankCardCash=10000, faction="The State", fun=1, hunger=2),
        Manager(name="Carolina", faction="BlueCorp", bankCardCash=500, fun=1, hunger=3),
        GangMember(name="Swiz", faction="White Gang", bankCardCash=50, fun=1, hunger=3),
        #CorporateAssasin(name="Jane", faction="BlueCorp", bankCardCash=10000, fun=0, hunger=1),
        #Civilian(name="Vihaan", bankCardCash=100, faction="Nonce", fun=0, hunger=7),
        #CorporateSecurity(name="John", faction="BlueCorp", bankCardCash=200, fun=0, hunger=4),
        #RiotCop(name="Cletus", faction="The State", bankCardCash= 125, fun=1, hunger=4),
        #CEO(name="Terrence", faction="BlueCorp", bankCardCash=10000, fun=5, hunger=0),
        #Boss(name="Soren", faction="White Gang", bankCardCash=3000, fun=3, hunger=1),
        #Captain(name="Sven", faction="White Gang", bankCardCash=200, fun=2, hunger=1),
        #Employee(name="Susana", faction="BlueCorp", bankCardCash=100, fun=0, hunger=4),
        
    ]
    return characters