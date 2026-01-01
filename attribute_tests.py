#attribute_tests.py
import random
from debug_utils import debug_print

def attribute_test(attribute_value, difficulty=10, modifiers=0):
    """
    Simple attribute test: pass if attribute + mods > random threshold.
    """
    roll = random.randint(1, 20)#roll is not accessed
    total = attribute_value + modifiers

    return total >= difficulty#Is this a truthy return?

def adversarial_attribute_test(
    attempt_value,
    resistance_value,
    attempt_mod=0,
    resistance_mod=0,
    wildcard_mod=0,
    simulate=False,
):
    """
    General-purpose adversarial attribute test.
    Compares an attempt (e.g., intimidation, stealth) against a resistance (e.g., loyalty, intercept).
    Optional modifiers and wildcard allow contextual bonuses.
    Parameters:
    - simulate (bool): If True, skip random elements for AI decision planning.
    - verbose (bool): Print breakdown of the score if debugging.
    Returns:
    - bool: True if the attempt succeeds, False otherwise.
    """
    base_attempt = attempt_value + attempt_mod + wildcard_mod
    base_resist = resistance_value + resistance_mod

    if not simulate:
        base_attempt += random.randint(0, 10)
        base_resist += random.randint(0, 10)

    return base_attempt > base_resist