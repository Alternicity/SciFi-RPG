#actions.npc_bodily_actions.py
import random
from debug_utils import debug_print

from base.posture import Posture
from objects.furniture import CafeChair


def sit_auto(npc, region=None, chair=None, table=None, **kwargs):

    location = npc.location

    if table is not None:

        from objects.furniture import CafeChair

        free_chairs = [
            obj for obj in location.items.objects_present
            if isinstance(obj, CafeChair)
            and obj.table is table
            and obj.is_free()
        ]

        if not free_chairs:
            return False

        chair = free_chairs[0]

        if chair.occupy(npc):
            npc.posture = Posture.SITTING
            npc.current_chair = chair
            npc.seated_at = table
            npc.mind.remove_thoughts_with_tag("sit")

            debug_print(
                npc,
                f"[ACTION] {npc.name} sits at {chair.table.name} ({chair.name}) posture now: {npc.posture}",
                category="action"
            )
            npc.mind.remove_thoughts_with_tag("sit")
            npc.mind.remove_thoughts_with_tag("dine_in")
            return True

    return False


""" def stand_auto(npc, region=None, **kwargs):

    if npc.current_chair:
        npc.current_chair.vacate()

    npc.posture = Posture.STANDING

    from anchors.anchor_utils import debug_anchor
    from motivation.motivation import debug_motivations
    anchor = npc.current_anchor
    debug_anchor(anchor)

    debug_motivations(npc)#marked not defined, needs an import 

#and maybe augment this debug_print with its return value/s?
    debug_print(
        npc,
        f"[ACTION] {npc.name} stands up",
        category="action"
    ) """

def stand_auto(npc, region=None, **kwargs):

    if npc.current_chair:
        npc.current_chair.vacate()

    npc.posture = Posture.STANDING

    from anchors.anchor_utils import debug_anchor
    from motivation.motivation import debug_motivations
    anchor = npc.current_anchor
    

    debug_motivations(npc)#now its defined

    debug_print(
        npc,
        f"[ACTION] {npc.name} stands up",
        category="action"
    )
    
    #can we print the most urgent motivation or two here?
    