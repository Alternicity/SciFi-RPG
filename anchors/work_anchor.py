# anchors/work_anchor.py
from anchors.anchor import Anchor

class WorkAnchor(Anchor):#Anchor marked not defined
    #No __init__
    #If an anchor must do extra setup, do it after super().__init__() and keep the signature identical.
    def resolve_target_location(self):
        npc = self.owner
        if getattr(npc, "employment", None):
            return npc.employment.workplace
        return None