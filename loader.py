import os
import json
import logging
import yaml
import csv

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Mapping of user-friendly region names to filenames
REGION_MAPPING = {
    "NorthVille": "North.json",
    "EastSide": "East.json",
    "WestSide": "West.json",
    "SouthVille": "South.json",
    "Downtown": "Central.json",
}
# Base directory for region data
# Base directory for region data (absolute path)
# Assuming the loader.py file is located in the project root directory
BASE_REGION_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "Test City", "Regions")
)

def get_region_file_path(region_name: str) -> str:
    """
    Resolve the file path for a given region name.
    Args:
        region_name (str): User-friendly region name.
    Returns:
        str: Full normalized path to the JSON file.
    Raises:
        ValueError: If the region name is not found in the mapping.
    """
    filename = REGION_MAPPING.get(region_name)
    if not filename:
        logger.error(f"Region name '{region_name}' not found in the mapping.")
        raise ValueError(f"Region name '{region_name}' is not valid.")
    
    region_file_path = os.path.join(BASE_REGION_DIR, filename)
    logger.debug(f"Resolved file path: {region_file_path}")
    return os.path.normpath(region_file_path)



def load_region_data(region_name: str) -> dict:
    """
    Load region data from the JSON file.
    
    Args:
        region_name (str): User-friendly region name.
    
    Returns:
        dict: Parsed region data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If JSON data cannot be decoded.
    """

    
    logger.debug(f"Loading region data for: {region_name}")

    # Get the full file path
    region_file_path = get_region_file_path(region_name)
    
    # Log the absolute path for debugging
    absolute_path = os.path.abspath(region_file_path)
    logger.info(f"Attempting to load region file: {absolute_path}")
    
    try:
        with open(region_file_path, "r") as file:
            region_data = json.load(file)
        logger.info(f"Successfully loaded region data from {absolute_path}")
        #logger.debug(f"Resolved file path: {region_file_path}")
        #logger.debug(f"Current working directory: {os.getcwd()}")
        return region_data
    
    except FileNotFoundError:
        logger.error(f"Region file not found: {absolute_path}")
        raise FileNotFoundError(f"File not found: {absolute_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from file: {absolute_path}")
        raise ValueError(f"Invalid JSON in file: {absolute_path}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading region data: {e}")
        raise

def _check_missing_keys(entry, required_keys):
    """Check if any required keys are missing in the entry."""
    missing_keys = [key for key in required_keys if key not in entry]
    if missing_keys:
        raise ValueError(f"Missing required keys in entry: {missing_keys}")

def load_shops(region_name):
    """
    Load shops for a given region.
    
    Args:
        region_name (str): Name of the region.
    
    Returns:
        list: List of shop objects.
    """
    shops_file_path = os.path.normpath(
        os.path.join("scifiRPG", "data", "Test City", "Shops", f"{region_name}_shops.json")
    )
    absolute_path = os.path.abspath(shops_file_path)
    logger.info(f"Attempting to load shops from: {absolute_path}")

    try:
        with open(shops_file_path, "r") as file:
            shops_data = json.load(file)
        
        shops = []
        for shop_data in shops_data:
            if shop_data["type"] == "Shop":
                shop = Shop(
                    name=shop_data["name"],
                    inventory=shop_data["inventory"],
                    cash=shop_data["cash"],
                    bankCardCash=shop_data["bankCardCash"],
                    legality=shop_data["legality"],
                    security=shop_data["security"]
                )
            elif shop_data["type"] == "CorporateStore":
                shop = CorporateStore(
                    name=shop_data["name"],
                    corporation=shop_data["corporation"],
                    inventory=shop_data["inventory"],
                    cash=shop_data["cash"],
                    bankCardCash=shop_data["bankCardCash"],
                    legality=shop_data["legality"],
                    security=shop_data["security"]
                )
            elif shop_data["type"] == "Stash":
                shop = Stash(
                    name=shop_data["name"],
                    inventory=shop_data["inventory"],
                    cash=shop_data["cash"],
                    bankCardCash=shop_data["bankCardCash"],
                    legality=shop_data["legality"],
                    security=shop_data["security"]
                )
            shops.append(shop)
        
        logger.info(f"Successfully loaded {len(shops)} shops for region '{region_name}'.")
        return shops
    except Exception as e:
        logger.error(f"Failed to load shops for region '{region_name}': {e}")
        raise

def _validate_goal(goal):
    """Validate a goal entry."""
    if "goal" not in goal:
        raise ValueError(f"Missing 'goal' in goal entry: {goal}")
    if "priority" not in goal or goal["priority"] not in ["low", "medium", "high"]:
        raise ValueError(f"Invalid or missing 'priority' in goal entry: {goal}")
    if "reward" not in goal or not isinstance(goal["reward"], (int, float)):
        raise ValueError(f"Invalid or missing 'reward' in goal entry: {goal}")
    if goal["reward"] < 0:
        raise ValueError(f"Reward cannot be negative in goal entry: {goal}")

def validate_data(data, required_keys, validate_goals=False):
    """
    Validates that all required keys exist in the data and checks specific attributes for goals.

    Args:
        data (list or dict): Data to be validated.
        required_keys (list): List of keys that must be present.
        validate_goals (bool): Flag to validate goals, if applicable.

    Raises:
        ValueError: If any key is missing or if goal attributes are invalid.
    """
    if isinstance(data, dict):
        data = [data]  # Convert it to a list of one item for uniform processing

    for entry in data:
        _check_missing_keys(entry, required_keys)

        if "goals" in entry and validate_goals:
            for goal in entry["goals"]:
                _validate_goal(goal)

    logger.info("Validation passed!")


# Example usage
if __name__ == "__main__":
    try:
        region_name = "NorthVille"  # Replace with user input
        data = load_region_data(region_name)
        print(f"Region Data for {region_name}: {data}")
    except Exception as e:
        print(f"Error: {e}") 
