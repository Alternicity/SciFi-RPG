import json
import os

def parse_city_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r") as f:
        city_data = json.load(f)
    
    characters = []
    locations = []
    
    for district, district_data in city_data.get("city", {}).items():
        print(f"Processing district: {district}")
        # Extract characters
        for character in district_data.get("characters", []):
            character["district"] = district  # Add district info for context
            characters.append(character)
        
        # Extract locations
        for location in district_data.get("locations", []):
            location["district"] = district  # Add district info for context
            locations.append(location)
    
    return characters, locations

def save_data(data, folder_name, file_name):
    # Ensure folder exists
    os.makedirs(folder_name, exist_ok=True)
    output_path = os.path.join(folder_name, file_name)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved: {output_path}")

# Main logic
file_path = "C:/Users/Stuart/Python Scripts/scifi RPG/data/Locations/test_city.json"

try:
    characters, locations = parse_city_data(file_path)
    
    # Print results for verification
    print("Characters:", characters)
    print("Locations:", locations)
    
    # Save outputs to the respective folders
    save_data(characters, "C:/Users/Stuart/Python Scripts/scifi RPG/data/Characters", "characters.json")
    save_data(locations, "C:/Users/Stuart/Python Scripts/scifi RPG/data/Locations", "locations.json")
except FileNotFoundError as e:
    print(e)
except RecursionError as e:
    print("Recursion Error:", e)
