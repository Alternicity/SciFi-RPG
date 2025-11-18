#createCivilians.py
import random
import collections
import math
from base_classes import Character, Factionless
from location import Shop, Region, Park
from location_types import WORKPLACES, PUBLIC_PLACES, RESIDENTIAL
from characters import Civilian, SpecialChild, Adepta
from InWorldObjects import Wallet
from motivation_presets import MotivationPresets
from status import CharacterStatus, FactionStatus, StatusLevel
from ai_civilian import AdeptaAI
from utils import normalize_location_regions, get_region_for_location, find_location_by_type
from city_vars import CIVILIANS_PER_REGION, SHOP_PATRONS_MIN, SHOP_PATRONS_MAX, MAX_CIVILIANS_PER_LOCATION
from debug_utils import debug_print, add_character

def create_civilian_population(all_locations, all_regions, factionless, num_civilians=None):#30
    """Generate civilians and assign them logical locations."""
    from create_character_names import create_name
    from create_game_state import get_game_state
    game_state = get_game_state()

    normalize_location_regions(all_locations, all_regions)  # 🧹 Ensure valid region refs

    civilians = []
    valid_races = Character.VALID_RACES
    race_pool = ["Terran"] * 5 + [race for race in valid_races if race != "Terran"]

    # Categorize locations
    homes = [loc for loc in all_locations if isinstance(loc, RESIDENTIAL)]
    workplaces = [loc for loc in all_locations if isinstance(loc, tuple(WORKPLACES))]
    public_spaces = [loc for loc in all_locations if isinstance(loc, PUBLIC_PLACES)]
    shops = [loc for loc in all_locations if isinstance(loc, Shop)]
    
    if not homes:
        raise ValueError("❌ No residential locations found for civilian placement.")
    if not workplaces:
        print("⚠️ No workplaces found. Civilians will start at home only.")

    civilians_per_region = num_civilians or CIVILIANS_PER_REGION

    # --- Region-based creation ---
    for region in all_regions:
        for _ in range(civilians_per_region):
            race = random.choice(race_pool)
            gender = random.choice(["male", "female"])
            name = create_name(race, gender)
            random_cash = random.randint(5, 500)

        # Assign home
            home = random.choice(homes)
            region_for_home = get_region_for_location(home, all_regions)
            if not region_for_home:
                print(f"⚠️ Skipping {name}: home {home.name} has no region.")
                continue

            # Motivation setup
            motivations = MotivationPresets.for_class("Civilian")

            # Base character
            civilian = Civilian(
                name=name,
                region=region_for_home,
                sex=gender,
                location=None,  # Assigned later
                race=race,
                faction=factionless,
                motivations=motivations,
                wallet=Wallet(bankCardCash=random_cash),
                status=CharacterStatus()
            )

            civilian.status.set_status("general_population", FactionStatus(StatusLevel.LOW, "Normie"))
            civilian.home = home
            civilian.residences = [home]
            civilian.is_employee = random.random() < 0.8
            civilian.workplace = None
            civilian.is_working = False
            civilian.shift = "day"

            civilians.append(civilian)
            game_state.civilians.append(civilian)
            game_state.all_characters.append(civilian)

    # --- Assign workplaces for employees ---
    assign_workplaces(civilians, workplaces, shops)

    #verbose
    debug_print(npc=None, message=f"[ECONOMY INIT] Civ {civilian.name} home={civilian.home.name} is_employee={civilian.is_employee}", category="economy")
    for civ in civilians[:10]:  # sample first 10 to avoid flood
        debug_print(npc=None, message=f"[ECONOMY ASSIGN] Civ {civ.name} workplace={getattr(civ.workplace,'name',None)} is_employee={civ.is_employee}", category="economy")

    # Print global constants so we can verify they aren't being overridden
    debug_print(npc=None, message=f"[ECONOMY VARS] SHOP_PATRONS_MIN={SHOP_PATRONS_MIN} SHOP_PATRONS_MAX={SHOP_PATRONS_MAX} MAX_CIVILIANS_PER_LOCATION={MAX_CIVILIANS_PER_LOCATION}", category="economy")

    # --- Assign logical start locations ---
    # --- Assign logical start locations ---
    for civ in civilians:
        # RULE:
        # 1) If employee in a NON-SHOP workplace → start at home 80% of time, workplace 20% of time.
        # 2) If employee in a SHOP → ALWAYS start at home.
        # 3) Non-employees → start at home only.

        if civ.is_employee and civ.workplace and not isinstance(civ.workplace, Shop):
            if random.random() < 0.2:  # 20% chance they start at work
                civ.location = civ.workplace
                add_character(civ.workplace, civ)
            else:
                civ.location = civ.home
                add_character(civ.home, civ)
        else:
            civ.location = civ.home
            add_character(civ.home, civ)
            

        #civ.location.characters_there.append(civ)
        #I just commented this out as it is duplicated below

        """ Shops no longer get employees at worldgen
        But civilians still have a workplace for later simulation
        Shops will only get patrons from later systems, not 3 pipelines at once """


        if civ.location:
            civ.location.characters_there.append(civ)

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
    sex = "female"
    race = "French"
    faction = factionless
    from utils import find_location_by_type #move this to top if poss
    location = playground = find_location_by_type(all_locations, "playground")

    motivations=MotivationPresets.for_class("SpecialChild"), 

    Luna = SpecialChild(
        name="Luna",
        race="French",
        ai=LunaAI(UtilityAI),
        sex="female",
        faction=factionless,
        region=factionless.region,
        location=location,        #ATTN npcs are placed with add_character() now

        motivations=motivations,
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

    from character_memory import Memory

    luna_memory = Luna.mind.memory
    errors = validate_memory_references(luna_memory)

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
        motivations=motivations,
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

def assign_workplaces(civilians, workplaces, shops):#line 253
    """Assign workplaces to civilians who are employees.
    - workplaces: list of location objects (excludes shops if you prefer)
    - shops: list of Shop objects (kept separate so we can treat employees vs patrons)
    """

    shop_index = 0
    for civ in civilians:
        if civ.is_employee:
            # 80% employee assignment probability exists, but assignment should be broad.
            available_wp = workplaces  # includes shops
            if not available_wp:
                continue

            # Balanced distribution
            chosen = available_wp[shop_index % len(available_wp)]
            shop_index += 1

            civ.workplace = chosen
            chosen.employees_there.append(civ)
            """ Employees now have the workplace assigned
            But are not placed inside it yet """
            #no need for a return here


from debug_utils import debug_print

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

        # Debug
        debug_print(
            civ,
            f"Placed at {getattr(civ.location, 'name', 'None')} (home={bool(home)})",
            category="placement"
        )
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

    debug_print(npc=None, message=f"[CIVILIANS] Populated {len(shops)} shops with civilian patrons (non-employees).", category="economy")
    debug_print(npc=None, message=f"[INIT VARS] SHOP_PATRONS_MIN={SHOP_PATRONS_MIN} SHOP_PATRONS_MAX={SHOP_PATRONS_MAX} MAX_CIVILIANS_PER_LOCATION={MAX_CIVILIANS_PER_LOCATION} CIVILIANS_PER_REGION={CIVILIANS_PER_REGION}", category="economy")


def get_playground_location(all_locations):
    for loc in all_locations:
        if loc.name == "Park":
            if loc.sublocations:
                for sub in loc.sublocations:
                    if "playground" in sub.name.lower():
                        return sub
    return None