#perceptibility.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import uuid
from tabulate import tabulate

# Avoid using .get() for dict access unless missing keys are expected.
# Use dict["key"] if the key should exist (will raise KeyError if missing).
# Use dict["key"] if "key" in dict else fallback_value if it's optional.
# Example:
# salience = percept["salience"] if "salience" in percept else "?"

class PerceptibleMixin:
    def __init__(self):
        self.id = str(uuid.uuid4())

    def compute_salience(self, observer=None):
        return getattr(self, "salience", 1)

    def percept_weight(self, observer=None):
        return getattr(self, "weight", 1)

    def get_suggested_actions(self, observer=None):
        return getattr(self, "suggested_actions", [])

    def has_security(self):
        return getattr(self, "security_level", 0) > 0

    def get_percept_data(self, observer=None):
        return {
            "name": getattr(self, "name", "Unknown"),
            "type": self.__class__.__name__.lower(),
            #"description": f"a {self.__class__.__name__}",
            "description": getattr(self, "name", str(self)),
            "region": getattr(getattr(self, "region", None), "name", None),
            "location": getattr(getattr(self, "location", None), "name", None),
            "sublocation": getattr(getattr(self, "sublocation", None), "name", None),
            "robbable": getattr(self, "robbable", True),
            "origin": self,
            """ Proposal:
            origin in a percept means “the actual object in the world this percept refers to”.
            This way, anything else the AI needs to know can be retrieved from the origin reference, not just from the percept snapshot. 
            keep origin as the pointer back to source entity."""

            "salience": self.compute_salience(observer),
            "tags": getattr(self, "tags", []),
            "urgency": getattr(self, "urgency", 1),
            "weight": self.percept_weight(observer),
            "source": None,
            "suggested_actions": self.get_suggested_actions(observer),
            "security": getattr(self, "security_level", 0),
            "is_open": getattr(self, "is_open", False),
            "has_security": self.has_security(),
            "bloodstained": getattr(self, "bloodstained", None)
        }


    def describe_self(self) -> str:
        """
        Optional: Turn percept data into a string for debug/logging/GUI purposes.
        """
        return str(self.get_percept_data())
    
    
    def validate_percepts(character):
        """
        Debugging tool: Check all percepts on the character and report malformed entries.
        """
        for key, entry in character._percepts.items():
            if "data" not in entry:
                print(f"[ERROR] Percept for key '{key}' missing 'data' field.")
                continue

            data = entry["data"]
            origin = entry.get("origin", data.get("origin"))

            if not isinstance(data, dict):
                print(f"[ERROR] Percept data for key '{key}' is not a dict: {data}")
            if "description" not in data:
                print(f"[WARNING] Percept data for key '{key}' is missing 'description'.")
            if origin is None:
                print(f"[WARNING] Percept for key '{key}' is missing an origin.")
            if "type" not in data:
                print(f"[WARNING] Percept data for key '{key}' is missing 'type'.")

            #usage
            #validate_percepts(npc)


#Optional: Enums or constants (like percept categories: VISUAL, AUDIO, ITEM, etc.)
def extract_appearance_summary(obj):
    from base_classes import Character
    """Given an object (Character, Location, ObjectInWorld), return a simple appearance string."""
    if hasattr(obj, "get_percept_data"):
        data = obj.get_percept_data()

        # Apply any _postprocess_percept functions
        if hasattr(obj, "_postprocess_percept") and callable(obj._postprocess_percept):
            data = obj._postprocess_percept(data, observer=None)

        if isinstance(obj, Character):
            # Basic visual traits
            race = obj.race
            sex = obj.sex
            features = obj.appearance.get("notable_features", [])
            visual = [race, sex] + features
            return ", ".join(filter(None, visual))

        elif hasattr(obj, "condition") and hasattr(obj, "security"):
            # Likely a Location
            guarded = "guarded" if getattr(obj.security, "guards", []) else "unguarded"
            return f"{obj.condition}, {guarded}"

        elif hasattr(obj, "item_type"):
            # Likely ObjectInWorld or similar
            return data.get("description", obj.__class__.__name__)

    return "[Unknown appearance]"