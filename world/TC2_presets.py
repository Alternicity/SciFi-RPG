# world.tc2_presets.py
import random
from employment.employee import EmployeeProfile
from employment.roles import CAFE_MANAGER, WAITRESS
from debug_utils import debug_print
from world.placement import place_character

from objects.food.drinks import Coffee
from objects.food.cutlery_crockery import Cup
from location.locations import Cafe
from objects.furniture import CafeTable, CafeChair



def get_tc2_cafe(region):
    cafe = next(
        (loc for loc in region.locations if loc.__class__.__name__ == "Cafe"),
        None
    )
    if not cafe:
        raise RuntimeError("TC2 requires a Cafe in region")
    return cafe#initial reference to the TC2 cafe. Doesnt seem to store a reference to this, just returns the cafe.
    #Probably not safe for future referencing as there will be more cafes eventually

def setup_tc2_civilian_liberty(npc, region):
    npc.region = region
    npc.home_region = region
    npc.hunger = 5 #bump npc hunger here, perhaps we could add some random range that will result in burger some tests and sandwich on others.

    debug_print(
        npc,
        f"[TC2 CIVILIAN:LIBERTY SETUP] region={region.name}",
        category=["placement"]
    )


def setup_tc2_worker(worker, region, *, role):#civilian_manager
    
    cafe = get_tc2_cafe(region)

    worker.is_employee = True

    # Create employment profile
    worker.employment = EmployeeProfile(
        workplace=cafe,
        role=role,
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

def place_tc2_passive_npc(npc, region):
    """
    Places a passive civilian in the Cafe, seated at a table,
    sipping coffee.
    """

    cafe = next((loc for loc in region.locations if isinstance(loc, Cafe)), None)
    if not cafe:
        raise RuntimeError("No Cafe found in region for passive NPC placement.")

    # Assign region + location
    npc.region = region
    npc.location = cafe
    npc.seated_at = None
    
    cafe.characters_there.append(npc)

    # Lock down behaviour
    npc.debug_role = "civilian_passive"
    npc.placement_locked = True

    # Find a table
    table = next(
        (o for o in cafe.items.objects_present
         if isinstance(o, CafeTable) and not o.occupants),
        None
    )

    if table:
        npc.seated_at = table
        table.occupants.append(npc)

    # Create drink
    cup = Cup()
    coffee = Coffee()
    cup.add(coffee)

    # Put cup on table if seated
    if table:
        cafe.items.objects_present.append(cup)
    else:
        cafe.items.objects_present.append(cup)

    return npc

def place_tc2_npc(npc, region):
    npc.region = region
    debug_print(
        npc,
        f"[TC2 PLACEMENT] region={npc.region.name} location={npc.location}",
        category="placement"
    )

def assign_tc2_staging_location(npc, region):
    """
    TC2-only placement.
    Puts NPC somewhere sensible in-region but not in a Cafe, Park or Vacantlot
    """
    candidates = [
        loc for loc in region.locations
        if loc.__class__.__name__ not in ("Cafe", "Park", "VacantLot")
    ]

    if not candidates:
        return False

    loc = random.choice(candidates)
    npc.location = loc
    npc.region = region
    loc.characters_there.append(npc)
    return True
