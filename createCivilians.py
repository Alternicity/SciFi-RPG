from faction import GeneralPopulation
import random
from base_classes import Character
from location import Shop, Region
from location_types import WORKPLACES, PUBLIC_PLACES, RESIDENTIAL
from faction import GeneralPopulation
from characters import Civilian
from InWorldObjects import Wallet
from motivation_presets import MotivationPresets

general_population_faction = GeneralPopulation(name="General Population", violence_disposition="low")

from utils import normalize_location_regions
def create_civilian_population(all_locations, all_regions, num_civilians=10):
    """Generate civilians and assign them logical locations."""
    from create_character_names import create_name
    from utils import get_region_for_location

    normalize_location_regions(all_locations, all_regions)  # 🧹 Ensure valid region refs

    civilians = []
    valid_races = Character.VALID_RACES
    race_pool = ["Terran"] * 5 + [race for race in valid_races if race != "Terran"]
    
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
        #print("📜 All known regions:")
        for reg in game_state.all_regions:
            #print(f" - {reg.name}")
            pass
        
        region = get_region_for_location(location, all_regions)

        random_cash = random.randint(5, 500)

        if region is None:
            print(f"⚠️🟣🟣 No matching region found for location: {location.name} with region = {location.region}")
            continue  # Skip this civilian creation if region is invalid
        else:
            #print(f"✅🟣🟣 Region resolved: {region.name} for location {location.name}")
            pass

        civilian = Civilian(
            name=name,
            region=region,
            location=location,
            race=race,
            faction=general_population_faction,
            initial_motivations=MotivationPresets.for_class("Civilian"),
            wallet=Wallet(bankCardCash=random_cash),
        )
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
                #print(f"Assigned {civilian.name} to {correct_workplace.name} in {correct_workplace.region}")
            else:
                print(f"⚠️ WARNING: No available workplaces for {civilian.name}")

    return civilians