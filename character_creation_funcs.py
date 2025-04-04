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
from location import MunicipalBuilding, PoliceStation, HQ, Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalRepairWorkshop, Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Warehouse, ResearchLab, Museum, Library, SportsCentre, Holotheatre, Park, VacantLot, ApartmentBlock, House





def get_valid_races():
    from base_classes import Character
    return list(Character.VALID_RACES)

from common import BASE_CHARACTERNAMES_DIR
def generate_name(race, gender):


    """Generate a full name based on race and gender."""
    valid_races = get_valid_races()  # Get list of valid races from Character class

    # If no race is provided, choose one randomly from valid races
    if race is None:
        race = random.choice(valid_races)
    if race not in valid_races:
        raise ValueError(f"Invalid race '{race}'. Must be one of: {valid_races}")
    
    filepath = os.path.join(BASE_CHARACTERNAMES_DIR, f"{race}Names.txt")

    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found! {filepath}")
        return "Unknown Unknown"

    #print(f"DEBUG: Looking for name file at {filepath}")
    male_names, female_names, family_names = load_names_from_csv(filepath)
    #print(f"DEBUG: Loaded {len(male_names)} male, {len(female_names)} female, {len(family_names)} family names for {race}")
    
    #is gender actually present here?
    if gender.lower() == "male":
        first_name = random.choice(male_names) if male_names else "Unknown"
        #assign also characters 
    elif gender.lower() == "female":
        first_name = random.choice(female_names) if female_names else "Unknown"
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    last_name = random.choice(family_names) if family_names else "Unknown"
    
    full_name = f"{first_name} {last_name}"  # Concatenate first and last name
    #print(f"Generated name: {full_name}")  # Debugging output

    return full_name

def generate_faction_characters(faction, all_regions, all_locations):
    from create_game_state import get_game_state
    game_state = get_game_state()
    MuniBuildings = None  # Initialize at the start of the function
    valid_races = get_valid_races()
    state_staff = []
    # Choose a dominant race for the faction
    faction_race = random.choice(valid_races) if faction.type == "gang" else None

    # Handle faction location logic properly
    from faction import State, GeneralPopulation # Ensure this is necessary
    from location import Region

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

    if faction.type == "Gang":        
        print(f"Creating Boss for {faction.name}...")
        boss = Boss(
        name=generate_name(faction_race, random.choice(["Male", "Female"])),
        race=faction_race,
        faction=faction,
        region=faction.region,
        location=None,
        initial_motivations=["gain_high"]
    )

        # Assign boss to the correct gang in GameState
        from create_game_state import get_game_state
        game_state = get_game_state()
        for gang in game_state.gangs:
            if gang.name == faction.name:  # Match gang by name
                gang.add_boss(boss)
                break

        characters.append(boss)  # Add the boss to the character list
        print(f"Boss Created: {boss.name} (Faction: {faction.name})")

        for _ in range(random.randint(2, 3)):
            captain = Captain(
                name=generate_name(faction_race, random.choice(["Male", "Female"])),
                race=faction_race,
                faction=faction,
                region=faction.region,
                location=None,
                initial_motivations=["gain_high"]
            )
            characters.append(captain)
            faction.members.append(captain)

        for _ in range(random.randint(5, 10)):
            characters.append(GangMember(name=generate_name(faction_race, random.choice(["Male", "Female"])), race=faction_race, faction=faction, region=faction.region, location=None, initial_motivations=["gain_mid"]))
        
    elif faction.type == "Corporation":
        from create import factions
        # Ensure characters are created specifically for each corporation
        from faction import Corporation
        for corp in [f for f in factions if isinstance(f, Corporation)]:
            
            corp_hqs = [loc for loc in faction.region.locations if isinstance(loc, HQ) and loc.faction == faction]
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
    
        for _ in range(random.randint(3, 6)):
            characters.append(Employee(name=generate_name(None, random.choice(["Male", "Female"])),
                faction=faction,
                region=faction.region,
                location=corp_hq,
                initial_motivations=["earn_money"]))
    
        for _ in range(random.randint(2, 4)):
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
        
        race = random.choice(["Terran", "Martian", "German", "French"])  # Adjust races as needed
        gender = random.choice(["Male", "Female"])
        name = generate_name(race, gender) #needs to be integrated into cahracter creation below, and names assigned
        
        # Ensure faction.region and locations exist
        if not faction.region or not faction.region.locations:
            print(f"Faction Region: {faction.region}")
            print(f"Locations in Region: {faction.region.locations if faction.region else 'No Region'}")
            raise ValueError(f"No valid region or locations found for faction {faction.name}")

        # Attempt assignment
        MuniBuildings = game_state.municipal_buildings.get(faction.region.name)
        # Define municipal_buildings before using it
        municipal_buildings = [loc for loc in faction.region.locations if isinstance(loc, MunicipalBuilding)] if faction.region else []
        #print(f"Municipal buildings found: {municipal_buildings}")

        if municipal_buildings:
            MuniBuildings = municipal_buildings[0]
        elif faction.region.locations:
            MuniBuildings = faction.region.locations[0]

        # Confirm that MuniBuildings is valid before using it
        if MuniBuildings is None:
            raise ValueError(f"No valid locations found for faction: {faction.name} in region: {faction.region.name if faction.region else 'Unknown'}")

        vip = VIP(
        name=generate_name(None, random.choice(["Male", "Female"])),
        faction=faction,
        region=faction.region if faction.region else "Default Region",
        location=MuniBuildings,
        initial_motivations=["gain_elite"]
    )
        faction.state_staff.append(vip)  # Add to State object directly
        game_state.add_state_staff(vip)

        # Managers, Employees, and Taxmen
    for cls, count, motivations in [
        (Manager, random.randint(2, 3), ["influence"]),
        (Employee, random.randint(2, 3), ["influence"]),
        (Taxman, random.randint(2, 4), ["gain_money", "squeeze_taxes"])
    ]:
        for _ in range(count):
            staff = cls(
                name=generate_name(None, random.choice(["Male", "Female"])),
                faction=faction,
                region=faction.region,
                location=MuniBuildings,
                initial_motivations=motivations
            )
            faction.state_staff.append(staff)  # Add to State object directly
            game_state.add_state_staff(staff)

    # Police Stations with Fallback
    police_stations = [loc for loc in faction.region.locations if isinstance(loc, PoliceStation)]
    copshop = police_stations[0] if police_stations else faction.region.locations[0] if faction.region.locations else None

        # Police Station Staff
    for cls, count, motivations in [
        (RiotCop, random.randint(3, 5), ["earn_money", "enforce_law"]),
        (Detective, random.randint(1, 3), ["earn_money", "enforce_law"])
    ]:
        for _ in range(count):
            cop = cls(
                name=generate_name(None, random.choice(["Male", "Female"])),
                faction=faction,
                region=faction.region,
                location=copshop,
                initial_motivations=motivations
            )
            faction.state_staff.append(cop)
            game_state.add_state_staff(cop)

        characters.extend(faction.state_staff)  # Add staff to characters list.
    print(f"generate_faction_characters() executed, created {len(state_staff)} state characters")
    return characters

# Define location categories (if 'type' is not present in the Location class)
WORKPLACES = (Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalRepairWorkshop,
              Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe,
              Warehouse, ResearchLab, Museum, Library, SportsCentre, Holotheatre)
#These now refer to actual classes not strings.

#At some point you may need to import other locations listed below if they are handled as classes in logic.
PUBLIC_PLACES = (Museum, Library, SportsCentre, Holotheatre, Park, VacantLot)
RESIDENTIAL = (ApartmentBlock, House)


# Outside the function (global or passed in)
from faction import GeneralPopulation

general_population_faction = GeneralPopulation(name="General Population", violence_disposition="low")


def create_civilian_population(all_locations, all_regions, num_civilians=10):
    """Generate civilians and assign them logical locations."""
    civilians = []
    
    # Bias towards Terran by adding it more frequently
    valid_races = Character.VALID_RACES
    race_pool = ["Terran"] * 5 + [race for race in valid_races if race != "Terran"]
    
    # Categorize locations
    homes = [loc for loc in all_locations if isinstance(loc, RESIDENTIAL)]
    public_spaces = [loc for loc in all_locations if isinstance(loc, PUBLIC_PLACES)]
    
    for _ in range(num_civilians):
        race = random.choice(race_pool)
        gender = random.choice(["male", "female"])
        name = generate_name(race, gender)
        
        home = random.choice(homes) if homes else None
        public_place = random.choice(public_spaces) if public_spaces else None
        location = home if home else public_place
        
        region = next((r for r in all_regions if r.name == location.region), None) if location else None
        
        civilian = Civilian(
            name=name,
            region=region,
            location=location,
            race=race,
            faction=general_population_faction,
            initial_motivations=["earn_money", "have_fun", "find_partner"],
        )
        # 80% chance this civilian is an employee
        civilian.is_employee = random.random() < 0.8
        
        civilians.append(civilian)
        from create_game_state import get_game_state
        game_state = get_game_state()
        game_state.civilians.append(civilian)
        game_state.all_characters.append(civilian)
    
    return civilians

def assign_workplaces(civilians, all_locations):
    """Assigns workplaces to civilians, prioritizing shops."""
    workplaces = [loc for loc in all_locations if isinstance(loc, tuple(WORKPLACES))]
    shop_instances = [loc for loc in workplaces if isinstance(loc, Shop)]
    shop_index = 0  # Ensures round-robin assignment to shops

    #Instead of using the actual workplace object as a dictionary key, you can use its unique id() (or its .name if those are unique).
    workplace_counts = {id(place): 0 for place in workplaces}  # Use unique ID as key

    for civilian in civilians:
        correct_workplace = None

        if civilian.is_employee:
            if shop_instances:
                # Assign employees in order to shops first
                correct_workplace = shop_instances[shop_index % len(shop_instances)]
                shop_index += 1  # Move to next shop in order
            elif workplaces:
                correct_workplace = random.choice(workplaces)

            if correct_workplace:
                correct_workplace.employees_there.append(civilian)
                civilian.workplace = correct_workplace
                workplace_counts[id(correct_workplace)] += 1
                print(f"✅ DEBUG: Assigned {civilian.name} to {correct_workplace.name} in {correct_workplace.region}")
            else:
                print(f"⚠️ WARNING: No available workplaces for {civilian.name}")

    return civilians


def create_all_characters(factions, all_locations, all_regions, faction):
    print("\n" * 3)  # Line breaks for clarity
    print("create_all_characters() is about to run")
    #does this run twice? The print runs thrice
    all_characters = []
   
    new_characters = generate_faction_characters(faction, all_regions, all_locations)

    #print(f"✅ Finished {faction.name}, generated {len(new_characters)} characters")
    all_characters.extend(new_characters)

    civilians = create_civilian_population(all_locations, all_regions)
    assign_workplaces(civilians, all_locations) #I added a call here
    all_characters.extend(civilians)

    return all_characters


def player_character_options(all_regions, factions) -> list:
    print("Checking available regions and factions...")
    # Ensure we get a valid Corporation
    from faction import Corporation, Gang

    available_corporations = [faction for faction in factions if isinstance(faction, Corporation)]
    if not available_corporations:
        raise ValueError("No corporation factions available!")

    available_gangs = [faction for faction in factions if isinstance(faction, Gang)]
    if not available_gangs:
        raise ValueError("No corporation factions available!")
    
    selected_faction = random.choice(available_corporations)  # Pick one at random

from base_classes import Character
def select_character_menu():
    """Displays character selection and returns the selected character and their region."""
    from character_creation_funcs import player_character_options
    from display import show_character_details
    from create import all_regions, factions
    from base_classes import Character
    character_options = player_character_options(all_regions, factions)

    if not character_options:
        print("No characters available for selection.")
        return None, None

    # Display character choices
    print("\nSelect a character:")
    for idx, char_data in enumerate(character_options, start=1):
        print(f"{idx}. {char_data['name']} {char_data['Class'].name}")

    # Player selects a character
    while True:
        try:
            choice = int(input("Enter the number of your chosen character: ")) - 1
            if 0 <= choice < len(character_options):
                char_data = character_options[choice]
                selected_character = Character(
                    name=char_data["name"],
                    #their class name
                )
                selected_character.is_player = True
                global current_character  # Declare global to use it in other modules
                current_character = selected_character

                #I had to add this line to make it be defined:
                character = selected_character
                print(f"🔴🔴DEBUG: {character.name} location.name = {character.location.name}")
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Show character details
    show_character_details(selected_character)

    return selected_character, selected_character.region


def player_character_options(all_regions, factions):
    """Return a list of dictionaries with character info instead of full objects."""
    # Define character options as data dictionaries
    character_data = [
        {"class": Manager, "name": "Karen"},
        {"class": GangMember, "name": "Swiz"}
    ]

    return character_data
    
def instantiate_character(char_data, all_regions, factions):
    from create_game_state import get_game_state
    game_state = get_game_state()    
    if game_state is None:
        print("ERROR: game_state is not initialized!")

    """Instantiate the selected PLAYER character with relevant data."""
    from utils import get_faction_by_name, get_region_by_name, get_location_by_name  # Assuming they exist

    # Dynamically retrieve factions, regions, and locations
    faction = get_faction_by_name("Hannival" if char_data["name"] == "Karen" else "White Gang", factions)
    region = get_region_by_name("Downtown" if char_data["name"] == "Karen" else "Easternhole", all_regions)
    location = get_location_by_name("Municipal Building" if char_data["name"] == "Karen" else "Stash", all_regions)
    if location is None:
        print(f"Warning: Could not find specified location for {char_data['name']}. Defaulting to region center.")
        location = region.locations[0] if region.locations else None

    
    character = char_data["class"](
        name=char_data["name"],
        faction=faction,
        region=region,
        location=location,
        bankCardCash=500 if char_data["name"] == "Karen" else 50,
        fun=1,
        hunger=3
    )
    
    game_state.player_character = character  # Set the instantiated character as the player character
    return character


    