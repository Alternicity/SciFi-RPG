#generate Store
import sys
print(sys.path)

try:
    from distributions import generate_black_swan, generate_normal
except ModuleNotFoundError:
    from ..distributions import generate_black_swan, generate_normal



def generate_stores(economic_level: int, danger_level: int):
    """
    Generate store data with occasional Black Swan events.
    
    Args:
        economic_level (int): The economic strength of the region.
        danger_level (int): The overall danger level of the region.

    Returns:
        list: A list of dictionaries containing store information.
    """
    num_stores = max(1, int(generate_normal(mean=economic_level, std_dev=2)))
    stores = []
    
    for i in range(num_stores):
        black_swan_event = generate_black_swan(threshold=0.1, impact_range=(1000, 5000))  # Rare high revenue
        revenue = (
            black_swan_event if black_swan_event 
            else int(generate_normal(mean=100 * economic_level, std_dev=20))
        )
        stores.append({
            "name": f"Store {i+1}",
            "economic_level": economic_level,
            "revenue": revenue,
            "items_for_sale": (
                ["Weapons", "Food", "Electronics"] if danger_level > 5 
                else ["Food", "Clothing"]
            ),
        })
    
    return stores
