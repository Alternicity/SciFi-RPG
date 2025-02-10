import os
import json
import logging
from typing import List, Union
from location import Shop, CorporateStore, Stash
from characters import Character, Employee, Civilian, Manager
from location_security import Security
#from character_creation_funcs import player_character_options
from typing import List, Dict, Union
#If loader.py already imports location, and location imports Security, you could access it as:
#from location import Security
#ALL files use this to get the project root
from common import BASE_REGION_DIR, BASE_SHOPS_DIR, BASE_CHARACTERNAMES_DIR
# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
import csv


def get_region_file_path(region_name: str) -> str:
    """
    Constructs the full file path for a region's shop data.
    
    Args:
        region_name (str): The name of the region (e.g., 'North').
    
    Returns:
        str: The absolute path to the region's shop JSON file.
    
    Raises:
        ValueError: If the region name is invalid.
    """
    # List of valid regions
    valid_regions = ["North", "East", "West", "South", "Central"]
    
    # Check if the region name is valid
    if region_name not in valid_regions:
        logger.error(f"Region name '{region_name}' is not valid.")
        raise ValueError(f"Region name '{region_name}' is not valid.")
    
    # Capitalize the first letter of the region name and construct the file name
    region_file_name = f"{region_name.capitalize()}_shops.json"  # Capitalize first letter
    region_file_path = os.path.join(BASE_REGION_DIR, region_file_name)
    logger.debug(f"Resolved file path: {region_file_path}")
    
    # Normalize the path (this ensures compatibility with both Windows and Unix systems)
    return os.path.normpath(region_file_path)


def get_gang_names_filepath():
    """Returns the file path for the gang names data file."""
    return "scifiRPG/data/Names/GangNames.txt"

def load_gang_names(filepath):
    """Loads gang name parts from file and returns two lists (first part, second part)."""
    with open(filepath, "r") as file:
        lines = file.readlines()

    first_part, second_part = [], []
    current_list = None

    for line in lines:
        line = line.strip()
        if "First part:" in line:
            current_list = first_part
        elif "Second Part:" in line:
            current_list = second_part
        elif line and current_list is not None:
            current_list.append(line)

    return first_part, second_part

def get_shops_file_path(region_name: str) -> str:
    """
    Constructs the full path to the shops JSON file for shops data.
    
    Args:
        region_name (str): The name of the region (e.g., 'North').
    
    Returns:
        str: The full path to the shops file for the region.
    """
    valid_regions = ["North", "East", "West", "South", "Central"]
    
    if region_name not in valid_regions:
        logger.error(f"Region name '{region_name}' is not valid.")
        raise ValueError(f"Region name '{region_name}' is not valid.")
    
    shops_file_name = f"{region_name.capitalize()}_shops.json"
    shops_file_path = os.path.join(BASE_SHOPS_DIR, shops_file_name)
    

    logger.debug(f"Resolved file path: {shops_file_path}")
    return os.path.normpath(shops_file_path)
    
def load_shops(region_name: str) -> List[Dict]:
    """
    Loads the shops data for the specified region from the corresponding JSON file.
    Returns:
        list: A list of shop dictionaries.
    """
    shops_file_path = get_shops_file_path(region_name)

    # Check if the file exists before attempting to open
    if not os.path.exists(shops_file_path):
        raise FileNotFoundError(f"Shops data file '{shops_file_path}' not found.")
    
    try:
        with open(shops_file_path, 'r') as file:
            shops_data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON data from '{shops_file_path}': {e}")
    
    # Validate shop data
    for shop_data in shops_data:
        if not validate_shop_data(shop_data):
            raise ValueError(f"Invalid shop data: {shop_data}")

    return shops_data

def validate_shop_data(shop_data: Dict) -> bool:
    """
    Validates a single shop entry from the JSON data.
    Returns True if valid, False otherwise.
    """
    required_keys = {"type", "name", "inventory", "cash", "bankCardCash", "legality", "security"}
    missing_keys = required_keys - shop_data.keys()
    if missing_keys:
        print(f"Shop entry is missing required keys: {missing_keys}")
        return False
    
    if shop_data["type"] == "CorporateStore" and "corporation" not in shop_data:
        print(f"CorporateStore entry missing 'corporation': {shop_data}")
        return False

    # Additional validation logic (e.g., value types, ranges)
    if not isinstance(shop_data["inventory"], dict):
        print(f"'inventory' must be a dictionary: {shop_data}")
        return False

    return True

def initialize_shops(region_name: str) -> List[Union[Shop, CorporateStore, Stash]]:
    """
    Initializes shop objects for the given region.
    """
    #logger.debug(f"Initializing shops for region: {region_name}")
    shops = load_shops(region_name)

    # Perform additional processing (e.g., assign faction ownership)
    for shop in shops:
        # Example: Assign a default faction if not set
        if isinstance(shop, CorporateStore) and not getattr(shop, "corporation", None):
            shop.corporation = "Neutral Corporation"
            shops = enrich_shops_with_faction_data(shops)

    return shops


def load_region_data(region_name: str) -> dict:
    """
    Loads region-specific data from a JSON file.
    
    Args:
        region_name (str): The name of the region (e.g., 'North').
    
    Returns:
        dict: A data structure containing the region data.
    
    Raises:
        FileNotFoundError: If the region data file does not exist.
        ValueError: If there is an error decoding the JSON data.
    """
    file_path = os.path.join(BASE_REGION_DIR, f"{region_name}.json")
    #region_file_path = get_region_file_path(region_name)
    #Use BASE_REGION_DIR in common.py for this

    # Check if the file exists before attempting to open
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Region data file does not exist: {file_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {file_path}: {e}")
    
    return region_data

""" def load_characters(selected_character_data):
    
    logging.info("Loading characters...")
    
    characters = player_character_options()

    # Validate input or default to empty list
    if selected_character_data is None:
        logging.error("No character data provided to loader.")
        return []
    
    # Initialize the character list
    characters = []


    # Instantiate the selected character
    data = selected_character_data
    if data["type"] == "Manager":
        character = Manager(
            name=data["name"],
            faction=data["faction"],
            bankCardCash=data["bankCardCash"],
            fun=data["fun"],
            hunger=data["hunger"],
        )
    elif data["type"] == "Civilian":
        character = Civilian(
            name=data["name"],
            faction=data["faction"],
            occupation=data.get("occupation", "Unemployed"),
        )
    else:
        character = Character(
            name=data["name"],
            faction=data["faction"],
        )

    characters.append(character)
    #logging.info(f"Loaded characters: {characters}")
    return characters """

def load_names_from_csv(filepath):
    """
    Loads names from a CSV file structured with separate Male, Female, and Family sections.
    """
    male_names = []
    female_names = []
    family_names = []
    
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        current_list = None
        
        for row in reader:
            if not row:
                continue
            
            if row[0].lower() == "id,male name":
                current_list = male_names
                continue
            elif row[0].lower() == "id,female name":
                current_list = female_names
                continue
            elif row[0].lower() == "id,family name":
                current_list = family_names
                continue
            
            if current_list is not None and len(row) > 1:
                current_list.append(row[1].strip())
    
    return male_names, female_names, family_names

# Example usage
if __name__ == "__main__":
    try:
        region_name = "North"  # Example region name, replace with user input
        shops = load_shops(region_name)
        print(f"Loaded {len(shops)} shops for region '{region_name}'.")
    except Exception as e:
        print(f"Error: {e}")


