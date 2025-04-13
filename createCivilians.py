from faction import GeneralPopulation
import random
from base_classes import Character
from location import Shop
from location_types import WORKPLACES, PUBLIC_PLACES, RESIDENTIAL
from faction import GeneralPopulation
from characters import Civilian
general_population_faction = GeneralPopulation(name="General Population", violence_disposition="low")

def create_civilian_population(all_locations, all_regions, num_civilians=10):
    """Generate civilians and assign them logical locations."""
    from create_character_names import create_name
    civilians = [] # other createXYZFaction functions use local characters = [], the intention is to aggregate them in
    #create_character_funcs.py. Dont forget to also add civilians = [] to this (and update game_state)
    # Bias towards Terran by adding it more frequently
    valid_races = Character.VALID_RACES
    race_pool = ["Terran"] * 5 + [race for race in valid_races if race != "Terran"]
    
    # Categorize locations
    homes = [loc for loc in all_locations if isinstance(loc, RESIDENTIAL)]
    public_spaces = [loc for loc in all_locations if isinstance(loc, PUBLIC_PLACES)]
    
    for _ in range(num_civilians):
        race = random.choice(race_pool)
        gender = random.choice(["male", "female"])
        name = create_name(race, gender)
        
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