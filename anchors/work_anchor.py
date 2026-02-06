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
        
    def propose_action(self):
        npc = self.owner

        if not getattr(npc, "employment", None):
            return None

        # Must already be at workplace
        if npc.location != npc.employment.workplace:
            return None

        debug_print(
            npc,
            f"[WORK ANCHOR DEBUG] role={npc.debug_role} "
            f"loc={npc.location} "
            f"workplace={npc.employment.workplace if npc.employment else None} "
            f"tags={self.tags}",
            category="anchor"
        )

        debug_print(
            npc,
            f"[WORK CHECK] on_shift={npc.employment.is_on_shift if hasattr(npc.employment,'is_on_shift') else '??'} "
            f"hour={game_state.hour}",
            category="anchor"
        )

        debug_print(
            npc,
            "[WORK ANCHOR] Proposing action: perform_work",
            category="anchor"
        )

        return {"name": "perform_work"}
