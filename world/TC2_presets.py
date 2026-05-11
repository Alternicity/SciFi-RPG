# world.tc2_presets.py
import random
from employment.employee import EmployeeProfile
from employment.roles import CAFE_MANAGER, WAITRESS
from debug_utils import debug_print
from world.placement import place_character
from base.posture import Posture
from objects.food.drinks import Coffee
from objects.food.cutlery_crockery import Cup
from location.locations import Cafe
from objects.furniture import CafeTable, CafeChair
from create.create_game_state import get_game_state
from character_components.npc_effects import MorningSettlingEffect

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
    npc.hunger = 5#bump npc hunger here, perhaps we could add some random range that will result in burger some tests and sandwich on others.
    npc.effects.append(MorningSettlingEffect())
    npc.effects[-1].on_start(npc)

    # Force home to be in the correct region
    home_candidates = [
        loc for loc in region.locations
        if loc.__class__.__name__ in ("House", "ApartmentBlock")
    ]
    if home_candidates:
        chosen_home = random.choice(home_candidates)
        npc.residences = [chosen_home]      # sets npc.home via property
        npc.location = chosen_home
        if npc not in chosen_home.characters_there:
            chosen_home.characters_there.append(npc)
        gs = get_game_state()
        gs.reserved_homes[npc.id] = chosen_home
#bump npc hunger here, perhaps we could add some random range that will result in burger some tests and sandwich on others.

def setup_tc2_worker(worker, region, *, role):#civilian_manager, and civilian_waitress
    
    cafe = get_tc2_cafe(region)

    worker.is_employee = True

    # Create employment profile
    worker.employment = EmployeeProfile(
        workplace=cafe,
        role=role,
        role_type=role.role_type,
        shift="day",
        shift_start=1,
        shift_end=4
    )

    # Register as employee (NOT arrival)
    if hasattr(cafe, "employees"):
        cafe.employees.append(worker)

    # Force home to correct region
    home_candidates = [
        loc for loc in region.locations
        if loc.__class__.__name__ in ("House", "ApartmentBlock")
    ]
    if home_candidates:
        chosen_home = random.choice(home_candidates)
        if chosen_home not in worker.residences:
            worker.residences = [chosen_home]  # set as primary residence
        worker.location = chosen_home
        if worker not in chosen_home.characters_there:
            chosen_home.characters_there.append(worker)

        gs = get_game_state()
        gs.reserved_homes[worker.id] = chosen_home

    # Attach to worker/manager to counter
    if isinstance(worker.location, Cafe) and worker.employment.role == CAFE_MANAGER:
        counter = getattr(worker.location, "counter", None)
        if counter:
            counter.seat(worker)
            worker.posture = Posture.STANDING  # behind counter
            worker.current_counter = counter

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
    npc.location = cafe#a fragile way to get the cafe in the downtown/TC2 region
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
        from actions.npc_bodily_actions import sit_auto #actions.npc_bodily_actions marked Import cannot be resolved
        sit_auto(npc, table=table)

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

    # 🔥 Ensure valid starting location in region
    if not npc.location or npc.location.region != region:
        candidates = [
            loc for loc in region.locations
            if loc.__class__.__name__ in ("House", "ApartmentBlock")
        ]

        if candidates:
            location = random.choice(candidates)
            place_character(npc, location)
        else:
            # fallback but STILL in region
            fallback = random.choice(region.locations)
            place_character(npc, fallback)

def assign_tc2_staging_location(npc, region):

    candidates = [
        loc for loc in region.locations
        if "restaurant" not in loc.tags
        and "cafe" not in loc.tags
        and "park" not in loc.tags
        and "vacant" not in loc.tags
    ]

    if not candidates:
        return False

    loc = random.choice(candidates)

    npc.location = loc
    npc.region = region
    loc.characters_there.append(npc)

    return True
