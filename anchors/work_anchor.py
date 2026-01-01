# anchors/work_anchor.py

class WorkAnchor(Anchor):#Anchor marked not defined
    def __init__(self, npc, motivation):
        self.npc = npc
        self.motivation = motivation
        self.name = "work_anchor"

    def resolve_target_location(self):
        return self.npc.employment.workplace