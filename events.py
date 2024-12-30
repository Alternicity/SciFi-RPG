import json
from distributions import generate_normal, generate_black_swan

class Event:
    def __init__(self, name, event_type, effect, **kwargs):
        self.name = name
        self.event_type = event_type
        self.effect = effect
        self.params = kwargs

    def apply(self, target):
        """
        Apply the event's effect to the target (e.g., economy, faction, character).
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

def load_events(file_path):
    """
    Load events from a JSON or YAML file.

    Args:
        file_path (str): Path to the file containing event data.

    Returns:
        list: A list of Event instances.
    """
    with open(file_path, "r") as file:
        event_data = json.load(file)

    events = []
    for name, config in event_data.items():
        events.append(Event(name=name, **config))
    return events

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