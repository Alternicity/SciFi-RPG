#augment.augmentLocations.py

import random
from random import randint
from create.create_game_state import get_game_state
from debug_utils import debug_print
game_state = get_game_state()
from base.location import CommercialLocation
from region.region_flavor import REGION_CULTURAL_ADJECTIVES as REGIONAL_FLAVOR
from location.locations import Cafe, Restaurant, Library, Park, LunaSanctum, SportsCentre, Factory, Powerplant, Nightclub
from objects.food.prepared_food import Sandwich, Burger
from objects.furniture import CafeChair, CafeTable, CafeCounter, Table, Chair
from objects.InWorldObjects import Pot, CashRegister, Toughness, ItemType, Size
from objects.trees_and_plants import GoldenRatioTree, Plant, Tree, OakTree, DustPalm, EchoWillow
from objects.trees_and_plants import BonsaiTree
from base.location import Location, Sublocation

DEFAULT_SPECIALIZATION = "general"

SUPPORTED_SPECIALIZATIONS = [
    "weapon", "electronics", "medical", "tools", "luxury", "general"
]

SHOP_TYPES = {#not used, and overalps with SPECIALIZATION_KEYWORDS
    "weapon": ["Arms", "Armory", "Firearms", "Guns", "Ballistics"],
    "electronics": ["Tech", "Electronics", "Circuitry", "Gadgets"],
    "pharmacy": ["Pharma", "Health", "Meds", "FirstAid"],
    "general": ["Goods", "Mart", "Store", "Depot"],
    "tools": ["Workshop", "Tools", "Repairs", "Fixers"],
}

#REGIONAL_FLAVOR = REGION_CULTURAL_ADJECTIVES

""" REGIONAL_FLAVOR = {
    "northville": ["Northern", "Breezy"],
    "southville": ["Southern", "Dusty"],
    "easternhole": ["Eastern", "Hollow"],
    "westborough": ["Western", "Borough"],
    "downtown": ["Metro", "Central"]
} """

SPECIALIZATION_KEYWORDS = {#apparently not used in this file, or anywhere, yet. Either it or SHOP_TYPES is probably best removed
    "weapon": ["Arms", "Guns", "Weapons", "Armory"],
    "electronics": ["Circuits", "Gadgets", "Tech", "Devices"],
    "medical": ["Meds", "Pharma", "Health", "Remedy"],
    "mechanical": ["Gears", "Tools", "Fixit", "Workshop"],
    "electrical": ["Volts", "Electro", "Power", "Current"]
}

spec_suffixes = ["Armory", "Emporium", "Outlet", "Depot", "Mart", "Bazaar", "Vault", "Shop", "Store"]
family_surnames = game_state.extant_family_names
# augment/augment_locations.py

def assign_location_names(all_locations):
    from world.location_names import LIBRARY_NAMES, PARK_NAMES, generate_cafe_name
    
    lib_names = list(LIBRARY_NAMES)
    park_names = list(PARK_NAMES)
    
    for loc in all_locations:
        if isinstance(loc, Library) and loc.name == "Public Library":
            if lib_names:
                loc.name = lib_names.pop(0)
        elif isinstance(loc, Park) and loc.name == "Green Park":
            if park_names:
                loc.name = park_names.pop(0)
        elif isinstance(loc, Cafe) and loc.name == "Metro Cafe":
            loc.name = generate_cafe_name()

def assign_location_ownership(all_locations, all_corporations):
    """Assign corporations to commercial locations that lack owners."""
    from economy.economy_queries.location_queries import get_location_owner
    from economy.economy_helpers import assign_location_owner
    
    sports_centres = [loc for loc in all_locations if isinstance(loc, SportsCentre)]
    
    if not all_corporations:
        return
    
    for loc in sports_centres:
        if get_location_owner(loc) is None:
            corp = random.choice(all_corporations)
            #loc.owner = corp
            assign_location_owner(
                loc,
                corp
            )

            # Name derives from owner
            loc.name = f"{corp.name} Arena"
            


def seed_park_objects(all_locations):
    
    for loc in all_locations:
        if not isinstance(loc, Park):
            continue
        if isinstance(loc, LunaSanctum):
            continue  # Luna's park gets seeded separately. Unique sublocation to be later incorprated

        if any(isinstance(o, Tree) for o in loc.items.objects_present):#added
            continue  # already seeded
            #But will this mean that the park ends up with exactly 1 tree?
        # Trees
       # 2-3 mundane trees
        mundane = [OakTree, DustPalm]
        for i, cls in enumerate(random.choices(mundane, k=3)):
            tree = cls()
            tree.name = f"{tree.name} {i+1}"
            tree.location = loc
            loc.items.objects_present.append(tree)

        # One special tree — sometimes GoldenRatio, sometimes EchoWillow
        special_cls = random.choice([GoldenRatioTree, EchoWillow])
        special = special_cls()
        special.location = loc
        loc.items.objects_present.append(special)

        # Benches
        for i in range(4):
            bench = Chair(name=f"Park Bench {i+1}")
            bench.location = loc
            loc.items.objects_present.append(bench)

        loc.fun = min(8, 1 + sum(
            getattr(t, "resonance_factor", 1.0)
            for t in loc.items.objects_present
            if isinstance(t, Tree)
        ))

        # One special tree
        """ spiral = GoldenRatioTree()
        loc.items.objects_present.append(spiral) """

        # Ambient boost from trees


def seed_library_furniture(all_locations):
    for loc in all_locations:
        if not isinstance(loc, Library):
            continue
        if any(isinstance(o, Table) for o in loc.items.objects_present):
            continue  # already seeded

        for t in range(4):  # 4 reading tables
            table = Table(
                name=f"Reading Table {t+1}",
                size=Size.LARGE,
                seating_capacity=2,  # intimate, focused
                toughness=Toughness.DURABLE,
            )
            table.location = loc
            table.region = loc.region
            loc.items.objects_present.append(table)

            for c in range(2):
                chair = Chair(name=f"Reading Chair {t+1}-{c+1}")
                chair.table = table
                chair.location = loc
                table.chairs.append(chair)
                loc.items.objects_present.append(chair)

def seed_library_books(all_locations):
    from world.books_catalogue import LIBRARY_COLLECTION
    for loc in all_locations:
        if not isinstance(loc, Library):
            continue
        for book in LIBRARY_COLLECTION:
            loc.items.objects_present.append(book)

def rename_powerplants():

    game_state = get_game_state()

    for loc in game_state.all_locations:

        if not isinstance(loc, Powerplant):
            continue

        region_name = (
            loc.region.name.capitalize()
            if loc.region else "Unknown"
        )

        if loc.owner:
             loc.name = f"{loc.owner.name} Powerplant ({loc.region.name})"

def rename_factories():

    game_state = get_game_state()

    used_names = set()

    for loc in game_state.all_locations:

        if not isinstance(loc, Factory):
            continue

        region_name = (
            loc.region.name.capitalize()
            if loc.region else "Unknown"
        )

        if loc.owner:
            base_name = (f"{loc.owner.name} Factory ({loc.region.name})")

        else:

            base_name = (
                f"{region_name} Factory"
            )

        name = base_name
        counter = 2

        while name in used_names:
            name = f"{base_name} {counter}"
            counter += 1

        loc.name = name
        used_names.add(name)

def rename_nightclubs():
    from data.Names.nightclub_names import NIGHTCLUB_NAMES
    game_state = get_game_state()

    used_names = set()

    clubs = [
        loc for loc in game_state.all_locations
        if isinstance(loc, Nightclub)
    ]

    random.shuffle(NIGHTCLUB_NAMES)

    for i, club in enumerate(clubs):

        if i < len(NIGHTCLUB_NAMES):
            name = NIGHTCLUB_NAMES[i]
        else:
            name = f"Nightclub {i+1}"

        while name in used_names:
            name += " X"

        club.name = name

        used_names.add(name)

def reassign_shop_names_after_character_creation():
    game_state = get_game_state()
    all_shops = game_state.all_shops
    family_pool = list(game_state.extant_family_names)

    #debug_print(None, f"[DEBUG] extant_family_names={game_state.extant_family_names}", "economy")

    if not family_pool:
        debug_print(None, "[WARN] No extant family names exist; shop renaming skipped.", "economy")
        return

    used_names = set()

    #debug_print(None, f"[INFO] Reassigning names for {len(all_shops)} shops.", "shops")

    for shop in all_shops:

        if not shop.name.startswith("Generic"):
            continue  # Only rename placeholder names

        # 1. Choose unused family name

        available = [f for f in family_pool if f not in used_names]
        if not available:
            available = family_pool  # fallback, allow reuse

        family = random.choice(available)
        used_names.add(family)

        # 2. Determine region flavor

        region_name = shop.region.name if shop.region else "Unknown"
        region_flavor_list = REGIONAL_FLAVOR.get(region_name, [])
        flavor = random.choice(region_flavor_list) + " " if region_flavor_list and random.random() < 0.4 else ""

        # 3. Determine suffix based on specialization

        spec_suffix = {
            "weapon": "Guns",
            "electronics": "Electrics",
            "medical": "Meds",
            "tools": "Hardware",
            "luxury": "Finery",
            "general": "Store",
        }.get(shop.specialization, "Store")

        # 4. Assign final name
        shop.name = f"{family}'s {flavor}{spec_suffix}"
        #debug_print(None, f"Renamed shop → {shop.name}", "shops")


def seed_food_locations(all_locations):
    for loc in all_locations:
        if isinstance(loc, Cafe):
            sandwich = Sandwich(quantity=5)
            burger = Burger(quantity=3)

            loc.items_available.extend([sandwich, burger])

def seed_commercial_equipment(all_locations):
    for loc in all_locations:
        if not isinstance(loc, CommercialLocation):
            continue

            #Objects like CashRegister lives in loc.items.objects_present

        if any(isinstance(o, CashRegister) for o in loc.items.objects_present):
            continue

        register = CashRegister(
            name=f"{loc.name} Register",
            toughness=Toughness.DURABLE,
            item_type=ItemType.GADGET,
            size=Size.MEDIUM,
            blackmarket_value=200,
            initial_cash=getattr(loc, "register_initial_cash", 300),
        )

        loc.items.objects_present.append(register)
        loc.cash_register = register  # optional convenience pointer




def seed_ambience_objects(all_locations):
    for loc in all_locations:
        if isinstance(loc, Cafe):
            # Prevent duplicate ambience
            if any(isinstance(o, Pot) for o in loc.items.objects_present):
                continue

            pot = Pot(quantity=1)
            bonsai = BonsaiTree()
            pot.add(bonsai)
            loc.items.objects_present.append(pot)


from objects.furniture import CafeTable, CafeChair
from location.locations import Cafe

def seed_nightclub_furniture(all_locations):
    from objects.sports_objects import PoolBall, PoolCue, PoolTable

    #tmp
    from perception.perceptibility import PerceptibleMixin


    for loc in all_locations:
        if not isinstance(loc, Nightclub):
            continue
            #see some  LargeTable, Sofa, Barstool, CafeChair objects, ClubBar, PoolTable
            #if club has tag "classy" then also some plants in vases
            #if it has tag: pool, add PoolTable

        

        tables = []

        for t in range(8):
            table = CafeTable(name=f"Table {t+1}")
            table.location = loc
            table.region = loc.region

            loc.items.objects_present.append(table)
            tables.append(table)

            # Add 8 chairs per table. Later incorporate sofas on one side instead
            for c in range(8):
                chair = CafeChair(name=f"Chair {t+1}-{c+1}")
                chair.location = loc
                chair.region = loc.region
                chair.table = table
                table.chairs.append(chair)#Club tables will have 8 places, 4 chairs along one side, and 2 small, or one
                #long sofa on the other side
                loc.items.objects_present.append(chair)

        loc.tables = tables


        if loc.has_tag("pool"):
            pool_table = PoolTable()
            pool_table.location = loc
            pool_table.region = loc.region

            loc.items.objects_present.append(pool_table)

        dancefloor = Sublocation(
            name="Dancefloor",
            perceptible_from_parent=True
        )

        dancefloor.parent_location = loc
        dancefloor.region = loc.region
        dancefloor.accessible_roles = []
        loc.sublocations.append(dancefloor)
        

        dj_booth = Sublocation(
            name="DJ Booth",
            perceptible_from_parent=True
        )

        dj_booth.parent_location = loc
        dj_booth.region = loc.region
        dj_booth.accessible_roles = ["DJ"]
        loc.sublocations.append(dj_booth)

        vip_lounge = Sublocation(
            name="VIP Lounge",
            perceptible_from_parent=True
        )
        vip_lounge.parent_location = loc
        vip_lounge.region = loc.region
        vip_lounge.accessible_roles = ["VIP", "Babe"]
        loc.sublocations.append(vip_lounge)

        if loc.has_tag("classy"):#tag doesnt exist yet
                add_classy_plants(vip_lounge)

        entry_booth = Sublocation(
            name="Entry Booth",
            perceptible_from_parent=True
        )
        entry_booth.parent_location = loc
        entry_booth.region = loc.region
        entry_booth.accessible_roles = ["Staff"]
        loc.sublocations.append(entry_booth)

        #tmp
        if isinstance(loc, Nightclub):
            for sub in loc.sublocations:
                print(
                    sub.name,
                    isinstance(sub, PerceptibleMixin),
                    getattr(sub, "is_perceptible", None)
                )

def add_classy_plants(loc):
    count = random.randint(2, 5)

    for _ in range(count):
        pot = Pot()
        tree = GoldenRatioTree()
        pot.add(tree)
        pot.location = loc
        pot.region = loc.region
        loc.items.objects_present.append(pot)#not added to vip area
        #But nor can any npc enter a sublocation yet.









#reference for above
def seed_cafe_furniture(all_locations):
    for loc in all_locations:
        if not isinstance(loc, Cafe):
            continue

        # Avoid duplicate seeding
        if any(isinstance(o, CafeTable) for o in loc.items.objects_present):
            continue

        tables = []

        for t in range(8):
            table = CafeTable(name=f"Table {t+1}")
            table.location = loc
            table.region = loc.region

            loc.items.objects_present.append(table)
            tables.append(table)

            # Add 4 chairs per table
            for c in range(4):
                chair = CafeChair(name=f"Chair {t+1}-{c+1}")
                chair.location = loc
                chair.region = loc.region
                chair.table = table
                table.chairs.append(chair)
                loc.items.objects_present.append(chair)

        loc.tables = tables  # optional reference for later AI logic

        # Add counter if not present
        if not any(isinstance(o, CafeCounter) for o in loc.items.objects_present):
            counter = CafeCounter()
            counter.location = loc
            counter.region = loc.region

            loc.items.objects_present.append(counter)
            loc.counter = counter


""" park_sublocs = [Playground(), Storeroom()]
nightclub_sublocs = [DanceFloor(), Storeroom(), Office()] """


def seed_sports_centre_equipment(all_locations):
    from objects.sports_objects import PoolTable, BowlingLane, PoolCue
    from location.locations import SportsCentre

    for loc in all_locations:
        if not isinstance(loc, SportsCentre):
            continue
        if any(isinstance(o, PoolTable) for o in loc.items.objects_present):
            continue  # already seeded

        # 2 pool tables
        for i in range(1, 3):
            table = PoolTable(name=f"Pool Table {i}")
            table.location = loc
            table.region = loc.region
            loc.items.objects_present.append(table)
            # Add cues to location inventory too
            for cue in table.cues:
                cue.location = loc
                loc.items.objects_present.append(cue)

        # 3 bowling lanes
        for i in range(1, 4):
            lane = BowlingLane(lane_number=i)
            lane.location = loc
            lane.region = loc.region
            loc.items.objects_present.append(lane)

        # Boost fun value from equipment
        loc.fun = 4

def seed_residential_furniture(all_locations):
    from objects.furniture import Bed
    from location.locations import House, ApartmentBlock

    for loc in all_locations:
        if not isinstance(loc, (House, ApartmentBlock)):#stopgap until sublocations exist.
            continue
        if any(isinstance(o, Bed) for o in loc.items.objects_present):
            continue

        if isinstance(loc, House):
            beds = 2
        else:
            beds = 4  # shared block — multiple beds until sublocations exist

        for i in range(beds):
            bed = Bed(name=f"Bed {i+1}")
            bed.location = loc
            bed.region = loc.region
            loc.items.objects_present.append(bed)

def seed_residential_food(all_locations):
    from location.locations import House, ApartmentBlock
    from objects.food.prepared_food import Sandwich, Burger
    #Lets put 2x Sandwich and 2 x Burger in each fridge
    #ApartmentBlock will be an edge case, as sublocations are not yet developed
    #So apartments dont exist

    