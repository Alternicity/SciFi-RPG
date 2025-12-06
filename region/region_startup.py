#region.region_startup.py

def get_region_wealth(region):#never called
    """
    Returns the wealth level of a given region.
    """

    regions_with_wealth = {
        "North": "Rich",
        "South": "Normal",
        "East": "Poor",
        "West": "Normal",
        "Central": "Rich",
    }
    return regions_with_wealth.get(region, "Unknown")

# Define the regions list before using it
regions = ["North", "Central", "South", "East", "West"]

