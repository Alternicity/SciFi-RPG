#create.createLocations.py
from location.locations import MunicipalBuilding, Shop, Region, Location, House, ApartmentBlock
from base.location import Location
from base.character import Character
from typing import List
from create.create_game_state import get_game_state
from utils import get_region_by_name
from location.location_types_by_wealth import LocationTypes
from location.location_types import RESIDENTIAL
from location.security_setup import attach_default_security
from objects.InWorldObjects import SmartPhone, Size, Item
from weapons import Pistol
from shop_name_generator import generate_shop_name
import traceback
from debug_utils import debug_print
from augment.augmentLocations import seed_food_locations, seed_ambience_objects
game_state = get_game_state()

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

                attach_default_security(loc)
                locations.append(loc)
            except Exception as e:
                debug_print(
                    npc=None,
                    message=(
                        f"⚠️ Failed to instantiate {location_class.__name__} "
                        f"in region '{region.name}'\n"
                        f"  Exception type: {type(e).__name__}\n"
                        f"  Exception repr: {repr(e)}\n"
                        f"  Traceback:\n{traceback.format_exc()}"
                    ),
                    category="create"
                )

        # 2. RESIDENTIAL SAFETY PASS
        # Ensures every region has enough homes for civilian placement

        residential_locs = [loc for loc in locations if isinstance(loc, RESIDENTIAL)]

        # Minimum basic housing
        MIN_HOUSES = 4
        MIN_APARTMENTS = 2

        houses_needed = max(0, MIN_HOUSES - sum(isinstance(l, House) for l in residential_locs))
        apartments_needed = max(0, MIN_APARTMENTS - sum(isinstance(l, ApartmentBlock) for l in residential_locs))

        for _ in range(houses_needed):
            try:
                h = House(region=region, name="Family House")

                attach_default_security(h)
                locations.append(h)
            except Exception as e:
                debug_print(None, f"⚠️ Error creating House in {region.name}: {e}", "create")

        for _ in range(apartments_needed):
            try:
                block = ApartmentBlock(region=region, name="Mass Housing")
                attach_default_security(block)
                locations.append(block)
            except Exception as e:
                debug_print(None, f"⚠️ Error creating ApartmentBlock in {region.name}: {e}", "create")


    # 3. Shop naming + inventory injection

    shops = [loc for loc in locations if hasattr(loc, "inventory") and hasattr(loc, "is_shop")]
    
    for shop in shops:
        
        family_surnames = game_state.extant_family_names#family_surnames not accessed
        specialization = None
        shop.name = generate_shop_name(specialization=None, region_name=region.name,)
        shop.inventory.owner = shop

        try:
            shop.inventory.add_item(SmartPhone(price=200, quantity=1))
            shop.inventory.add_item(Pistol(price=500, quantity=1))

            specialization = guess_specialization_from_inventory(shop.inventory)
            shop.specialization = specialization
            #print shop stock injection
            #debug_print(None, f"[DEBUG] Stocked {shop.name} with SmartPhones and Pistols.", category="create")
            #debug_print(None, f"[VERIFY] {shop.name} inventory: {shop.inventory.get_inventory_summary()}", category="verify")
        except Exception as e:
            debug_print(None, f"⚠️ Error stocking shop, or adding specialization '{shop.name}': {e}", "create")

    # NO CORPORATE_STORE NAMING CALL, CODE EXISTS IN SHOP NAMING FILE

    # -------------------------
    # 4. Add Municipal Building
    # -------------------------
    from location.locations import MunicipalBuilding

    try:
        municipal = MunicipalBuilding(
            region=region,
            name="Municipal Building",
            tags=["government", "law", "tax"]
        )
        attach_default_security(municipal)
        locations.append(municipal)
        region.add_location(municipal)

        game_state.municipal_buildings[region.name] = municipal

    except Exception as e:
        debug_print(None, f"⚠️ Error creating MunicipalBuilding in {region.name}: {e}", "create")


    # 5. Final bookkeeping.

    region.locations = locations
    region.shops = [loc for loc in locations if hasattr(loc, "is_shop")]

    

    #all_locations.append(locations)
    #all_locations is marked as not defined
    #lets also add a temporary print here to show its size, or if it contains houses and apartment blocks
    # Maintain global lists
    if not hasattr(game_state, "all_shops"):
        game_state.all_shops = []
    game_state.all_shops.extend(region.shops)

    if not hasattr(game_state, "all_locations"):
        game_state.all_locations = []
    game_state.all_locations.extend(locations)


    #get the cafes and retaurants here, 
    seed_food_locations(game_state.all_locations)
    seed_ambience_objects(game_state.all_locations)

    return locations

#this function is a mess, but currently unused
def add_location(self, location: Location):
    location.region = self#what is this?
    self.locations.append(location)
    #dont forget to add to region and RegionKnowledge (perhaps via gossip)
    game_state = get_game_state()
    get_game_state().all_locations.append(location)
    if hasattr(game_state, "all_locations"):
        #game_state.all_locations.append(location) #← legacy
        game_state.location_registry.register(location)  # ← new

def guess_specialization_from_inventory(inventory) -> str:
    if inventory is None or not hasattr(inventory, "items"):
        return 

    tags = []
    for item in inventory.items.values():
        if hasattr(item, "get_percept_data"):
            data = item.get_percept_data()
            if data is not None:
                tags.extend(data.get("tags", []))

    # Simplified heuristics
    if any("weapon" in tag for tag in tags):
        return "weapon"
    elif any(tag in ["electronics", "smartphone", "laptop"] for tag in tags):
        return "electronics"
    elif any("medical" in tag or tag == "medkit" for tag in tags):
        return "medical"
    elif any(tag in ["tool", "toolkit"] for tag in tags):
        return "tools"
    elif any(tag in ["luxury", "statue", "vase", "lamp"] for tag in tags):
        return "luxury"
    else:
        return 
