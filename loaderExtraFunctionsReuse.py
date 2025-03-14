
def _check_missing_keys(entry, required_keys):
    """Check if any required keys are missing in the entry."""
    missing_keys = [key for key in required_keys if key not in entry]
    if missing_keys:
        raise ValueError(f"Missing required keys in entry: {missing_keys}")
    
    #possibly deprecated
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