def load_region_data(region_name: str) -> dict:
    
    logger.debug(f"load_region_data called with: {region_name}")
    
    # Get the file path for the region
    region_file_path = get_region_file_path(region_name)
    logger.debug(f"Loading region data from: {region_file_path}")
    logger.debug(f"Region file path resolved to: {region_file_path}")
    if not os.path.exists(region_file_path):
        logger.error(f"Region file does not exist: {region_file_path}")


    try:
        with open(region_file_path, 'r') as file:
            region_data = json.load(file)
            return region_data
    except FileNotFoundError:
        logger.error(f"File not found: {region_file_path}")
        raise FileNotFoundError(f"Region data file '{region_file_path}' not found.")
    except ValueError as e:
        logger.error(f"Error decoding JSON data from '{region_file_path}': {e}")
        raise ValueError(f"Error decoding JSON data from '{region_file_path}': {e}")

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