#create locations
from location import MunicipalBuilding, Shop
from base_classes import Location
from typing import List
from create_game_state import get_game_state


def create_locations(region_name: str, wealth: str) -> List[Location]:
    """Creates a list of location objects for a region based on its wealth level."""
    locations = [] 
    game_state = get_game_state()

    # Fetch location types for this wealth level
    from location_types_by_wealth import LocationTypes
    location_types = LocationTypes.location_types_by_wealth.get(wealth, [])

    for location_class, count in location_types:
        for _ in range(count):  # Create the specified number of locations
            try:
                location_obj = location_class(
                    region=region_name,  
                    name=location_class.__name__
                )
                locations.append(location_obj)

            except Exception as e:
                print(f"Error creating location {location_class.__name__} in {region_name}: {e}")

    # ✅ Update both region and game_state with the same shop instances
    shop_instances = [loc for loc in locations if isinstance(loc, Shop)]
    
    from utils import get_region_by_name
    region_obj = get_region_by_name(region_name, game_state.all_regions)  #game_state!
    if region_obj:
        region_obj.locations.extend(shop_instances)  # Ensure they match!
    for shop in shop_instances:
        print(f"✅ DEBUG: Created {shop.name} in {shop.region} (ID: {id(shop)})")
        from InWorldObjects import SmartPhone, Size, Item
        from weapons import Pistol #is importing within a for loop inefficient?

        # Instantiate items
        smartphone = SmartPhone()
        pistol = Pistol()

        # Add to inventory
        shop.inventory.add_item(SmartPhone(price=200, quantity=5))
        shop.inventory.add_item(Pistol(price=500, quantity=2))


        if isinstance(shop, Shop):
            print(f"🔍 {shop.name} initial inventory (object-level):")
            for name, item in shop.inventory.items.items():
                print(f"    {name}: {item.quantity} (type: {type(item)})")


        print(f"🛒 DEBUG: Added items to {shop.name} inventory.")
    # Always create a MunicipalBuilding
    try:
        municipal_building = MunicipalBuilding(
            region=region_name, #ALERT
            name=f"Municipal Building in {region_name}"
        )
        locations.append(municipal_building)

        game_state.all_locations.append(municipal_building)
        game_state.municipal_buildings[region_name] = municipal_building  

    except Exception as e:
        print(f"Error creating MunicipalBuilding in {region_name}: {e}")

    #print(f"📌 DEBUG: Created locations for {region_name}: {locations}") #verbose
    return locations