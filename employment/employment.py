# employment.employment.py

from create.create_game_state import get_game_state
game_state = get_game_state()
from debug_utils import debug_print
from memory.memory_entry import MemoryEntry
from anchors.anchor_utils import Anchor
from create.create_game_state import get_game_state
from employment.service_jobs.cafe_restaurant_work import CafeRestaurantWorkSession
current_hour = game_state.hour

def update_employee_presence(npc, hour):
    #This function is idempotent and safe to call every hour

    #Don’t create anchors in update_employee_presence
    emp = npc.employment
    if not emp or not emp.workplace:
        return
    
    workplace = emp.workplace
    on_duty = emp.on_duty(hour)

    previous_state = emp.is_on_shift
    # Update shift flag
    emp.is_on_shift = on_duty

    if previous_state and not on_duty:
        emp.just_got_off_shift = True
    elif not previous_state and on_duty:
        emp.just_got_off_shift = False

    at_workplace = npc.location == workplace
    present = npc in workplace.employees_there

    debug_print(#this is called regardless of whether waitress npc is at the cafe workplace
        npc,
        f"[EMP PRESENCE] hour={hour} "
        f"on_duty={on_duty} "
        f"is_on_shift={emp.is_on_shift} "
        f"at_workplace={at_workplace}",
        category="employment"
    )

    # on_duty(hour) is the single authority for shift state.
    # is_on_shift mirrors schedule truth and should not be set elsewhere.

    #World queries should rely on emp.is_on_shift

    # Enter workplace
    if on_duty and at_workplace and not present:
        npc.work_session = CafeRestaurantWorkSession(
            npc,
            workplace
        )
        debug_print(
            npc,
            f"[WORK SESSION] Created new session",
            category="employment"
        )
        workplace.employees_there.append(npc)

        npc.mind.memory.add_episodic(
        MemoryEntry(
            subject=npc.name,
            verb="arrived_at_work",
            object_=workplace.name,
            details=f"Arrived at work at {workplace.name}.",
            importance=2,
            tags=["work", "arrival"]
        )
    )

        debug_print(npc, f"[WORK] Started shift at {workplace.name}", category="employment")

    # Leave workplace
    if present and (not on_duty or not at_workplace):
        workplace.employees_there.remove(npc)
        entry = MemoryEntry(
        subject=npc.name,
        verb="left_workplace",
        object_=workplace.name,
        details=f"Left workplace {workplace.name}.",
        owner=npc,
        importance=2,
        tags=["work", "departure"]
    )

        npc.mind.memory.add_episodic(entry)
        #alter just_got_off_shift here?
        npc.work_session = None#delete the current session
        debug_print(npc, f"[WORK] Left shift at {workplace.name}", category="employment")


