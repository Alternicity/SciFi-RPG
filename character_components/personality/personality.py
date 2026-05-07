#character_components.personality.personality.py
from base.core_types import PersonalityBase
import random
class Personality(PersonalityBase):

    def __init__(self,
                 extroversion,
                 curiosity,
                 discipline,
                 agreeableness,
                 neuroticism):

        self.extroversion = extroversion
        self.curiosity = curiosity
        self.discipline = discipline
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism

    def as_dict(self):
        return {
            "extroversion": self.extroversion,
            "curiosity": self.curiosity,
            "discipline": self.discipline,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism
        }