#perceptibility.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import uuid

class PerceptibleMixin(ABC):
    """
    Mixin to provide perceptual data to observers.
    This should be added to any class that can be perceived in the world (items, characters, locations, etc.)
    """

    def __init__(self):
        self.id = str(uuid.uuid4())

    def compute_salience(self, observer):
        return 5  # default, overridable

    @abstractmethod
    def get_percept_data(self, observer=None):
        return {
            "type": self.__class__.__name__,
            "salience": self.compute_salience(observer),
            "weight": self.percept_weight(observer),
            "suggested_actions": self.get_suggested_actions(observer)
        }


    def describe_self(self) -> str:
        """
        Optional: Turn percept data into a string for debug/logging/GUI purposes.
        """
        return str(self.get_percept_data())
    
    
#Optional: Enums or constants (like percept categories: VISUAL, AUDIO, ITEM, etc.)
