# world.tc2_presets.py
from employment.employee import EmployeeProfile

def setup_tc2_worker(worker, region):
    cafe = next(
        (loc for loc in region.locations if loc.__class__.__name__ == "Cafe"),
        None
    )
    if not cafe:
        raise RuntimeError("TC2 requires a Cafe in region")

    worker.employment = EmployeeProfile(
        workplace=cafe,
        shift_start=9,
        shift_end=17,
        shift="day"
    )
#note: do not set is_on_shift here
