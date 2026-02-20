# anchors/work_anchor.py
from anchors.anchor import Anchor
from debug_utils import debug_print
from create.create_game_state import get_game_state
game_state = get_game_state()
class WorkAnchor(Anchor):
    #No __init__
    #If an anchor must do extra setup, do it after super().__init__() and keep the signature identical.
    type = "work"
    name = "work"
    
    def resolve_target_location(self):
        npc = self.owner
        if getattr(npc, "employment", None):

            debug_print(
                npc,
                f"[WORK RESOLVE] {npc.name} is_on_shift={npc.employment.is_on_shift}",
                category="anchor"
            )

            return npc.employment.workplace