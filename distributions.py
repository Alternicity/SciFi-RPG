#distributions.py
import random

def generate_normal(mean, std_dev):
    """
    Generate a value from a normal (Gaussian) distribution.

    Args:
        mean (float): The mean of the distribution.
        std_dev (float): The standard deviation of the distribution.

    Returns:
        float: A value from the normal distribution.
    """
    return random.gauss(mean, std_dev)

def generate_black_swan(threshold, impact_range):
    """
    Generate a value from a Black Swan distribution (rare, high-impact events).

    Args:
        threshold (float): The probability of a Black Swan event occurring (0 to 1).
        impact_range (tuple): The range of possible impacts (min, max).

    Returns:
        float or None: A high-impact value if the event occurs, otherwise None.
    """
    if random.random() < threshold:  # Rare event
        return random.uniform(impact_range[0], impact_range[1])
    return None  # No event

