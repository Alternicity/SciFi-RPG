def get_region_wealth(region):
    """
    Returns the wealth level of a given region.
    """
    print(f"Debug: Received region = {region}")
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

# Data-specific logic for getting regions started
for region in regions:
    #print(f"Processing region: {region}")  # Debugging print
    #print(f"Region wealth: {get_region_wealth(region)}")  # Debugging print
    pass