#create.create.py
import logging
from pathlib import Path


from loader import get_corp_names_filepath, load_corp_names
from base.character import  Character
from base.location import Location
from location.locations import Shop, CorporateStore, Stash, Region, VacantLot, HQ, MunicipalBuilding
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, GangMember, Child, Influencer,
                           Babe, Detective)
from faction import Corporation, Gang, State
from goals import Goal
from location.location_security import Security #greyed, not access currently
from visual_effects import loading_bar, RED, color_text
from typing import List, Dict, Union
import os
from display import display_sellers
from character_creation_funcs import create_all_characters
import random
from debug_utils import debug_print
from region.region_flavor import REGION_CULTURAL_ADJECTIVES
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(message)s"
)


def create_object(data):
    pass
    
def create_regions():
    from create.create_game_state import get_game_state
    from create.createLocations import create_locations
    from location.locations import Shop#now outdated, why is this here, but it is seemingly accessed, so deserve a look
    from display import debug_display_all_shops


    game_state = get_game_state()

    region_names = ["northville", "southville", "easternhole", "westborough", "downtown"]

    wealth_map = {
        "northville": "Normal",
        "easternhole": "Poor",
        "westborough": "Rich",
        "southville": "Normal",
        "downtown": "Rich",
    }

    all_regions = []
    all_locations = []
    for region_name in region_names:
        try:
            wealth = wealth_map.get(region_name, "Normal")
            
            region_obj = Region(
                name=region_name.lower().replace(" ", ""),
                name_for_player=region_name,
                shops=[],
                locations=[],
                factions=[],
                danger_level=None,
                cultural_adjectives=list(
                    REGION_CULTURAL_ADJECTIVES.get(region_name, [])
                ),
            )
            all_regions.append(region_obj)
            game_state.all_regions.append(region_obj)
            
        except Exception as e:
            print(f"Error creating Region object for '{region_name}': {e}")

    # 🔁 Now populate each region with locations
    for region in all_regions:
        try:
            # Use the correct wealth for this region (pull from wealth_map using region.name)
            region_wealth = wealth_map.get(region.name, "Normal")
            location_list = create_locations(region, region_wealth)

            if not location_list:
                debug_print(
                    None,
                    f"[CREATE] Warning: create_locations returned 0 locations for region {region.name} (wealth={region_wealth}).",
                    category="create"
                )

            region.locations = location_list
            region.shops = [loc for loc in location_list if isinstance(loc, Shop)]

            # Set region ref on each location
            for loc in location_list:
                loc.region = region

            # Add into global flat list
            all_locations.extend(location_list)

            # 🔍 INSERT DIAGNOSTICS HERE
            #debug_print("system", f"\n[DEBUG] Region {region.name} locations (identity check):", category = "create")
            #muted for brevity

            for loc in location_list:
                pass
                #verbose
                #debug_print("system", f"  id={id(loc)}  name={loc.name}  region={loc.region.name}", category = "create")

        except Exception as e:
            debug_print(
                npc=None,
                message=f"⚠️ Error creating locations for region '{region.name}': {e}",
                category="create"
            )
    total_locations = sum(len(r.locations) for r in all_regions)
    #debug_print(None, f"[CREATE] Created {len(all_regions)} regions and {total_locations} locations total.", category="create")

    

    # 📦 Save to game_state
    game_state.all_regions = all_regions
    game_state.all_locations = all_locations
    return all_regions, all_locations

def create_gang_factions(num_gangs, all_regions):
    from create.create_game_state import get_game_state
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
        region_name = assigned_region.name.replace(" ", "")
        attr_name = f"{region_name}_gangs"
        gang_name = f"{random.choice(first_part)} {random.choice(second_part)}"
        gang = Gang(name=gang_name, violence_disposition="5", race=race)
        gang.region = assigned_region  # Assign region before adding to list
        gangs.append(gang)
        game_state.add_gang(gang)  # Add to global GameState

        assigned_region.region_gangs.append(gang)  # Local region tracking

        # Dynamically update the correct GameState list
        attr_name = f"{region_name}_gangs"
        if hasattr(game_state, attr_name):
            getattr(game_state, attr_name).append(gang)
        else:
            print(f"[Warning] GameState has no attribute '{attr_name}'")

                # Update region's gang list

        assign_hq(gang, assigned_region)
        
        #assign Boss
        # Assign a random goal
        random_goal_type = random.choice(Goal.VALID_GOALS)
        goal_description = f"{gang.name} aims to {random_goal_type.replace('_', ' ')}."
        gang.goals.append(Goal(description=goal_description, goal_type=random_goal_type))

    return gangs

def create_corp_factions(num_corps, all_regions):
    from create.create_game_state import get_game_state
    game_state = get_game_state()

    corporations = []
    
    CORP_NAMES_FILE = get_corp_names_filepath()
    if os.path.exists(CORP_NAMES_FILE):
        first_parts, second_parts = load_corp_names(CORP_NAMES_FILE)
    else:
        first_parts, second_parts = ["Default"], ["Corporation"]

    hannival_region = random.choice(all_regions)
    hannival_corp = Corporation(name="Hannival", violence_disposition="2")
    hannival_corp.region = hannival_region
    assign_hq(hannival_corp, hannival_region)
    corporations.append(hannival_corp)

    game_state.add_corporation(hannival_corp)

    hannival_region.region_corps.append(hannival_corp)
    #also I must  update game_states self.corporations list and all_locations, and also
    # the correct game_state.xyz_corps list here

    region_name = hannival_region.name.replace(" ", "")
    attr_name = f"{region_name}_corps"

    if hasattr(game_state, attr_name):
        getattr(game_state, attr_name).append(hannival_corp)
    else:
        print(f"[Warning] GameState has no attribute '{attr_name}'")


    for _ in range(num_corps):
        corp_name = f"{random.choice(first_parts).replace(',', '')} {random.choice(second_parts).replace(',', '')}"
        assigned_region = random.choice(all_regions)

        corporation = Corporation(name=corp_name, violence_disposition="2")
        corporation.region = assigned_region

        region_name = assigned_region.name.replace(" ", "")
        attr_name = f"{region_name}_corps"

        if hasattr(game_state, attr_name):
            getattr(game_state, attr_name).append(corporation)
        else:
            print(f"[Warning] GameState has no attribute '{attr_name}'")

        # **Check if it already has an HQ before assigning**
        if corporation.HQ is None:
            assign_hq(corporation, assigned_region)
            if corporation.HQ:
                corporation.HQ.controlling_faction = corporation #needs checking. Should this be in assign_hq?

        corporations.append(corporation)
        game_state.add_corporation(corporation)
        
        assigned_region.region_corps.append(corporation)
        assign_hq(corporation, assigned_region)
        
        
    return corporations


def create_factions(all_regions, all_locations):
    from create.create_game_state import get_game_state
    game_state = get_game_state()
    #print(f"create_factions() called from {__name__}")

    #print("all_regions content:", [region.name for region in all_regions])
    factions = []  # Store created factions

    # Find downtown region
    downtown_region = next((region for region in all_regions if region.name == "downtown"), None)
    if not downtown_region:
        raise ValueError("Error: downtown region not found in all_regions.")

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
        if faction.type.lower() == "gang":
            faction.is_vengeful = True  # ✅ gangs are aggressive by default
        else:
            faction.is_vengeful = False

    from base.faction import Faction, Factionless
    factionless = Factionless(name="Factionless", violence_disposition="1")
    factionless.region = downtown_region
    factions.append(factionless)

    corp_factions = create_corp_factions(10, all_regions)
    factions.extend(corp_factions)

    all_characters = create_all_characters(factions, all_locations, all_regions)

    #tmp - prints what gang members are present in their HQ
    """ print("[DEBUG] Gang Member Spawn Check:")
    for gang in game_state.gangs:
        hq = gang.HQ
        hq_list = [c.name for c in getattr(hq, "characters_there", [])] if hq else []
        print(f"\nGang: {gang.name}")
        print(f"  HQ: {hq.name if hq else 'None'}")
        print(f"  HQ.characters_there: {hq_list}")

        for m in gang.members:
            print(f"    Member: {m.name}  | location={m.location.name if m.location else None}") """



    return factions, all_characters

def create_HQ(region, faction_type="gang"):
    """Dynamically creates an HQ for a faction in a given region."""
    hq_name = f"{region.name} {'Corporate' if faction_type == 'corporate' else 'Gang'} HQ"
    new_hq = HQ(name=hq_name, region=region)
    
    #print(f"Created new {faction_type} HQ: {hq_name} in {region.name}")
    return new_hq #this var appears unused?

def assign_hq(faction, region):
    from create.create_game_state import get_game_state
    game_state = get_game_state()

    #Not all gang factions successfully get an HQ
    

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
        #the problem with adding it to these lists is they are not named yet
        #add it to all_locations, which is not yet present here
        #add it to game_state.all_locations

        available_hqs.append(new_hq)

    if available_hqs: 
        hq = random.choice(available_hqs)
        hq.faction = faction
        hq.name = f"{faction.name} HQ"
        faction.HQ = hq

        #so appending to lists/register should happen here?
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
                
#create new factions
def create_gang(game_state, gang, is_street_gang=True):
    region_name = gang.region.name.lower().replace(" ", "")
    
    # Add to global gang list
    game_state.add_gang(gang)
    
    # Add to region-specific list
    gang.region.region_gangs.append(gang)

    # Add to GameState region list dynamically
    attr_name = f"{region_name}_gangs"
    if hasattr(game_state, attr_name):
        getattr(game_state, attr_name).append(gang)
    else:
        print(f"[Warning] GameState has no attribute '{attr_name}'")

    # Optional: store street gang info if needed
    gang.is_street_gang = is_street_gang

def destroy_gang(game_state, gang):
    region_name = gang.region.name.lower().replace(" ", "")
    
    # Remove from global list
    if gang in game_state.gangs:
        game_state.gangs.remove(gang)

    # Remove from region-specific list
    if gang in gang.region.region_gangs:
        gang.region.region_gangs.remove(gang)

    # Remove from GameState region list
    attr_name = f"{region_name}_gangs"
    if hasattr(game_state, attr_name):
        region_list = getattr(game_state, attr_name)
        if gang in region_list:
            region_list.remove(gang)

def create_corporation(game_state, corp):
    region_name = corp.region.name.lower().replace(" ", "")
    
    game_state.add_corporation(corp)
    corp.region.region_corps.append(corp)

    attr_name = f"{region_name}_corps"
    if hasattr(game_state, attr_name):
        getattr(game_state, attr_name).append(corp)
    else:
        print(f"[Warning] GameState has no attribute '{attr_name}'")


def destroy_corporation(game_state, corp):
    region_name = corp.region.name.lower().replace(" ", "")
    
    if corp in game_state.corporations:
        game_state.corporations.remove(corp)
    if corp in corp.region.region_corps:
        corp.region.region_corps.remove(corp)

    attr_name = f"{region_name}_corps"
    if hasattr(game_state, attr_name):
        region_list = getattr(game_state, attr_name)
        if corp in region_list:
            region_list.remove(corp)
