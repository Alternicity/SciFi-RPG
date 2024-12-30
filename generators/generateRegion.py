#generateRegion.py

from generators.generateGang import generateGang
from generators.generateCorp import generate_corporations
from generators.generateStore import generate_stores
from generators.generateLocation import generate_locations


def generate_region(region_size, economic_level, danger_level):
    try:
        locations = generate_locations(region_size)
        gangs = generateGang(danger_level)
        corporations = generate_corporations(economic_level)
        stores = generate_stores(economic_level, danger_level)
    except ValueError as e:
        print(f"Value error in region generation: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

    return {
        "locations": locations,
        "gangs": gangs,
        "corporations": corporations,
        "stores": stores,
    }
