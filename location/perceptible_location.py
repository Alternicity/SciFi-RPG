from perception.perceptibility import PerceptibleMixin
from base.location import Location

class PerceptibleLocation(PerceptibleMixin, Location):

    def has_tag(self, tag: str) -> bool:
        return hasattr(self, "tags") and tag in self.tags