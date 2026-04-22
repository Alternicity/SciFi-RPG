#region.region_utils.py
#hmmmm...doesnt do much yet

from typing import List
def get_all_regions() -> List[str]:
    
    #Returns a list of all available regions.
    region_names = ["North", "East", "West", "South", "Central"]
    return region_names
    

REGION_NEIGHBORS = {

    "Central": ["North", "South", "East", "West"],

    "North": ["Central"],
    "South": ["Central"],
    "East": ["Central"],
    "West": ["Central"]

}
    
from collections import deque


def calculate_region_travel_distance(start, end):
    #breadth first search
    if start == end:
        return 0

    visited = set()
    queue = deque([(start, 0)])

    while queue:

        region, distance = queue.popleft()

        if region == end:
            return distance

        visited.add(region)

        for neighbor in REGION_NEIGHBORS.get(region, []):

            if neighbor not in visited:
                queue.append((neighbor, distance + 1))

    return None

"""  Allowing Diagonal Travel Later

You mentioned:

skipping downtown

If you later want diagonal routes:

North → East
North → West
South → East
South → West

You would simply change the map:

"North": ["Central", "East", "West"]

The algorithm already supports this. """