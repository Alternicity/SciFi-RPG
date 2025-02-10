import yaml
import os


def load_locations_from_yaml(region):
    filepath = os.path.join("scifiRPG", "data", "RuntimeData", "Regions", f"{region}.yml")
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
        return data.get("locations", [])

def load_serialized_characters(): # is this relevant here?
    try:
        with open("characters.json", "r") as f:
            data = json.load(f)
        characters = [Character(**char_data) for char_data in data]
        #logging.info(f"Loaded characters: {characters}")
        return characters
    except FileNotFoundError:
        #logging.error("No serialized character data found.")
        return []
    except Exception as e:
        logging.error(f"Error loading serialized characters: {e}")
        return []