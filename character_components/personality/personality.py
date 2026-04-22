#character_components.personality.personality.py
from base.core_types import PersonalityBase
import random
class Personality(PersonalityBase):

    def __init__(self,
                 extroversion,
                 curiosity,
                 discipline,
                 agreeableness,
                 boldness):

        self.extroversion = extroversion
        self.curiosity = curiosity
        self.discipline = discipline
        self.agreeableness = agreeableness
        self.boldness = boldness

    def as_dict(self):
        return {
            "extroversion": self.extroversion,
            "curiosity": self.curiosity,
            "discipline": self.discipline,
            "agreeableness": self.agreeableness,
            "boldness": self.boldness
        }