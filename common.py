import os
from enum import Enum, auto
import json

def get_file_path(*path_parts):
    """
    Constructs an absolute file path from the provided path parts.
    """
    # Use only the necessary relative path without hardcoding the base
    return os.path.join(os.getcwd(), *path_parts)

def get_project_root():
    # Set the project root directory explicitly
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
class Status(Enum):
    LOW = "low"
    MID = "mid"
    HIGH = "high"
    ELITE = "elite"

    #fetch relevant faction locations
def load_locations(filepath, faction_name):
    with open(filepath, "r") as file:
        data = json.load(file)
    locations = []
    for region in data.get("regions", []):
        if faction_name in region.get("factions", []):
            locations.extend(region.get("locations", []))
    return locations

# Define BASE_REGION_DIR dynamically
BASE_REGION_DIR = get_file_path("data", "Test City", "Regions")

# Define BASE_SHOPS_DIR dynamically
BASE_SHOPS_DIR = get_file_path("data", "Test City", "Shops")

# Define BASE_RUNTIME_DIR dynamically
BASE_RUNTIME_DIR = get_file_path("scifiRPG", "data", "RuntimeData")