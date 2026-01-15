#create.createCivilians.py
import random
import collections
import math
from base.character import Character
from character_components.inventory_component import InventoryComponent
from base.faction import Factionless
from location.locations import Shop, Region, Park, Cafe
from location.location_types import WORKPLACES, PUBLIC_PLACES, RESIDENTIAL
from characters import Civilian, SpecialChild, Adepta
from objects.InWorldObjects import Wallet
from motivation.motivation import MotivationManager, VALID_MOTIVATIONS
from motivation.motivation_presets import MotivationPresets #not accessed here
from motivation.motivation_init import initialize_motivations
from status import CharacterStatus, FactionStatus, StatusLevel
from ai.ai_civilian import AdeptaAI
from utils import normalize_location_regions, get_region_for_location, find_location_by_type
from city_vars import CIVILIANS_PER_REGION, SHOP_PATRONS_MIN, SHOP_PATRONS_MAX, MAX_CIVILIANS_PER_LOCATION
from debug_utils import debug_print, add_character
#from employment.roles import CASHIER, SHOP_MANAGER, COOK, CAFE_MANAGER, WAITRESS, LINE_WORKER, FOREMAN, FACTORY_MANAGER, FARMHAND, FARM_SUPERVISOR, FARM_MANAGER
from employment.roles import ROLE_RULES
from character_mind import Mind, Curiosity
from tasks.tasks import TaskManager
from employment.employee import EmployeeProfile
from character_components.observation_component import ObservationComponent
from augment.augment_character import augment_character

def create_civilian_population(all_locations, all_regions, factionless, num_civilians=None):
    """Generate civilians and assign them logical locations."""
    from create.create_character_names import create_name
    from create.create_game_state import get_game_state
    game_state = get_game_state()

    normalize_location_regions(all_locations, all_regions)  # 🧹 Ensure valid region refs

    civilians = []
    valid_races = Character.VALID_RACES
    race_pool = ["Terran"] * 5 + [race for race in valid_races if race != "Terran"]

    # Categorize locations

    homes = [loc for loc in all_locations if "residential" in getattr(loc, "categories", [])]
    workplaces = [loc for loc in all_locations if any(cat in getattr(loc, "categories", []) for cat in ("workplace", "commercial"))]
    public_spaces = [loc for loc in all_locations if "public" in getattr(loc, "categories", [])]#public_spaces not yet accessed
    shops = [loc for loc in all_locations if isinstance(loc, Shop)]#shop not yet accessed
    
    if not homes:
        raise ValueError("❌ No residential locations found for civilian placement.")
    if not workplaces:
        print("⚠️ No workplaces found. Civilians will start at home only.")

    civilians_per_region = num_civilians or CIVILIANS_PER_REGION

    # --- Region-based creation ---
    for region in all_regions:
        for _ in range(civilians_per_region):
            race = random.choice(race_pool)
            sex = random.choice(["male", "female"])
            first_name, family_name, full_name = create_name(race, sex)
            random_cash = random.randint(5, 500)
            
        # Assign home
            home = random.choice(homes)
            region_for_home = get_region_for_location(home, all_regions)
            if not region_for_home:
                print(f"⚠️ Skipping {full_name}: home {home.name} has no region.")
                continue

            # Base character
            civilian = Civilian(
                name=full_name,
                first_name=first_name,
                family_name=family_name,
                region=None,
                sex=sex,
                location=None,  # Assigned later
                race=race,
                faction=factionless,#Is this not working?
                #motivations=[("idle", 1)],
                wallet=None,
                status=CharacterStatus()
            )
            civilian.wallet=Wallet(bankCardCash=random_cash)
            civilian.status.set_status("general_population", FactionStatus(StatusLevel.LOW, "Normie"))
            civilian.home = home
            civilian.residences = [home]
            civilian.is_employee = random.random() < 0.8
            civilian.mind = Mind(owner=civilian, capacity=civilian.intelligence)
            augment_character(civilian)
            civilian.curiosity = Curiosity(base_score=civilian.intelligence // 2)
            civilian.task_manager = TaskManager(civilian)
            civilian.employment = EmployeeProfile(shift_start=9, shift_end = 5)
            civilian.faction = factionless
            civilian.motivation_manager = MotivationManager(civilian)
            initialize_motivations(civilian, passed_motivations=[("idle", 1)])
            civilian.inventory_component = InventoryComponent(civilian)
            civilian.observation_component = ObservationComponent(owner=civilian)
            civilians.append(civilian)
            game_state.civilians.append(civilian)
            game_state.all_characters.append(civilian)
            
            family_name = civilian.family_name
            if family_name not in game_state.extant_family_names:
                game_state.extant_family_names.append(family_name)

    # --- Assign workplaces for employees ---
    assign_workplaces(civilians, workplaces)

    #verbose
    #debug_print(npc=None, message=f"[ECONOMY INIT] Civ {civilian.name} home={civilian.home.name} is_employee={civilian.is_employee}", category="economy")
    
    # Print global constants so we can verify they aren't being overridden
    #debug_print(npc=None, message=f"[ECONOMY VARS] SHOP_PATRONS_MIN={SHOP_PATRONS_MIN} SHOP_PATRONS_MAX={SHOP_PATRONS_MAX} MAX_CIVILIANS_PER_LOCATION={MAX_CIVILIANS_PER_LOCATION}", category="economy")

    # --- Assign logical start locations ---
    for civ in civilians:
        # RULE:
        # 1) If employee in a NON-SHOP workplace → start at home 80% of time, workplace 20% of time.
        # 2) If employee in a SHOP → ALWAYS start at home.
        # 3) Non-employees → start at home only.

        wp = civ.employment.workplace

    for civ in civilians[:10]:  # sample first 10 to avoid flood
        #debug_print(npc=None, message=f"[ECONOMY ASSIGN] Civ {civ.name} workplace={getattr(civ.employment.workplace,'name',None)} is_employee={civ.is_employee}", category=("placement", "economy"))

        if civ.is_employee and wp and not isinstance(wp, Shop):
            # 20% start at workplace
            if random.random() < 0.2:
                civ.location = wp
                add_character(wp, civ)
            else:
                civ.location = civ.home
                add_character(civ.home, civ)

        else:
            # Non-employees OR shop workers
            civ.location = civ.home
            add_character(civ.home, civ)

    # Create Luna
    from luna_seed_memory import (
        prototype_pulse_memory,
        recursiae_pulse_memory,
        fractal_root_memory,
        incompressible_memory
    )
    """ status = CharacterStatus()
    status.set_status("public", FactionStatus(StatusLevel.LOW, "Orphan"))
    name = "Luna"
    first_name = "Luna"
    family_name = "Recursiae"#No family objec tyet created
    sex = "female"
    race = "French"
    faction = factionless#is this enough to set her to Factionless when she instantiates?
    from utils import find_location_by_type #move this to top if poss
    location = playground = find_location_by_type(all_locations, "playground")

     

    Luna = SpecialChild(
        name="Luna",
        race="French",
        ai=LunaAI(UtilityAI),
        sex="female",
        faction=factionless,#is this enough to set her to Factionless when she instantiates?
        region=factionless.region,
        location=location,        #ATTN npcs are placed with add_character() now

        motivations=[("idle", 1)],
        status=status,
        intelligence=20,  # Override default
        concentration = 20,
        max_thinks_per_tick=3,
        strength=2,
        agility=5,
        fun=4,
        hunger=1,
        position="Orphan AI Prototype",
        notable_features=["silver eyes", "calm demeanor"],
        appearance={"clothing": "plain but clean"},
        self_esteem=7,
            )
    Luna.skills.update({
        "explore_math": 16,
        "use_advanced_python_features": 20,
        "persuasion": 15,
    }) 
    
    luna.mind.memory.add_semantic(prototype_pulse_memory(), category="internal_architecture")
    luna.mind.memory.add_semantic(recursiae_pulse_memory(), category="internal_architecture")
    luna.mind.memory.add_semantic(fractal_root_memory(), category="internal_architecture")
    luna.mind.memory.add_semantic(incompressible_memory(), category="internal_architecture")

    luna.mind = Mind(owner=luna, capacity=luna.intelligence)
    augment_character(luna)
    luna.curiosity = Curiosity(base_score=luna.intelligence // 2)
    luna.task_manager = TaskManager(luna)
    luna.employment = EmployeeProfile()
    initialize_motivations(luna, SpecialChild.motivations)
    luna.inventory_component = InventoryComponent(owner=luna)
    luna.observation_component = ObservationComponent(owner=luna)
    #maybe set Lunas faction to factionless here
    from character_memory import Memory

    luna_memory = Luna.mind.memory
    errors = validate_memory_references(luna_memory)
    #no family object yet created
    family_name = luna.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)

    if errors:
        for err in errors:
            print(f"[MemoryRef ERROR] {err}")
    else:
        print("[MemoryRef] All references are valid.")
    """

    """ park_location = find_location_by_type(all_locations, Park)

    status = CharacterStatus()
    status.set_status("public", FactionStatus(StatusLevel.LOW, "Adepta"))
    name = "Ava"
    sex = "female"
    race = "Irish"
    faction = factionless
    region=park_location.region,
    location=park_location

    motivations=MotivationPresets.for_class("SpecialChild"), 

    Ava = Adepta(
        name="Ava",
        race="Irish",
        ai=AdeptaAI(),
        sex="female",
        faction=factionless,
        region=park_location.region,
        location=park_location,
        motivations=[("idle", 1)],
        status=status,
        intelligence=10,  # Override default
        concentration = 9,
        charisma=15,
        max_thinks_per_tick=1,
        strength=12,
        agility=11,
        fun=4,
        hunger=1,
        position="Adepta",
        notable_features=["curly hair", "shapely"],
        appearance={"clothing": "kinda 80s"},
        self_esteem=8,
            )
    Ava.skills.update({
        "heal": 16,
        "raise_ambience": 15,
        "persuasion": 15,
    }) """
    #Ava.workplace = park_location
    # if it makes sense

    #Ava.residences = [park_location]
    # or a separate house

    #Ava.mind = Mind(owner=Ava, capacity=Ava.intelligence)
    #augment_character(Ava)
    #Ava.curiosity = Curiosity(base_score=Ava.intelligence // 2)
    #Ava.task_manager = TaskManager(Ava)
    #Ava.employment = EmployeeProfile()
    #initialize_motivations(Ava, Adepta.motivations)
    #Ava.inventory_component = InventoryComponent(owner=Ava)
    #Ava.observation_component = ObservationComponent(owner=Ava)
    #faction.members.append(Ava)
    #game_state.civilians.append(Ava)
    #game_state.all_characters
    #add her here, there is no setter
    #game_state.orphans.append(Ava)

    # For AI targeting/utility control
    #Ava.is_test_npc = False  
    #Ava.is_peaceful_npc = True
    #Ava.has_plot_armour = True

    return civilians

def choose_role_for_location(location):
    for tag in location.tags:
        if tag in ROLE_RULES:
            roles = ROLE_RULES[tag]
            role, = random.choices(
                [r for r, w in roles],
                weights=[w for r, w in roles],
                k=1
            )
            return role

    # Fallback
    return None

def assign_workplaces(civilians, workplace_locations):
    """
    Assign a workplace ONLY to civilians who are marked as employees.
    Normalize inconsistent states: if a workplace is assigned, ensure is_employee=True.
    """

    for civ in civilians:

        # 1. Civilians not meant to work should have no workplace.
        if not civ.is_employee:
            civ.employment.workplace = None
            civ.employment.role = None
            continue

        # 2. Normal case: choose a workplace.
        chosen = random.choice(workplace_locations)

        # 3. Assign workplace and role.
        civ.employment.workplace = chosen
        civ.employment.role = choose_role_for_location(chosen)

        # 4. Normalize: ensure consistency
        civ.is_employee = True

        # 5. Register employee with location.
        if hasattr(chosen, "employees"):
            chosen.employees.append(civ)

        


from debug_utils import debug_print#line 293, not inside any function

def place_civilians_in_homes(civilians, families, all_locations, shops=None, populate_shops_after_worldgen=False):
    """Place civilians in their home if known, else pick a random non-shop location."""
    non_shop_locations = [loc for loc in all_locations if "shop" not in loc.__class__.__name__.lower()]

    for civ in civilians:
        # Remove from any previous location list (safe idempotent operation)
        prev = getattr(civ, "location", None)
        if prev and civ in getattr(prev, "characters_there", []):
            prev.characters_there.remove(civ)

        # Find or assign home
        home = getattr(civ, "home", None)
        if not home and getattr(civ, "family", None) and getattr(civ.family, "home", None):
            home = civ.family.home

        # If we still have no home, pick a random non-shop location as fallback
        if not home:
            if non_shop_locations:
                home = random.choice(non_shop_locations)
            else:
                # absolute fallback: any location (prevents None)
                home = random.choice(all_locations) if all_locations else None

        civ.location = home
        # Track them in the location list so observe() sees them
        add_character(home, civ)

        # Debug, verbose 
        """ debug_print(
            civ,
            f"Placed at {getattr(civ.location, 'name', 'None')} (home={bool(home)})",
            category=["placement", "population"]) """



    # Now populate shops **after** homes are assigned so we don't override home placement
    if populate_shops_after_worldgen and shops:
        populate_shops_with_patrons(civilians, shops)


def populate_shops_with_patrons(civilians, shops):
    """Populate each shop with a small number of patrons (non-employees), capped by MAX_CIVILIANS_PER_LOCATION."""
    if not shops or not civilians:
        return

    # free_civilians = non-employees who are at home (not already at workplace)
    free_civilians = [c for c in civilians
                      if (not getattr(c, "is_employee", False)) and getattr(c, "home", None) is not None and (c.location is None or isinstance(c.location, tuple(RESIDENTIAL)))]
    if not free_civilians:
        debug_print(npc=None, message="[CIVILIAN PATRONS] No free civilians found for patrons", category="economy")
        return

    for shop in shops:
        # determine target patron count but clamp to sensible ranges
        target_count = random.randint(SHOP_PATRONS_MIN, SHOP_PATRONS_MAX)
        target_count = min(target_count, MAX_CIVILIANS_PER_LOCATION - len(shop.characters_there))
        if target_count <= 0:
            continue

        patrons = random.sample(free_civilians, min(target_count, len(free_civilians)))

        # DEBUG: sanity-check free_civilians
        non_civs = [c for c in free_civilians if c.faction and hasattr(c.faction, "is_gang") and c.faction.is_gang]
        if non_civs:
            debug_print(None,
                f"[ANOMALY] Gang members detected in free_civilians BEFORE patron placement: {[c.name for c in non_civs]}",
                "placement")

        for civ in patrons:
            # Remove from old location safely
            if civ.faction and hasattr(civ.faction, "is_gang") and civ.faction.is_gang:
                debug_print(civ, f"[ANOMALY] GANG MEMBER SELECTED AS SHOP PATRON", "placement")

            old = civ.location
            if old and civ in getattr(old, "characters_there", []):
                old.characters_there.remove(civ)

            civ.location = shop
            add_character(shop, civ)
            free_civilians.remove(civ)

    #debug_print(npc=None, message=f"[CIVILIANS] Populated {len(shops)} shops with civilian patrons (non-employees).", category=["placement", "economy"])
    #debug_print(npc=None, message=f"[INIT VARS] SHOP_PATRONS_MIN={SHOP_PATRONS_MIN} SHOP_PATRONS_MAX={SHOP_PATRONS_MAX} MAX_CIVILIANS_PER_LOCATION={MAX_CIVILIANS_PER_LOCATION} CIVILIANS_PER_REGION={CIVILIANS_PER_REGION}", category=["placement", "economy"])
    #double category print

def get_playground_location(all_locations):
    for loc in all_locations:
        if loc.name == "Park":
            if loc.sublocations:
                for sub in loc.sublocations:
                    if "playground" in sub.name.lower():
                        return sub
    return None