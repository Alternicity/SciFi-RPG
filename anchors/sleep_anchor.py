#anchors.sleep_anchor.py
from anchors.anchor import Anchor

class SleepAnchor(Anchor):
    type = "sleep"
    name = "sleep"

    def requires_movement(self):
        npc = self.owner
        return npc.location != getattr(npc, "home", None)

    def resolve_target_location(self):
        return getattr(self.owner, "home", None)

    def is_valid(self):
        npc = self.owner
        return not npc.motivation_manager.is_suppressed("sleep")