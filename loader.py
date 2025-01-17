import os
import json
import logging
from typing import List, Union
from location import Shop, CorporateStore, Stash


# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Base directory for region data
BASE_REGION_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "Test City", "Shops")
)

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


def get_shops_file_path(region_name: str) -> str:
    """
    Constructs the full path to the shops JSON file for a given region.
    
    Args:
        region_name (str): The name of the region (e.g., 'North').
    
    Returns:
        str: The full path to the shops file for the region.
    """
    valid_regions = ["North", "East", "West", "South", "Central"]
    
    if region_name not in valid_regions:
        logger.error(f"Region name '{region_name}' is not valid.")
        raise ValueError(f"Region name '{region_name}' is not valid.")
    
    region_file_name = f"{region_name.capitalize()}_shops.json"
    shops_file_path = os.path.join(BASE_REGION_DIR, region_file_name)
    
    logger.debug(f"Resolved file path: {shops_file_path}")
    return os.path.normpath(shops_file_path)


def load_shops(region_name: str) -> List[Union[Shop, CorporateStore, Stash]]:
    """
    Loads the shops data for the specified region from the corresponding JSON file.
    
    Args:
        region_name (str): The name of the region (e.g., 'North').
    
    Returns:
        list: A list of shop objects created from the JSON data.
    
    Raises:
        FileNotFoundError: If the shops file does not exist.
        ValueError: If there is an error decoding the JSON data.
    """
    shops_file_path = get_shops_file_path(region_name)

    # Check if the file exists before attempting to open
    if not os.path.exists(shops_file_path):
        logger.error(f"Shops file does not exist: {shops_file_path}")
        raise FileNotFoundError(f"Shops data file '{shops_file_path}' not found.")
    
    logger.debug(f"Loading shop data for region: {region_name}")
    try:
        with open(shops_file_path, 'r') as file:
            shops_data = json.load(file)
            logger.debug("Shops data loaded successfully.")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON data from '{shops_file_path}': {e}")
        raise ValueError(f"Error decoding JSON data from '{shops_file_path}': {e}")
    
        # Validate and parse shop data
    for shop_data in shops_data:
        if not validate_shop_data(shop_data):
            raise ValueError(f"Invalid shop data: {shop_data}")


    # Parse shop data and create shop objects
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

def validate_shop_data(shop_data: dict) -> bool:
    """
    Validates a single shop entry from the JSON data.
    Returns True if valid, False otherwise.
    """
    required_keys = {"type", "name", "inventory", "cash", "bankCardCash", "legality", "security"}
    missing_keys = required_keys - shop_data.keys()
    if missing_keys:
        logger.error(f"Shop entry is missing required keys: {missing_keys}")
        return False
    
    if shop_data["type"] == "CorporateStore" and "corporation" not in shop_data:
        logger.error(f"CorporateStore entry missing 'corporation': {shop_data}")
        return False
    else:
        return True

    # Additional validation logic (e.g., value types, ranges)
    if not isinstance(shop_data["inventory"], list):
        logger.error(f"'inventory' must be a list: {shop_data}")
        return False
    return True

def initialize_shops(region_name: str) -> List[Union[Shop, CorporateStore, Stash]]:
    """
    Initializes shop objects for the given region.
    """
    logger.debug(f"Initializing shops for region: {region_name}")
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
        dict: A dictionary containing the region data.
    
    Raises:
        FileNotFoundError: If the region data file does not exist.
        ValueError: If there is an error decoding the JSON data.
    """
    region_file_path = get_region_file_path(region_name)

    # Check if the file exists before attempting to open
    if not os.path.exists(region_file_path):
        logger.error(f"Region data file does not exist: {region_file_path}")
        raise FileNotFoundError(f"Region data file '{region_file_path}' not found.")
    
    try:
        with open(region_file_path, 'r') as file:
            region_data = json.load(file)
            logger.debug(f"Region data loaded successfully from '{region_file_path}'.")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON data from '{region_file_path}': {e}")
        raise ValueError(f"Error decoding JSON data from '{region_file_path}': {e}")
    
    return region_data



# Example usage
if __name__ == "__main__":
    try:
        region_name = "North"  # Example region name, replace with user input
        shops = load_shops(region_name)
        print(f"Loaded {len(shops)} shops for region '{region_name}'.")
    except Exception as e:
        print(f"Error: {e}")
