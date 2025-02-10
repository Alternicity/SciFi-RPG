#common.py
import os
from enum import Enum, auto
import json
from dataclasses import dataclass, field
from typing import List, Optional

from status import Status

def get_file_path(*path_parts):
    """
    Constructs an absolute file path from the provided path parts.
    """
    # Use only the necessary relative path without hardcoding the base
    return os.path.join(os.getcwd(), *path_parts)

class DangerLevel(Enum):
    LOW = 1
    MID = 2
    HIGH = 3
    WARZONE = 4



# Default number of locations per region
# Mapping of region sizes to number of locations
region_size_to_locations = {
    "small": 5,
    "medium": 10,
    "large": 20,
}

    #fetch relevant faction locations
def load_locations(filepath, faction_name):
    with open(filepath, "r") as file:
        data = json.load(file)
    locations = []
    for region in data.get("regions", []):
        if faction_name in region.get("factions", []):
            locations.extend(region.get("locations", []))
    return locations


BASE_CHARACTERNAMES_DIR = get_file_path("data", "Names")

BASE_REGION_DIR = get_file_path("data", "Test City", "Regions")

BASE_SHOPS_DIR = get_file_path("data", "Test City", "Shops")

BASE_FACTIONS_DIR = get_file_path("data", "Test City", "Factions")

BASE_STARTINGLOYALTIES_DIR = get_file_path("data", "Test City", "startingLoyalties")

BASE_LOCATION_DIR = get_file_path("data", "Test City", "Locations")

BASE_CHARACTERS_DIR = get_file_path("data", "Test City", "Characters")

#Runtime data:
# Define BASE_RUNTIME_DIR dynamically
BASE_RUNTIME_DIR = get_file_path("scifiRPG", "data", "RuntimeData")

