import json
import os
import yaml
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(file_path):
    """
    Dynamically load data from JSON, YAML, CSV, or TXT files.

    Args:
        file_path (str): Path to the file to be loaded.

    Returns:
        dict or list: Parsed data from the file.

    Raises:
        ValueError: If the file format is unsupported.
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Current working directory: {os.getcwd()}")

    _, ext = os.path.splitext(file_path)

    try:
        # Load the file based on its extension
        if ext in [".json"]:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                logger.info(f"Successfully loaded JSON data from {file_path}.")
                return data
        elif ext in [".yaml", ".yml"]:
            with open(file_path, "r") as yaml_file:
                data = yaml.safe_load(yaml_file)
                logger.info(f"Successfully loaded YAML data from {file_path}.")
                return data
        elif ext in [".csv"]:
            with open(file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                data = [row for row in reader]
                logger.info(f"Successfully loaded CSV data from {file_path}.")
                return data
        elif ext in [".txt"]:
            data = {}
            with open(file_path, "r") as txt_file:
                for line in txt_file:
                    if "=" in line:  # Simple key-value format
                        key, value = line.strip().split("=")
                        data[key] = value
                    else:  # Treat as a list of values
                        data = [line.strip() for line in txt_file]
                logger.info(f"Successfully loaded TXT data from {file_path}.")
                return data
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise

def _check_missing_keys(entry, required_keys):
    """Check if any required keys are missing in the entry."""
    missing_keys = [key for key in required_keys if key not in entry]
    if missing_keys:
        raise ValueError(f"Missing required keys in entry: {missing_keys}")

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
        # Load and validate factions data
        factions_data = load_data("data/factions.yaml")["factions"]
        faction_required_keys = ["name", "type", "affiliation", "goals"]
        validate_data(factions_data, faction_required_keys, validate_goals=True)

        # Load and validate civilians data
        civilians_data = load_data("data/civilians.csv")
        civilians_required_keys = ["name", "role", "faction", "loyalty"]
        validate_data(civilians_data, civilians_required_keys)

        # Load and validate state data
        state_data = load_data("data/state.json")
        state_required_keys = ["name", "resources", "laws", "goals"]
        validate_data(state_data, state_required_keys, validate_goals=True)

        logger.info("All data loaded and validated.")
    except Exception as e:
        logger.error(f"Error during data loading or validation: {e}")