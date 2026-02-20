#actions.npc_bodily_actions.py
import random
from debug_utils import debug_print

from base.posture import Posture
from objects.furniture import CafeChair


def sit_auto(npc, chair=None):
    location = npc.location

    if chair is None:
        free_chairs = [
            obj for obj in location.items.objects_present
            if isinstance(obj, CafeChair) and obj.is_free()
        ]
        if not free_chairs:
            return False
        chair = random.choice(free_chairs)

    if chair.occupy(npc):
        npc.current_chair = chair
        npc.POSTURE = Posture.SITTING
        debug_print(npc, f"[ACTION] {npc.name} sits at {chair.name} posture now: {npc.posture}", category="action")

        return True

    return False


def stand_auto():
    pass

#etc