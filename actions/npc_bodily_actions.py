#actions.npc_bodily_actions.py
import random
from debug_utils import debug_print

from base.posture import Posture
from objects.furniture import CafeChair


def sit_auto(npc, chair=None, table=None):
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
        #Resolve any sit thought here


        #are these return statements stil necessary, or are they now deprecated?
        return True

    return False


def stand_auto(npc):
    if npc.current_chair:
        npc.current_chair.occupied_by = None
        npc.current_chair = None
    npc.posture = Posture.STANDING

#etc