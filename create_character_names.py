#create_character_names
from common import BASE_CHARACTERNAMES_DIR
import random
import os
from loader import load_names_from_csv
from get_valid_races import get_valid_races


def create_name(race, gender):

    """Generate a full name based on race and gender."""
    valid_races = get_valid_races()  # Get list of valid races from Character class

    # If no race is provided, choose one randomly from valid races
    if race is None:
        raise ValueError("create_name() called with race=None. This is not allowed for gangs.")
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