#createLocations.py
from location import MunicipalBuilding, Shop, Region, Location, House, ApartmentBlock
from base_classes import Location
from typing import List
from create_game_state import get_game_state
from utils import get_region_by_name
from location_types_by_wealth import LocationTypes
from location_types import RESIDENTIAL
from InWorldObjects import SmartPhone, Size, Item
from weapons import Pistol
from shop_name_generator import generate_shop_name, guess_specialization_from_inventory
from create_game_state import get_game_state
from debug_utils import debug_print
import random

def create_locations(region: Region, wealth: str) -> List[Location]:
    """Creates and returns a list of location objects for a region based on its wealth level."""
    locations = []
    game_state = get_game_state()

    # Get list of location classes for this wealth level
    location_types = LocationTypes.location_types_by_wealth.get(wealth, [])

    for location_class, count in location_types:
        for _ in range(count):
            try:
                loc = location_class(region=region, name=location_class.__name__)
                locations.append(loc)
            except Exception as e:
                debug_print(
                    npc=None,
                    message=(
                        f"⚠️ Failed to instantiate {location_class.__name__} "
                        f"in region '{region.name}': {e}"
                    ),
                    category="create"
                )

        # -------------------------
        # 2. RESIDENTIAL SAFETY PASS
        # Ensures every region has enough homes for civilian placement
        # -------------------------
        residential_locs = [loc for loc in locations if isinstance(loc, RESIDENTIAL)]

        # Minimum basic housing
        MIN_HOUSES = 4
        MIN_APARTMENTS = 2

        houses_needed = max(0, MIN_HOUSES - sum(isinstance(l, House) for l in residential_locs))
        apartments_needed = max(0, MIN_APARTMENTS - sum(isinstance(l, ApartmentBlock) for l in residential_locs))

        for _ in range(houses_needed):
            try:
                h = House(region=region, name="Family House")
                locations.append(h)
            except Exception as e:
                debug_print(None, f"⚠️ Error creating House in {region.name}: {e}", "create")

        for _ in range(apartments_needed):
            try:
                block = ApartmentBlock(region=region, name="Mass Housing")
                locations.append(block)
            except Exception as e:
                debug_print(None, f"⚠️ Error creating ApartmentBlock in {region.name}: {e}", "create")


    # 3. Shop naming + inventory injection
    # -------------------------
    shops = [loc for loc in locations if hasattr(loc, "inventory") and hasattr(loc, "is_shop")]
    
    for shop in shops:
        specialization = guess_specialization_from_inventory(shop.inventory)
        shop.name = generate_shop_name(specialization=specialization, ownership="family")
        shop.inventory.owner = shop
        debug_print(None, "[TRACE] About to run shop stocking block", "create")#added

        try:
            shop.inventory.add_item(SmartPhone(price=200, quantity=5))
            shop.inventory.add_item(Pistol(price=500, quantity=2))
            debug_print(None, f"[DEBUG] Stocked {shop.name} with SmartPhones and Pistols.", category="create")
            debug_print(None, f"[VERIFY] {shop.name} inventory: {shop.inventory.get_inventory_summary()}", category="verify")
        except Exception as e:
            debug_print(None, f"⚠️ Error stocking shop '{shop.name}': {e}", "create")


    # -------------------------
    # 4. Add Municipal Building
    # -------------------------
    from location import MunicipalBuilding

    try:
        municipal = MunicipalBuilding(
            region=region,
            name="Municipal Building",
            tags=["government", "law", "tax"]
        )
        locations.append(municipal)
        region.add_location(municipal)

        game_state.municipal_buildings[region.name] = municipal

    except Exception as e:
        debug_print(None, f"⚠️ Error creating MunicipalBuilding in {region.name}: {e}", "create")

    # -------------------------
    # 5. Final bookkeeping
    # -------------------------
    region.locations = locations
    region.shops = [loc for loc in locations if hasattr(loc, "is_shop")]

    # Maintain global lists
    if not hasattr(game_state, "all_shops"):
        game_state.all_shops = []
    game_state.all_shops.extend(region.shops)

    if not hasattr(game_state, "all_locations"):
        game_state.all_locations = []
    game_state.all_locations.extend(locations)

    return locations

def add_location(self, location: Location):
    location.region = self
    self.locations.append(location)
    #dont forget to add to region and RegionKnowledge (perhaps via gossip)
    game_state = get_game_state()
    get_game_state().all_locations.append(location)
    if hasattr(game_state, "all_locations"):
        #game_state.all_locations.append(location) #← legacy
        game_state.location_registry.register(location)  # ← new