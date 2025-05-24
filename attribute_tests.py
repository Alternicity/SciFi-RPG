import random

def attribute_test(attribute_value, difficulty=10, modifiers=0, verbose=False):
    """
    Simple attribute test: pass if attribute + mods > random threshold.
    """
    roll = random.randint(1, 20)
    total = attribute_value + modifiers
    if verbose:
        print(f"Attribute Test → Roll: {roll}, Attribute+Mods: {total}, Difficulty: {difficulty}")

        # Swiz tries to pick a lock with Dexterity 12
        #success = attribute_test(attribute_value=12, difficulty=14, modifiers=1, verbose=True)

    return total >= difficulty

def adversarial_attribute_test(
    attempt_value,
    resistance_value,
    attempt_mod=0,
    resistance_mod=0,
    wildcard_mod=0,
    simulate=False,
    verbose=False
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
        attempt_roll = random.randint(0, 10)
        resist_roll = random.randint(0, 10)
        base_attempt += attempt_roll
        base_resist += resist_roll
        if verbose:
            print(f"[Verbose] Random roll → Attempt +{attempt_roll}, Resistance +{resist_roll}")

    if verbose:
        print(f"[Verbose] Final Attempt score: {base_attempt} vs Resistance score: {base_resist}")

    return base_attempt > base_resist