from distributions import generate_normal, generate_black_swan

class Event:
    def __init__(self, name, event_type, effect, **kwargs):
        self.name = name
        self.description = description
        self.impact = impact or {}  # Dict to define changes caused by the event
        self.event_type = event_type
        self.effect = effect
        self.params = kwargs

    def handle_event(event_name, character, location):
        """Stub for an event system that will handle outcomes of actions."""
    event_outcomes = {
        "success": lambda: print(f"{character.name} successfully completes the action."),
        "detected": lambda: print(f"{character.name} was spotted! Guards are alerted."),
        "parsimony_opportunity": lambda: print(f"{character.name} notices another opportunity."),
        "triggered_trap": lambda: print(f"{character.name} sets off a trap! Trouble ahead."),
    }
    event_outcomes.get(event_name, lambda: print("Unknown event"))()

    def apply(self, target):
        """
        Older code that describes the rarity of game (not player) triggered events
        """
        if self.event_type == "normal":
            impact = generate_normal(self.params["mean"], self.params["std_dev"])
        elif self.event_type == "black_swan":
            impact = generate_black_swan(self.params["threshold"], self.params["impact_range"])
        else:
            raise ValueError(f"Unknown event type: {self.event_type}")

        if impact is not None:
            self._apply_effect(target, impact)

    def _apply_effect(self, target, impact):
        """
        Apply the effect to the target based on the event's configuration.
        """
        if self.effect["impact"] == "add":
            target[self.effect["resource"]] += impact
        elif self.effect["impact"] == "subtract":
            target[self.effect["resource"]] -= impact
        elif self.effect["impact"] == "modify":
            target[self.effect["attribute"]] += impact
        else:
            raise ValueError(f"Unknown effect type: {self.effect['impact']}")

        print(f"Event '{self.name}' occurred! Impact: {impact}")


def simulate_events(events, targets):
    """
    Simulate events and apply their effects to the targets.

    Args:
        events (list): A list of Event instances.
        targets (dict): A dictionary of targets (e.g., economy, factions).
    """
    for event in events:
        target = targets.get(event.effect["resource"] or event.effect["attribute"])
        if target:
            event.apply(target)



    def apply_to_faction(self, faction):
        """Apply event changes to a faction."""
        print(f"Applying event: {self.description}")
        for key, value in self.impact.items():
            if key in faction.resources:
                faction.resources[key] += value

#combatEvent
#combatAftermath