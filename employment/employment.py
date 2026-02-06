# employment.employment.py

from create.create_game_state import get_game_state
game_state = get_game_state()
from debug_utils import debug_print
from memory.memory_entry import MemoryEntry
from anchors.anchor_utils import Anchor

def update_employee_presence(npc, hour):
    #This function is idempotent and safe to call every hour

    


    #Don’t create anchors in update_employee_presence
    emp = getattr(npc, "employment", None)
    if not emp or not emp.workplace:
        return

    workplace = emp.workplace
    on_duty = emp.on_duty(game_state.hour)#we must also investigate on_duty
    at_workplace = npc.location == workplace
    present = npc in workplace.employees_there

    debug_print(
            npc,
            f"[EMP PRESENCE] hour={game_state.hour} "
            f"on_duty={on_duty} "
            f"is_on_shift={emp.is_on_shift} "
            f"at_workplace={at_workplace}",
            category="employment"
        )

    # --- Shift start ---
    if on_duty and not emp.is_on_shift:
        emp.is_on_shift = True#is this working?
        emp.just_got_off_shift = False

    # Enter workplace
    if on_duty and at_workplace and not present:
        workplace.employees_there.append(npc)
        npc.mind.memory.add_episodic(
            subject=npc,
            verb="arrived_at_work",
            object_=workplace.name,
            content=f"Arrived at work at {workplace.name}.",
            importance=2,
            tags=["work", "arrival"]
        )
        debug_print(npc, f"[WORK] Started shift at {workplace.name}", category="employment")

    # Leave workplace
    if present and (not on_duty or not at_workplace):
        workplace.employees_there.remove(npc)
        npc.mind.memory.add_episodic(
            subject=npc,
            verb="finished_shift",
            object_=workplace.name,
            content=f"Finished work at {workplace.name}.",
            importance=2,
            tags=["work", "departure"]
        )
        debug_print(npc, f"[WORK] Left shift at {workplace.name}", category="employment")

    # --- Shift end ---
    if emp.is_on_shift and not on_duty:
        emp.is_on_shift = False
        emp.just_got_off_shift = True
        day = game_state.day
        """ update_employee_presence emits facts, not interpretation
        So it should create minimal episodic memory """
        npc.mind.memory.add_episodic(
        MemoryEntry(
            subject=npc.name,
            verb="finished_shift",
            object_=emp.workplace.name if emp.workplace else None,
            importance=3,
            tags=["work", "shift", "transition"],
            type="employment"
        ),
        current_day=game_state.day
    )


