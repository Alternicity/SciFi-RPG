#createLocations.py
from location import MunicipalBuilding, Shop, Region
from base_classes import Location
from typing import List
from create_game_state import get_game_state
from utils import get_region_by_name
from location_types_by_wealth import LocationTypes
from InWorldObjects import SmartPhone, Size, Item
from weapons import Pistol


def create_locations(region: Region, wealth: str) -> List[Location]:
    """Creates and returns a list of location objects for a region based on its wealth level."""
    locations = []
    game_state = get_game_state()


    # Get list of location classes for this wealth level
    location_types = LocationTypes.location_types_by_wealth.get(wealth, [])

    for location_class, count in location_types:
        for _ in range(count):
            try:
                location_obj = location_class(
                    region=region,
                    name=location_class.__name__
                )
                #print(f"🧪 Creating {location_class.__name__} with region = {type(region)}")

                locations.append(location_obj)
                region.add_location(location_obj)  # 👈 Also updates game_state.all_locations
            except Exception as e:
                print(f"⚠️ Error creating location {location_class.__name__} in {region.name}: {e}")

    # 🔁 Handle Shops: add items
    for shop in [loc for loc in locations if isinstance(loc, Shop)]:
        shop.inventory.add_item(SmartPhone(price=200, quantity=5))
        shop.inventory.add_item(Pistol(price=500, quantity=2))

        #print(f"🔍 {shop.name} initial inventory:")
        for name, item in shop.inventory.items.items():
            #print(f"    {name}: {item.quantity} (type: {type(item)})")
            pass
        
    # 🏛️ Add one Municipal Building per region
    try:
        municipal_building = MunicipalBuilding(
            region=region,
            name=f"Municipal Building",
            tags=["government", "law", "tax"]
        )
        locations.append(municipal_building)
        region.add_location(municipal_building)

        game_state = get_game_state()
        #game_state.all_locations.append(municipal_building) # ← legacy
        game_state.municipal_buildings[region.name] = municipal_building
        game_state.location_registry.register(municipal_building)# ← new

    except Exception as e:
        print(f"⚠️ Error creating MunicipalBuilding in {region.name}: {e}")

    # 🔍 Optional: Insert auditing hook for dev tools
    # if DEV_MODE:
    #     audit_game_state()  # ← Could compare region.locations vs game_state.all_locations, etc.

    return locations

def add_location(self, location: Location):
    location.region = self
    self.locations.append(location)

    game_state = get_game_state()
    if hasattr(game_state, "all_locations"):
        #game_state.all_locations.append(location) #← legacy
        game_state.location_registry.register(location)  # ← new