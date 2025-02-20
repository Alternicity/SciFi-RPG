#create.py
import logging
from pathlib import Path

from loader import load_gang_names, get_gang_names_filepath, get_corp_names_filepath, load_corp_names
from base_classes import Location, Character
from location import Shop, CorporateStore, Stash, Region, UndevelopedRegion, VacantLot, HQ, MunicipalBuilding
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, GangMember, Child, Influencer,
                           Babe, Detective)
from faction import Corporation, Gang, State
from goals import Goal
from location_security import Security

from typing import List, Dict, Union
import os

from character_creation_funcs import create_all_characters
import random

from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(message)s"
)
DEBUG_MODE = False  # Set to True when debugging

def create_object(data):

    pass
    
def create_regions():
    """Create and return a list of Region objects with Locations inside them."""
    print("Initializing regions as objects...")

    region_wealth_levels = {
        "NorthVille": "Normal",
        "Easternhole": "Poor",
        "Westborough": "Rich",
        "SouthVille": "Normal",
        "Downtown": "Rich",
    }

    from createLocations import create_locations
    # Store region objects
    region_objects = []

    for region, wealth in region_wealth_levels.items():
        try:
            location_list = create_locations(region, wealth)  # Get Location objects
            #Are locations created twice, here and in main.py?

            region_obj = Region(
                name=region,
                shops=[loc for loc in location_list if isinstance(loc, Shop)],  # Extract Shops separately
                locations=location_list,  # Full list of Locations
                factions=[],
                DangerLevel=None,
            )
            #add each location to its region here, in its location_list setting its region attribute?
            #
            region_objects.append(region_obj)
            
        except Exception as e:
            print(f"Error creating region '{region}': {e}")

    return region_objects   

def create_gang_factions(num_gangs, all_regions):
    gangs = []
    VALID_RACES = Character.VALID_RACES  # Access the tuple from the class

    #GANG Race name lookup table
    RACE_NAME_LOOKUP = {
    "Terran": (["Druze", "Based", "Cringe", "Hell", "Incensed", "Nile", "Pain", "Rich", "Spiky", "Vengeful", "Weeping", "War", "Young", "Swooping", "Diving", "Septic", "Armoured", "Spamier", "Plastic", "Radioactive", "Trusty"], 
               ["Vipers", "Shadows", "Reapers", "Angels", "Devils", "Doubters", "Fifth", "Jokers", "Punishers", "StormPhags"]),
    "Chinese": (["Ribbon", "Honourable", "Bronze", "Gold", "Golden", "Silver", "Incense", "Magic"], 
                ["Sifus", "Makers", "Blades", "Cranes", "Masters", "Tong", "Wukongs", "Wangs", "Tzus", "Dragons"]),
    "French": (["Fromage", "Petits", "Grands", "Propres", "Rapides", "Grands", "Mauvais", "Fous", "Effrayants", "Ambitieux", "Ravis", "Vénimeux", "Premiers", "Attrayants", "Poilus"], 
               ["Poignards", "Pépites", "Dégringolades", "Bouquiners", "Farouches", "TractionsAvant", "BriseDeMer", "Zenvolasca", "Bonnot"]),
    "German": (["Aryan", "Gepanzert", "Jung", "Basierend", "Astfalon", "Fervir", "Stein", "Eisen", "Fortgeschritten", "Grundlegend", "Kaltherzig", "Wiederauflebend", "Fünfte", "Gotisch", "Fervir", "Zusammengebaut"], 
               ["Waffe", "Äxte", "Hämmer", "Ambrones", "Zweihanders", "Lehrer", "Nehmer", "Söhne", "Luftreiniger"]),

    "Indian": (["Republican", "Weeping", "War", "Whiter", "Mass", "Clean", "Lustful", "Plentiful", "Unrepentant"],
               ["Chakras", "Engineers", "GaleeShitars", "Lingams", "Operators", "Tigers", "Lookers", "GrahBans", "Hashishim"]),
    
    "IndoAryan": (["Sundaro", "Partisan", "Flowing", "Sundaro", "War", "Xen", "Sundaro", "Pure", "Intense", "Clean", "Observant", "Forgotten", "Unrepentant", "Striking", "Intense", "Avenging"],
                ["Swarm", "Hunters", "Chakr", "Injeeniyar", "Lingam", "Tigers", "Lookers", "GrahBans", "GrahBans"]),
    
    
    "IranianPersian": (["hezbi", "ravan", "jang", "Scaly", "shodid", "pak", "nazer", "faramush shodeh", "vafadar"], 
                       ["mobarzan", "manpandsan", "pasaran", "bebrehya", "garecbannpana", "nizemanteoja"]),
    "Irish": (["Dead", "TuathaDe", "XandG", "Wild", "Cruthin", "Erainn", "Loígis", "Sharp", "Misty", "Celtic", "Silver", "Based"], 
              ["Rabbits", "O'Mores", "O'Nolans", "O'Dorans", "O'Lawlors", "O'Dowlings", "DálRiata", "UiFidgenti", "Kings", "Lashers", "Dál Riata", "UiFidgenti"]),
    "Italian": (["Republican", "Imperial", "Genovese", "Vengeful", "Gambino", "Incendii", "Ophelian", "Milanii", "Scipione", "Lucchese", "Tempête", ""], 
                ["Mafia", "Nostra", "XIV", "XX", "V", "IV", "IX", "XIII", "Angeli", "Ragazzi", "Punitori"]),
    "Japanese": (["Crimson", "Shadow", "Eternal", "Inagawa", "muzukashii", "atsui", "warui", "atarashii", "kireina"], 
                 ["Bosozoku", "Tekiya", "Bakuto", "Yankii", "Umibozo", "Gokudō", "Lotus", "Brotherhood", "Fists"]),
    "Martian": (["Promethei", "Sabaea", "Xanthe", "Promethei", "Sabaea", "Tyrrhena", "Margaritifer", "Eudoxus", "Byalax"], 
                ["Aurigans", "Synths", "FreeBreathers", "DeCrux", "Draconians", "Hydrans", "Corvids", "Zodians", "Machines"]),
    "German": (["Aryan", "Armoured", "Xanthe", "Promethei", "Sabaea", "Tyrrhena", "Margaritifer", "Eudoxus", "Byalax"], 
                ["Aurigans", "Synths", "FreeBreathers", "DeCrux", "Draconians", "Hydrans", "Corvids", "Zodians", "Machines"]),
    "Portuguese": (["Mau", "Amargo", "Azul", "Proxima", "Cheio", "Vermelho", "Educado", "Velho", "Feral", "Grosso", "Doce"], 
                   ["Braços", "Gente", "Pessoas", "Dentes", "Caralhos", "Cervejas", "Tomarenses", "Problemas", "Misericordias", "Templarios", "Cabeças", "Punhals", "Bêbados"]),
    "WhiteAryanNordic": (["Aryan", "Armed", "Eternal", "Golden", "Winged", "Fanged", "Plastic", "Lysergic", "Swooping", "Lofty", "Sly", "Avenging"], 
                         ["Svears", "Geats", "Brits", "Trøndere", "Viken", "Gotere", "Tjust", "Angles", "Scylfing", "Völsung", "Wægmunding", "Sippe"]),

    "BlackAmerican": (["Black", "Tooled", "Drip", "Goated", "Angelic", "Fanged", "Plastic", "Eyeball", "Hooded", "Strapped", "Sly", "Value"], 
                         ["Crips", "Hits", "Hoods", "Seps", "XYZ", "Homies", "Dreads", "Sweeties", "Xtians", "Panthers", "Boyz", "Orphans"])
}
    for i in range(num_gangs):
        # Assign race, ensuring diversity for at least the first len(VALID_RACES) gangs
        race = VALID_RACES[i % len(VALID_RACES)]  # Cycles through available races
        
        # Generate gang name based on race
        race_specific_names = RACE_NAME_LOOKUP.get(race, (["Default"], ["Gang"]))
        first_part, second_part = race_specific_names

        gang_name = f"{random.choice(first_part)} {random.choice(second_part)}"
        
        gang = Gang(name=gang_name, violence_disposition="High", race=race)
        gangs.append(gang)

    return gangs

def create_corp_factions(num_corps, all_regions):
    """Generates and returns a list of corporation factions using names from a file."""
    corporations = []
    
    CORP_NAMES_FILE = get_corp_names_filepath()
    if os.path.exists(CORP_NAMES_FILE):
        first_parts, second_parts = load_corp_names(CORP_NAMES_FILE)
    else:
        first_parts, second_parts = ["Default"], ["Corporation"]

    
    hannival_corp = Corporation(name="Hannival", violence_disposition="Medium")
    corporations.append(hannival_corp)

    for _ in range(num_corps):
        corp_name = f"{random.choice(first_parts)} {random.choice(second_parts)}"
        corp = Corporation(name=corp_name, violence_disposition="Low")
        corporations.append(corp)

        if DEBUG_MODE:
            print(f"DEBUG: Created Corporation - {corp.name}")
        #print("Created Corporations:", [corp.name for corp in corporations])
    return corporations

def create_factions(locations, all_regions, location_objects):

    print("Creating factions as list...")

    factions = []  # Store created factions

    # Find Downtown region
    downtown_region = next((region for region in all_regions if region.name == "Downtown"), None)
    if not downtown_region:
        raise ValueError("Error: Downtown region not found in all_regions.")

    # Create the State faction
    state = State(
        name="Unified Government",
        resources={"money": 1000000},
        laws=["No theft", "Corporate tax"],
        region=downtown_region
    )
    factions.append(state)

    print("About to create factions with faction.extend...")
    # Create gangs and corporations separately
    factions.extend(create_gang_factions(10, all_regions))
    
    print("Just went past faction.extend(create_gang_factions")
    # Show Gang Objects here:
    print("Created Gang Factions:")
    for faction in factions:
        if faction.type == "Gang":
            print(f"- {faction.name} (Region: {faction.region} ) ({faction.type}) ({faction.reources})")

    # Debugging: Check what create_gang_factions() returns before extending factions
    gang_factions = create_gang_factions(10, all_regions)
    print("Returned from create_gang_factions:", gang_factions)  # Check if anything is returned

    factions.extend(create_corp_factions(10, all_regions))
    #these lines curently come after create_corp_factions() and create_gang_factions()
    #so does that mean they run twice?


    # Create all characters for these factions
    all_characters = create_all_characters(factions, locations, all_regions, location_objects)
    #marked for deletion?

    return factions, all_characters


def assign_hq(faction, region): #deos this get called?
    
    available_hqs = [loc for loc in region.locations if isinstance(loc, HQ) and loc.faction is None]
    
    if available_hqs: #does this iterate over the available HQs?
        hq = available_hqs[0]  # Assign the first available HQ
        hq.faction = faction
        hq.name = f"{faction.name} HQ"  # Update HQ name
        faction.HQ = hq  # Update faction's HQ attribute
        print(f"{faction.name} HQ assigned: {hq.name} in {region.name}")
        #now remove that HQ from available_hqs? We dont want it reassigned to another faction
    else:
        print(f"No available HQ for {faction.name} in {region.name}. Assigning 'acquire HQ' goal.")
        faction.add_goal(Goal(description="Acquire an HQ", goal_type="acquire HQ"))


from character_creation_funcs import create_all_characters
def create_characters(factions, locations, all_regions, location_objects): 
    #what is this function here for? 
    return create_all_characters(factions, locations, all_regions, location_objects)


def initialize_regions():
    #why does this function exist?
    return create_regions()

# Ensure all_regions is initialized only once
all_regions = initialize_regions()

# Extract locations from all regions
all_locations = [location for region in all_regions for location in region.locations]
for region in all_regions:
    all_locations.extend(region.locations)  # Collect all locations into one list


from createLocations import create_locations
#this import currently not accessed

# Extract location objects from the regions
location_objects = [location for region in all_regions for location in region.locations]
#chatGPT can you explain what this line is doing?

#adding location_objects here causes a highly verbose program output
factions, all_characters = create_factions(all_locations, all_regions, location_objects)


# create_character is only called here!
#commented out for testing
#all_characters = create_characters(factions, all_locations, all_regions, location_objects)



