#characterActionTests.py
from attribute_tests import adversarial_attribute_test
from debug_utils import can_narrate, debug_print#can_narrate greyed out, not accessed
class IntimidationTest:
    """
    A wrapper around the general adversarial test for intimidation scenarios.

    This makes it easier to plug into events like robberies, interrogations, etc.
    """

    def __init__(self, robber, target, wildcard_bonus=0):
        self.robber = robber
        self.target = target
        self.wildcard_bonus = wildcard_bonus

    def run(self, simulate=False, verbose=None):
        from combat import calculate_intimidation_score, calculate_resistance_score

        # 🔒 Authority lives here
        verbose = getattr(self.robber, "debug_role", None) == "primary"

        attempt_value = calculate_intimidation_score(self.robber)
        resistance_value = calculate_resistance_score(self.target)
        
        

        success = adversarial_attribute_test(
            attempt_value=attempt_value,
            resistance_value=resistance_value,
            wildcard_mod=self.wildcard_bonus,
            simulate=simulate
        )

        if getattr(self.robber, "debug_role", None) == "primary":
            debug_print(
                self.robber,
                f"Intimidation result → success={success}",
                category="event"
            )

        return success