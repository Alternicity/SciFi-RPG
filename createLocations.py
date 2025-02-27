#create locations
from location import MunicipalBuilding
from base_classes import Location
from typing import List



def create_locations(region_name: str, wealth: str) -> List[Location]:
    """Creates a list of location objects for a region based on its wealth level."""
    locations = [] #this is functionaly identical here to locations but shows up in character_creation_funcs as well
    #so consider removing it and using locations here and there.

    # Fetch location types for this wealth level
    from location_types_by_wealth import LocationTypes
    location_types = LocationTypes.location_types_by_wealth.get(wealth, [])

    for location_class, count in location_types:
        for _ in range(count):  # Create the specified number of locations
            try:
                # Pass region and name if required by the location class
                location_obj = location_class(
                    region=region_name,  # If region is needed, pass it here
                    name=f"{location_class.__name__} in {region_name}"
                )
                locations.append(location_obj)
                #print(f"Created location: {location_obj} of type {type(location_obj)}")

            except Exception as e:
                print(f"Error creating location {location_class.__name__} in {region_name}: {e}")

    # Always create a MunicipalBuilding
    try:
        municipal_building = MunicipalBuilding(
            region=region_name, 
            name=f"Municipal Building in {region_name}"
        )
        locations.append(municipal_building)
    except Exception as e:
        print(f"Error creating MunicipalBuilding in {region_name}: {e}")
        print(f"MunicipalBuilding reference from createLocations import: {MunicipalBuilding} ({id(MunicipalBuilding)})")

    return locations