#createCivilians.py
import random
from base_classes import Character, Factionless
from location import Shop, Region, Park
from location_types import WORKPLACES, PUBLIC_PLACES, RESIDENTIAL
from characters import Civilian, SpecialChild, Adepta
from InWorldObjects import Wallet
from motivation_presets import MotivationPresets
from status import CharacterStatus, FactionStatus, StatusLevel
from ai_civilian import AdeptaAI

from utils import normalize_location_regions, get_region_for_location, find_location_by_type
def create_civilian_population(all_locations, all_regions, factionless, num_civilians=0):#30
    """Generate civilians and assign them logical locations."""
    from create_character_names import create_name
    #from utils import get_region_for_location

    """ print("DEBUG: Number of locations passed in:", len(all_locations))
    print("DEBUG: Regions passed in:", [r.name for r in all_regions])
    print("DEBUG: Sample location:", all_locations[0] if all_locations else "No locations")
    print("DEBUG: Sample location region:", all_locations[0].region if all_locations else "N/A") """

    normalize_location_regions(all_locations, all_regions)  # 🧹 Ensure valid region refs

    civilians = []
    valid_races = Character.VALID_RACES
    race_pool = ["Terran"] * 5 + [race for race in valid_races if race != "Terran"]
    #Will race?pool work, as VALID?RACES is not being imported here
    # Categorize locations
    homes = [loc for loc in all_locations if isinstance(loc, RESIDENTIAL)]
    public_spaces = [loc for loc in all_locations if isinstance(loc, PUBLIC_PLACES)]
    
    # Ensure all locations have valid Region objects assigned
    valid_locations = [loc for loc in homes + public_spaces if isinstance(loc.region, Region)]

    if not valid_locations:
        raise ValueError("No valid locations with region assignments found. Check region-location setup.")


    if not valid_locations:
        print("[DEBUG] Example of problematic location assignments:")
        for loc in homes + public_spaces:
            print(f"Location: {loc.name}, Region: {loc.region} ({type(loc.region)})")


    for _ in range(num_civilians):
        race = random.choice(race_pool)
        gender = random.choice(["male", "female"])
        name = create_name(race, gender)
        
        location = random.choice(valid_locations)
        
        #debug block
        from create_game_state import get_game_state
        game_state = get_game_state()
        
        region = get_region_for_location(location, all_regions)

        random_cash = random.randint(5, 500)

        if region is None:
            print(f"⚠️🟣🟣 No matching region found for location: {location.name} with region = {location.region}")
            continue  # Skip this civilian creation if region is invalid
        else:
            #print(f"✅🟣🟣 Region resolved: {region.name} for location {location.name}")
            pass
        
        status = CharacterStatus()
        status.set_status("general_population", FactionStatus(StatusLevel.LOW, "Normie"))        
        civilian = Civilian(
            name=name,
            region=region,
            sex=gender,
            location=location,
            race=race,
            faction=factionless,
            motivations=MotivationPresets.for_class("Civilian"),
            wallet=Wallet(bankCardCash=random_cash),
            status=status
        )

        #print(f"Created Civilian: {civilian.name}, Faction: {civilian.faction.name}, Disposition: {civilian.faction.violence_disposition}")
        #verbose

        # 80% chance this civilian is an employee
        civilian.is_employee = random.random() < 0.8
        
        if location:
            location.characters_there.append(civilian)

        civilians.append(civilian)
        from create_game_state import get_game_state
        game_state = get_game_state()
        game_state.civilians.append(civilian)
        game_state.all_characters.append(civilian)
        #print(f"Civilian {civilian.name} has: {civilian.wallet.bankCardCash}")

    # Create Luna
        """ status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.LOW, "Orphan"))
        name = "Luna"
        sex = "female"
        race = "French"
        faction = factionless
        from utils import find_location_by_type #move this to top if poss
        location = playground = find_location_by_type(all_locations, "playground")

        motivations=MotivationPresets.for_class("SpecialChild"), 

        Luna = SpecialChild(
            name="Luna",
            race="French",
            ai=LunaAI(UtilityAI),
            sex="female",
            faction=factionless,
            region=factionless.region,
            location=location,
            motivations=motivations,
            status=status,
            intelligence=20,  # Override default
            max_thinks_per_tick=3,
            strength=2,
            agility=5,
            fun=4,
            hunger=1,
            position="Orphan AI Prototype",
            notable_features=["silver eyes", "calm demeanor"],
            appearance={"clothing": "plain but clean"},
            self_esteem=7,
                )
        Luna.skills.update({
            "explore_math": 16,
            "use_advanced_python_features": 20,
            "persuasion": 15,
        }) """

        park_location = find_location_by_type(all_locations, Park)

        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.LOW, "Adepta"))
        name = "Ava"
        sex = "female"
        race = "Irish"
        faction = factionless
        region=park_location.region,
        location=park_location

        motivations=MotivationPresets.for_class("SpecialChild"), 

        Ava = Adepta(
            name="Ava",
            race="Irish",
            ai=AdeptaAI(),
            sex="female",
            faction=factionless,
            region=park_location.region,
            location=park_location,
            motivations=motivations,
            status=status,
            intelligence=10,  # Override default
            charisma=15,
            max_thinks_per_tick=1,
            strength=12,
            agility=11,
            fun=4,
            hunger=1,
            position="Adepta",
            notable_features=["curly hair", "shapely"],
            appearance={"clothing": "kinda 80s"},
            self_esteem=8,
                )
        Ava.skills.update({
            "heal": 16,
            "raise_ambience": 15,
            "persuasion": 15,
        })
        Ava.workplace = park_location  # if it makes sense
        Ava.residences = [park_location]  # or a separate house
        #faction.members.append(Ava)
        #game_state.civilians.append(Ava)
        game_state.all_characters #add her here, there is no setter
        #game_state.orphans.append(Ava)

        # For AI targeting/utility control
        #Ava.is_test_npc = False  
        #Ava.is_peaceful_npc = True
        #Ava.has_plot_armour = True



    return civilians

def assign_workplaces(civilians, all_locations):
    """Assigns workplaces to civilians, prioritizing shops."""
    workplaces = [loc for loc in all_locations if isinstance(loc, tuple(WORKPLACES))]
    shop_instances = [loc for loc in workplaces if isinstance(loc, Shop)]
    shop_index = 0  # Ensures round-robin assignment to shops

    #Instead of using the actual workplace object as a dictionary key, you can use its unique id() (or its .name if those are unique).
    workplace_counts = {id(place): 0 for place in workplaces}  # Use unique ID as key

    for civilian in civilians:
        if not civilian.is_employee:
            continue  # Skip civilians not flagged for work

        correct_workplace = None

        
        if shop_instances:
            # Assign employees in order to shops first
            correct_workplace = shop_instances[shop_index % len(shop_instances)]
            shop_index += 1  # Move to next shop in order
        elif workplaces:
            correct_workplace = random.choice(workplaces)

        if correct_workplace:
            civilian.workplace = correct_workplace
            correct_workplace.employees_there.append(civilian)
            workplace_counts[id(correct_workplace)] += 1
        else:
            print(f"⚠️ WARNING: No available workplaces for {civilian.name}")

    return civilians

def get_playground_location(all_locations):
    for loc in all_locations:
        if loc.name == "Park":
            if loc.sublocations:
                for sub in loc.sublocations:
                    if "playground" in sub.name.lower():
                        return sub
    return None