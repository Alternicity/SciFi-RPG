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
from visual_effects import loading_bar, RED, color_text
from typing import List, Dict, Union
import os

from character_creation_funcs import create_all_characters
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(message)s"
)
DEBUG_MODE = False  # Set to True when debugging

def create_object(data):
    pass
    
def create_regions():
    from create_game_state import get_game_state  # Keep this if needed
    from createLocations import create_locations
    from location import Region, Shop
    #global game_state  
    # Ensure Python uses the global game_state

    game_state = get_game_state()

    region_names = ["NorthVille", "SouthVille", "Easternhole", "Westborough", "Downtown"]

    wealth_map = {
        "NorthVille": "Normal",
        "Easternhole": "Poor",
        "Westborough": "Rich",
        "SouthVille": "Normal",
        "Downtown": "Rich",
    }

    all_regions = []
    
    for region_name in region_names:
        try:
            wealth = wealth_map.get(region_name, "Normal")
            
            region_obj = Region(
                name=region_name,
                shops=[],
                locations=[],
                factions=[],
                danger_level=None
            )
            all_regions.append(region_obj)

        except Exception as e:
            print(f"Error creating Region object for '{region_name}': {e}")

    # 🔁 Now populate each region with locations
    for region in all_regions:
        try:
            location_list = create_locations(region_obj, wealth)

            region.locations = location_list
            region.shops = [loc for loc in location_list if isinstance(loc, Shop)]

            # 🔗 Set the region reference on each location
            for loc in location_list:
                loc.region = region

        except Exception as e:
            print(f"❌ Error creating locations for region '{region.name}': {e}")

    # 📦 Save to game_state
    game_state.all_regions = all_regions
    return all_regions   

def create_gang_factions(num_gangs, all_regions):
    from create_game_state import get_game_state
    game_state = get_game_state()
    gangs = []
    VALID_RACES = Character.VALID_RACES  # Access from the from the class

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
        assigned_region = random.choice(all_regions)
        gang_name = f"{random.choice(first_part)} {random.choice(second_part)}"
        gang = Gang(name=gang_name, violence_disposition="High", race=race)
        gang.region = assigned_region  # Assign region before adding to list
        gangs.append(gang)
        game_state.add_gang(gang)  # Add to global GameState
        assigned_region.region_gangs.append(gang)  # Update region's gang list
        assign_hq(gang, assigned_region)
        #assign Boss
        # Assign a random goal
        random_goal_type = random.choice(Goal.VALID_GOALS)
        goal_description = f"{gang.name} aims to {random_goal_type.replace('_', ' ')}."
        gang.goals.append(Goal(description=goal_description, goal_type=random_goal_type))


    return gangs

def create_corp_factions(num_corps, all_regions):
    from create_game_state import get_game_state
    game_state = get_game_state()

    corporations = []
    
    CORP_NAMES_FILE = get_corp_names_filepath()
    if os.path.exists(CORP_NAMES_FILE):
        first_parts, second_parts = load_corp_names(CORP_NAMES_FILE)
    else:
        first_parts, second_parts = ["Default"], ["Corporation"]

    hannival_region = random.choice(all_regions)
    hannival_corp = Corporation(name="Hannival", violence_disposition="Medium")
    hannival_corp.region = hannival_region
    assign_hq(hannival_corp, hannival_region)
    corporations.append(hannival_corp)

    game_state.add_corporation(hannival_corp)
    hannival_region.region_corps.append(hannival_corp)

    for _ in range(num_corps):
        corp_name = f"{random.choice(first_parts).replace(',', '')} {random.choice(second_parts).replace(',', '')}"
        assigned_region = random.choice(all_regions)

        corporation = Corporation(name=corp_name, violence_disposition="Low")
        corporation.region = assigned_region

        # **Check if it already has an HQ before assigning**
        if corporation.HQ is None:
            assign_hq(corporation, assigned_region)

        corporations.append(corporation)
        game_state.add_corporation(corporation)
        
        assigned_region.region_corps.append(corporation)
        assign_hq(corporation, assigned_region)
        if DEBUG_MODE:
            print(f"DEBUG: Created Corporation - {corporation.name}")
        
    return corporations


#tmpPrint
""" def print_sample_characters_wallets(factions):
    print("\n=== Sample Characters and Wallets ===")
    for faction in factions:
        print(f"\nFaction: {faction.name}")
        seen_classes = set()

        for character in faction.members:
            class_name = character.__class__.__name__
            if class_name not in seen_classes:
                seen_classes.add(class_name)
                print(f" - {character.name} ({class_name}): Cash = {character.wallet.cash}, BankCard = {character.wallet.bankCardCash}")
 """

def create_factions(all_regions, all_locations):
    from create_game_state import get_game_state
    game_state = get_game_state()
    #print(f"create_factions() called from {__name__}")

    #print("all_regions content:", [region.name for region in all_regions])
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
    state.region = downtown_region #I added this spontaneously, while on an epic coffee crash
    game_state.set_state(state)
    factions.append(state)
    #print(f"[DEBUG] Added faction: {state.name} with region {state.region.name}")

    # Debugging: Check what create_gang_factions() returns before extending factions
    gang_factions = create_gang_factions(10, all_regions)
    factions.extend(gang_factions)

    for faction in gang_factions:
        if faction.type == "Gang":
            print(f"- {faction.name} (Region: {faction.region}) ({faction.type}) ({faction.resources})")
            factions.extend(gang_factions) #keep?

    from base_classes import Faction
    factionless = Faction("Factionless", "independent")
    factions.append(factionless) #factionless characters not present in new output print

    corp_factions = create_corp_factions(10, all_regions)
    factions.extend(corp_factions)

    all_characters = create_all_characters(factions, all_locations, all_regions)
    #print(f"create_all_characters() called from {__name__}")
    #print(f"✅ Total characters created: {len(all_characters)}")


    
    #print_sample_characters_wallets(factions)
    #verbose output


    return factions, all_characters

def create_HQ(region, faction_type="gang"):
    """Dynamically creates an HQ for a faction in a given region."""
    hq_name = f"{region.name} {'Corporate' if faction_type == 'corporate' else 'Gang'} HQ"
    new_hq = HQ(name=hq_name, region=region)
    
    #print(f"Created new {faction_type} HQ: {hq_name} in {region.name}")
    return new_hq #this var appears unused?

def assign_hq(faction, region):
    from create_game_state import get_game_state
    game_state = get_game_state()

    if faction.HQ is not None:  # ✅ Prevent multiple HQ assignments
        #print(f"{faction.name} already has an HQ in {faction.HQ.region.name}.")
        return  # Exit the function early
    
    if isinstance(faction, Corporation):
        hq_name = f"{faction.name} Corporate HQ"
    else:
        hq_name = f"{faction.name} HQ"  # Gangs get a generic HQ name

    available_hqs = [loc for loc in region.locations if isinstance(loc, HQ) and loc.faction is None]
    
    # If the faction is a corporation, ensure it gets an HQ
    if isinstance(faction, Corporation) and not available_hqs:
        #print(f"No available HQ for {faction.name}. Creating one.")
        new_hq = create_HQ(region, faction_type="corporate")
        region.locations.append(new_hq)
        available_hqs.append(new_hq)

    if available_hqs: 
        hq = random.choice(available_hqs)
        hq.faction = faction
        hq.name = f"{faction.name} HQ"  # Update HQ name
        faction.HQ = hq  # Update faction's HQ attribute
        #print(f"{faction.name} HQ assigned: in {region.name}")
        
    
    else:
        faction.is_street_gang = True
        
        region.region_street_gangs.append(faction)
        game_state.all_street_gangs.append(faction)

        if not any(goal.goal_type == "acquire HQ" for goal in faction.goals):
            faction.set_goal(Goal(description="Acquire an HQ", goal_type="acquire HQ"))
        
        #if there are > a threshhold of gangs in one region, this could trigger a game event "turf war"
        # Turf War Trigger
          # Example threshold
            
            street_gang_count = len(region.region_street_gangs)

            if street_gang_count > 3 and not region.turf_war_triggered:  # Prevent repeated triggers
                print(f"{street_gang_count} street gangs present in {region.name}, without HQs. {color_text('Turf war brewing!', RED)}")
                region.trigger_event("turf_war")
                region.turf_war_triggered = True
                






