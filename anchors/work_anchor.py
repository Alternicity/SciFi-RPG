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

        if not npc.employment or not npc.employment.is_on_shift:
            return None

        return npc.employment.workplace
        
    def is_valid(self):#Should class Anchor have a version of this, making this an override?
        npc = self.owner
        return npc.employment and npc.employment.is_on_shift
    
    def is_satisfied(self, npc):
        # Satisfied only when shift is over, not just when arrived
        hour = get_game_state().hour
        return not npc.employment.on_duty(hour)