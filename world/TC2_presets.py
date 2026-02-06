# world.tc2_presets.py
from employment.employee import EmployeeProfile
from employment.roles import CAFE_MANAGER, WAITRESS
from debug_utils import debug_print

def get_tc2_cafe(region):
    cafe = next(
        (loc for loc in region.locations if loc.__class__.__name__ == "Cafe"),
        None
    )
    if not cafe:
        raise RuntimeError("TC2 requires a Cafe in region")
    return cafe



def setup_tc2_worker(worker, region, *, role):
    
    cafe = get_tc2_cafe(region)

    worker.is_employee = True

    # Create employment profile
    worker.employment = EmployeeProfile(
        workplace=cafe,
        role=role,
        #role_type not passed here, so it uses the default front_of_house
        shift="day",
        shift_start=1,
        shift_end=4
    )

    # Register as employee (NOT arrival)
    if hasattr(cafe, "employees"):
        cafe.employees.append(worker)

    debug_print(
        worker,
        f"[EMPLOYMENT] Initialized as {role.name} at {cafe.name}",
        category="employment"
    )

    # Assign role explicitly (TC2 preset authority)
    #worker.employment.role = CAFE_MANAGER
     #we now need to specify taht this applies to civilian_worker
    #And that the following line only applies to the waitress
    #worker.employment.role =WAITRESS



#Call after all characters are created
def seed_tc2_presets(waitress, manager):
    social = waitress.mind.memory.semantic.get("social")
    rel = social.get_relation(manager)
    rel.current_type = "co_worker"
    rel.trust = 2

