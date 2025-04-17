from characterActions import adversarial_attribute_test

class IntimidationTest:
    """
    A wrapper around the general adversarial test for intimidation scenarios.

    This makes it easier to plug into events like robberies, interrogations, etc.
    """

    def __init__(self, robber, target, wildcard_bonus=0):
        self.robber = robber
        self.target = target
        self.wildcard_bonus = wildcard_bonus

    def run(self, simulate=False, verbose=False):
        from combat import calculate_intimidation_score, calculate_resistance_score

        attempt_value = calculate_intimidation_score(self.robber)
        resistance_value = calculate_resistance_score(self.target)

        return adversarial_attribute_test(
            attempt_value=attempt_value,
            resistance_value=resistance_value,
            wildcard_mod=self.wildcard_bonus,
            simulate=simulate,
            verbose=verbose
        )
