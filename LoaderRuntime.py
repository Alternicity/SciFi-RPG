import yaml
import os


def load_locations_from_yaml(region):
    filepath = os.path.join("scifiRPG", "data", "RuntimeData", "Regions", f"{region}.yml")
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
        return data.get("locations", [])
