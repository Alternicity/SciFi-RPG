#location.perceptible_location.py
from perception.perceptibility import PerceptibleMixin
from base.location import Location
from dataclasses import dataclass

@dataclass
class PerceptibleLocation(PerceptibleMixin, Location):

    def __post_init__(self):
        super().__post_init__()
        
    def has_tag(self, tag: str) -> bool:
        return hasattr(self, "tags") and tag in self.tags