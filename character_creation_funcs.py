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
from utils import get_faction_by_name, get_location_by_name, get_region_by_name


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
    print(f"Generated name: {first_name} {last_name}")
    return f"{first_name} {last_name}" #this is TWO variables, is that expected
    #DO we need a name = first_name + last_name


def generate_faction_characters(faction, all_regions, location_objects):
    print(f"DEBUG: Entered generate_faction_characters() for {faction.name} (Type: {faction.type})")
    print("generate_faction_characters() is being called!")
    print(f" generate_faction_characters() START for {faction.name}") 
    print(f"DEBUG: Processing faction {faction.name} ({faction.type})")

    #here faction_obj is not accesssed, should it be? SHould it be changed?
    #faction_obj = get_faction_by_name(faction, factions) if isinstance(faction, str) else faction
    #print(f"🔍 Checking attributes of faction {faction.name}: {dir(faction)}")
    #print(f"Faction Type: {faction.type}")
    
    #encapsulate in a function get_VALID_RACES()
    from base_classes import Character
    valid_races = list(Character.VALID_RACES)

    # Choose a dominant race for the faction
    faction_race = random.choice(valid_races) if faction.type == "gang" else None

    # Handle faction location logic properly
    from faction import State, GeneralPopulation # Ensure this is necessary
    from location import MunicipalBuilding, Location, PoliceStation

    """Creates initial characters for a faction based on its type."""
    characters = []

    # Determine faction locations
    if isinstance(faction, State):  
        #below, locations is not accessed
        locations = [loc for region in all_regions for loc in region.locations if isinstance(loc, MunicipalBuilding)]
    elif hasattr(faction, "region") and faction.region:
        locations = [loc for loc in faction.region.locations if isinstance(loc, MunicipalBuilding)]
    else:
        locations = []  # No valid locations if there's no region
    
    from location import HQ

    if faction.type == "Gang":
        #generate_name requires paramenters race, gender, sp should race=faction_race be here before the follwoing line:
        
        print(f"Creating Boss for {faction.name}...")
        boss = Boss(
        name=generate_name(faction_race, random.choice(["Male", "Female"])),
        race=faction_race,
        faction=faction,
        region=faction.region,
        location=None,
        initial_motivations=["gain_high"]
    )

        characters.append(boss)
        print(f"Boss Created: {boss.name} (Faction: {faction.name})")




        for _ in range(random.randint(2, 3)):
            characters.append(Captain(name=generate_name(faction_race, random.choice(["Male", "Female"])), race=faction_race, faction=faction, region=faction.region, location=None, initial_motivations=["gain_high"]))
            #possibly use faction=faction.name

        for _ in range(random.randint(5, 10)):
            characters.append(GangMember(name=generate_name(faction_race, random.choice(["Male", "Female"])), race=faction_race, faction=faction, region=faction.region, location=None, initial_motivations=["gain_mid"]))
        
    elif faction.type == "Corporation":
        from create import factions
        # Ensure characters are created specifically for each corporation
        from faction import Corporation
        for corp in [f for f in factions if isinstance(f, Corporation)]:
            
            corp_hqs = [loc for loc in region.locations if isinstance(loc, HQ) and loc.faction == faction]
            corp_hq = corp_hqs[0] if corp_hqs else None  # Get the first matching HQ or None

            characters.append(CEO(
                name=generate_name(None, random.choice(["Male", "Female"])),
                faction=faction,
                region=faction.region,
                location=corp_hq,  # Assign the correct HQ for this corporation
                initial_motivations=["increase_profits"]
            ))

            for _ in range(random.randint(2, 3)):
                characters.append(Manager(name=generate_name(None, random.choice(["Male", "Female"])),
                    faction=faction,
                    region=faction.region,
                    location=corp_hq,
                    initial_motivations=["earn_money, gain_high"]))
        

            for _ in range(random.randint(5, 10)):
                characters.append(Employee(name=generate_name(None, random.choice(["Male", "Female"])),
                    faction=faction,
                    region=faction.region,
                    location=corp_hq,
                    initial_motivations=["earn_money"]))
        
            for _ in range(random.randint(3, 5)):
                characters.append(CorporateSecurity(name=generate_name(None, random.choice(["Male", "Female"])),
                    faction=faction,
                    region=faction.region,
                    location=corp_hq,
                    initial_motivations=["patrol, observe"]))
        
            for _ in range(random.randint(1, 3)):
                characters.append(Accountant(name=generate_name(None, random.choice(["Male", "Female"])),
                    faction=faction,
                    region=faction.region,
                    location=corp_hq,
                    initial_motivations=["reduce taxes, earn money"]))

    elif faction.type == "The State":
        #print(f"Creating VIP for faction: {faction.name}, Region: {faction.region}")
        #print(f"Faction Region: {faction.region}")  # Debugging
        region = faction.region if faction.region else random.choice(all_regions)

        #print(f"Assigning region {region} to VIP")  # Debugging
        #print(f"Creating VIP for faction {faction.name} in region {faction.region}")

        if faction.region is None:
            raise ValueError(f"Error: faction '{faction.name}' has no region assigned! Fix in create_factions().")

        
        from location import MunicipalBuilding
        municipal_buildings = [loc for loc in region.locations if isinstance(loc, MunicipalBuilding)]
        location_instance = municipal_buildings[0] if municipal_buildings else None
        characters.append(VIP(
            name=generate_name(None, random.choice(["Male", "Female"])),
            faction=faction,
            region=faction.region if faction.region else "Default Region",
            location=location_instance,  
            initial_motivations=["gain_elite"]
))
        #print(f"MunicipalBuilding = {MunicipalBuilding} ({type(MunicipalBuilding)})")# Debugging
        #print(f"VIP from elif Faction: {faction.name}, Region: {faction.region}")
        for _ in range(random.randint(2, 3)):
            characters.append(Manager(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, region=faction.region or faction.region,  
                location=MunicipalBuilding,  
                initial_motivations=["influence"]))

        for _ in range(random.randint(5, 10)):
            characters.append(Employee(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, region=faction.region or faction.region,  
                location=MunicipalBuilding,  
                initial_motivations=["influence"]))


        police_stations = [loc for loc in faction.region.locations if isinstance(loc, PoliceStation)]
        riotcop_location = police_stations[0] if police_stations else None  # First police station or None
        for _ in range(random.randint(3, 5)):
            characters.append(RiotCop(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, region=faction.region or faction.region,
                location=riotcop_location,  # Clearer naming
                initial_motivations=["earn_money, enforce_law"]))
            

        municipal_buildings = [loc for loc in faction.region.locations if isinstance(loc, MunicipalBuilding)]
        taxman_location = municipal_buildings[0] if municipal_buildings else None  # First municipal building or None
        for _ in range(random.randint(2, 4)):
            characters.append(Taxman(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, region=faction.region or faction.region,  
                location=taxman_location,  
                initial_motivations=["gain_money, squeeze_taxes"]))


        police_stations = [loc for loc in faction.region.locations if isinstance(loc, PoliceStation)]
        detective_location = police_stations[0] if police_stations else None  # First police station or None
        for _ in range(random.randint(1, 3)):
            characters.append(Detective(name=generate_name(None, random.choice(["Male", "Female"])), faction=faction, region=faction.region or faction.region,   
                location=detective_location,
                initial_motivations=["earn_money, enforce_law"]))
        print(f"generate_faction_characters() executed, created {len(characters)} characters")        
    return characters

# Define location categories (if 'type' is not present in the Location class)
WORKPLACES = {"Shop", "CorporateStore", "MechanicalRepairWorkshop", "ElectricalRepairWorkshop",
              "Factory", "Nightclub", "Mine", "Powerplant", "Airport", "Port", "Cafe",
              "Warehouse", "ResearchLab", "Museum", "Library", "SportsCentre", "Holotheatre"}
PUBLIC_PLACES = {"Museum", "Library", "SportsCentre", "Holotheatre", "Park", "VacantLot"}
RESIDENTIAL = {"ApartmentBlock", "House"}


# Outside the function (global or passed in)
from faction import GeneralPopulation
general_population_faction = GeneralPopulation(name="General Population", violence_disposition="low")

def create_civilian_population(locations, num_civilians=10, num_employees=5):
    """Generate civilians and employees, assigning them to logical locations."""
    print(" create_civilian_population() is about to run")

    civilians = []

    # Categorize locations
    homes = [loc for loc in locations if loc.__class__.__name__ in RESIDENTIAL]
    workplaces = [loc for loc in locations if loc.__class__.__name__ in WORKPLACES]
    public_spaces = [loc for loc in locations if loc.__class__.__name__ in PUBLIC_PLACES]
    #where are these constants? Would this data be better noted in Location class defintions?
    #attribute list, as a location can be more than one

    # Generate civilians
    for _ in range(num_civilians):
        race = random.choice(["French", "Martian", "Italian", "Japanese", "German"]) #use get_VALID_RACES()
        gender = random.choice(["male", "female"])
        name = generate_name(race, gender)  # Implement this function to read CSVs

        home = random.choice(homes) if homes else None
        public_place = random.choice(public_spaces) if public_spaces else None
        location = home if home else public_place

        # Ensure start_region is defined
        region = location.region if location else None

        civilian = Civilian(
            name=name,
            region=region,  # FIX: Ensure start_region is passed
            location=location,
            race=race,
            initial_motivations=["earn_money", "have_fun", "find_partner"]
        )
        civilians.append(civilian)

    # Generate employees
    all_employees =  {} 
    # Key: character.name, Value: character.workplace

    for _ in range(num_employees):
        race = random.choice(["French", "Martian", "Italian", "Japanese", "German"])
        gender = random.choice(["male", "female"])
        name = generate_name(race, gender)
        workplace = random.choice(workplaces) if workplaces else None
        for _ in range(num_employees):
            default_faction = workplace.faction if workplace and hasattr(workplace, 'faction') else general_population_faction
        
        home = random.choice(homes) if homes else None
        location = workplace if workplace else home

        # Ensure start_region is defined
        region = location.region if location else None

        employee = Employee(
            name=name,
            faction=default_faction,  # Employees can be assigned to corporations later
            region=region,  # Ensure start_region is passed
            location=location,
            race=race,
            initial_motivations=["earn_money", "gain_mid", "patrol"]
        )
        civilians.append(employee)

    return civilians

def create_all_characters(factions, locations, all_regions, location_objects):
    """Generates all characters for the game and displays summary."""
    #print("DEBUG: factions contains:", factions)  # Check the input
    print("\n" * 3)  # Line breaks for clarity
    print("*" * 60)  # Start separator
    print("create_all_characters() is about to run")
    print("*" * 60)

    all_characters = []
    
    for faction in factions:
        """ print(f"\n🟢 Processing a faction: {faction}")  # Debug print

        if isinstance(faction, str):
            faction = get_faction_by_name(faction, factions)
            print(f"DEBUG: After lookup, faction is {faction} (Type: {type(faction)})")

        if not hasattr(faction, "name"):  # Check if faction is still incorrect
            print(f"❌ ERROR: Faction is not an object, but a {type(faction)}")
            print(f"Faction contents: {faction}")
            raise TypeError(f"Expected a faction object, but got {type(faction)}") """
        #START HERE


        new_characters = generate_faction_characters(faction, all_regions, location_objects)

        print(f"✅ Finished {faction.name}, generated {len(new_characters)} characters")
        all_characters.extend(new_characters)

    civilians = create_civilian_population(locations)
    all_characters.extend(civilians)

    return all_characters


def player_character_options(all_regions, factions) -> list:
    print("Checking available regions and locations...")
    # Ensure we get a valid Corporation
    from faction import Corporation
    available_corporations = [faction for faction in factions if isinstance(faction, Corporation)]
    if not available_corporations:
        raise ValueError("No corporation factions available!")

    selected_faction = random.choice(available_corporations)  # Pick one at random

    characters = [
Manager(
    name="Karen",
    faction=get_faction_by_name("Hannival", factions),  #Bluecorp is a placeholder, here we must get an
    #instantiated, named Corporation object, randomly or give the player teh choice from a list, using display.py
    #OR automatically assign this character to ready instantiated GeneralPopulation faction, then get corp choice
    #faction=selected_faction,  # Now it’s an actual Corporation object, not a string
    region=get_region_by_name("Downtown", all_regions),  
    location=get_location_by_name("Municipal Building", all_regions),  # Ensures it's an object
    bankCardCash=500,
    fun=1,
    hunger=3
)  
        
        
        
        
        #GangMember(name="Swiz", faction="White Gang", start_region="Easternhole", start_location="Stash", bankCardCash=50, fun=1, hunger=3),

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