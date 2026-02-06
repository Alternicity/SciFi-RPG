#create.create_character_names.py
from common import BASE_CHARACTERNAMES_DIR
import random
import os
from loader import load_names_from_csv
from get_valid_races import get_valid_races
from create.create_game_state import get_game_state

def create_name(race, sex):#npc or character or member cannot be passed in due to earlier logic

    """Generate a full name based on race and sex."""
    game_state = get_game_state()
    valid_races = get_valid_races()

    # If no race is provided, choose one randomly from valid races
    if race is None:#are we actually matching to the npcs race? 
        raise ValueError("create_name() called with race=None. This is not allowed for gangs.")
    if race not in valid_races:
        raise ValueError(f"Invalid race '{race}'. Must be one of: {valid_races}")
    
    filepath = os.path.join(BASE_CHARACTERNAMES_DIR, f"{race}Names.txt")

    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found! {filepath}")
        return "Unknown Unknown"

    male_names, female_names, family_names = load_names_from_csv(filepath)
    

    if sex.lower() == "male":
        first_name = random.choice(male_names) if male_names else "Unknown"

    elif sex.lower() == "female":
        first_name = random.choice(female_names) if female_names else "Unknown"
    else:
        raise ValueError("sex must be 'male' or 'female'")
    
    family_name = random.choice(family_names) if family_names else "Unknown"#family_name must be from the correct race family name pool
    if family_name not in game_state.extant_family_names:
        game_state.extant_family_names.append(family_name)
    #can we write to npc.family_name here? NO. Because npc/character/member cannot be passed into this function
    full_name = f"{first_name} {family_name}" 

    return first_name, family_name, full_name