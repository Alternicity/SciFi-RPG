import json

from common import get_file_path
#ALL files use this to get the project root

def verify_city_data(city_data):
    # Check if the required keys exist in the city_data
    required_keys = ["regions"]
    for key in required_keys:
        if key not in city_data:
            raise ValueError(f"Missing required key: {key}")

    # Check structure within regions
    for region, data in city_data.get("regions", {}).items():
        if "factions" not in data or "characters" not in data:
            raise ValueError(f"Missing factions or characters in region: {region}")
        
        # Check that each faction and character is properly defined
        for faction in data["factions"]:
            if not isinstance(faction, str):
                raise ValueError(f"Invalid faction format in region {region}: {faction}")
        
        for character in data["characters"]:
            if "name" not in character or "loyalties" not in character:
                raise ValueError(f"Missing name or loyalties in character: {character}")
    
    print("City data is valid.")

# Load the city data
region_file = get_file_path("scifiRPG", "data", "Test City", "Locations", "test_city.json")
city_data = json.load(f)

# Verify the data structure
verify_city_data(city_data)
