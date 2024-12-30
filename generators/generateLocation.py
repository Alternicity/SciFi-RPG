def generate_locations(region_size: str):
    """
    Generate location data with variability in security levels and capacities.
    
    Args:
        region_size (str): The size of the region ('small', 'medium', 'large').

    Returns:
        list: A list of dictionaries containing location information.
    """
    size_mapping = {"small": 5, "medium": 10, "large": 20}
    num_locations = max(1, int(generate_normal(mean=size_mapping.get(region_size, 5), std_dev=2)))
    
    locations = []
    for i in range(num_locations):
        security_level = max(1, int(generate_normal(mean=3, std_dev=1)))  # Variable security level
        capacity = max(10, int(generate_normal(mean=30, std_dev=5)))  # Variable capacity
        locations.append({
            "name": f"Location {i+1}",
            "type": random.choice(["Shop", "Warehouse", "Cafe", "Park", "Nightclub"]),
            "security_level": security_level,
            "capacity": capacity,
        })
    
    return locations
