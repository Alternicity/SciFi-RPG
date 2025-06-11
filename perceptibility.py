#perceptibility.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import uuid

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
            "type": self.__class__.__name__,
            "description": f"a {self.__class__.__name__}",
            "region": getattr(getattr(self, "region", None), "name", None),
            "location": getattr(getattr(self, "location", None), "name", None),
            "sublocation": getattr(getattr(self, "sublocation", None), "name", None),
            "robbable": getattr(self, "robbable", True),
            "origin": self,
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
    
    
#Optional: Enums or constants (like percept categories: VISUAL, AUDIO, ITEM, etc.)
