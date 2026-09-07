#GUI.inspectors.entity.sublocation_inspector.py


from base.location import Sublocation
from GUI.inspectors.npc.sublocation_inspector import build_sublocation_inspector

#DELETE candidate
def refresh_sublocation_inspector(self):

    if self.inspected_target is None:
        return

    if not isinstance(self.inspected_target, Sublocation):
        return

    build_sublocation_inspector(#It just calls build!
        self,
        self.npc_main_panel,#is this creating npc_main_panel ?
        self.inspected_target#implies a default inspccted target object for the inspector
    )