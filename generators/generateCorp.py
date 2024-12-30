from distributions import generate_normal

def generate_corporations(economic_level):
    """
    Generate corporations based on the destination region's economic level, with variability in size and wealth.
    
    Args:
        economic_level (int): The economic strength of the region.

    Returns:
        list: A list of dictionaries containing corporation information.
    """
    corporations = []
    num_corporations = max(1, int(generate_normal(mean=economic_level, std_dev=1.5)))  # More corps for higher levels

    for i in range(num_corporations):
        # Size variability: Larger regions can host larger corporations
        employees = max(
            20, 
            int(generate_normal(mean=50 * economic_level, std_dev=10))
        )
        # Wealth variability: Higher economic levels attract wealthier corporations
        wealth = max(
            1000, 
            int(generate_normal(mean=10000 * economic_level, std_dev=2000))
        )
        corporations.append({
            "name": f"Corporation {i+1}",
            "economic_level": economic_level,
            "employees": employees,
            "wealth": wealth,  # Add wealth attribute
        })
    
    return corporations
