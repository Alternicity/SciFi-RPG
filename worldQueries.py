#worldQueries.py
#location searches, filtering targets, etc.

from memory.memory_entry import RegionKnowledge
from typing import Dict, List, Optional
from debug_utils import debug_print
#essentially redundant now that Im doing salience computation directly via anchors.
def get_viable_robbery_targets(region):
    return [
        loc for loc in region.locations
        if getattr(loc, "robbable", False)
        and getattr(loc, "is_open", False)
        and not getattr(loc, "has_security", lambda: False)()
    ]
    #Keep get_viable_robbery_targets() in worldQueries for that purpose, 
    # but remove direct imports/uses from ai_gang.py or characterActions.py

    #If an NPC lacks personal region knowledge, VisitToRobAnchor
    #  could call get_viable_robbery_targets(region) as a fallback list of possible targets.

def get_nearby_objects(npc, location=None):
    if location is None:
        print(f"[DEBUG] {npc.name} has no valid location. No objects to observe.")
        return []

    nearby = []

    # Characters
    nearby.extend([c for c in location.characters_there if c is not npc])

    # Objects
    if hasattr(location, "objects_present"):
        nearby.extend(location.objects_present)

    # Fixtures
    if hasattr(location, "cash_register"):
        nearby.append(location.cash_register)

    # causes duplicated location percepts
    #nearby.append(location)

    return nearby

#remove
""" def observe_location(self, loc):
    perceptibles = getattr(loc, "list_perceptibles", lambda exclude=None: [])(exclude=[self])
    for obj in perceptibles:
        return """
    
def get_region_knowledge(semantic_memory, region_name):
    for rk in semantic_memory.get("region_knowledge", []):
        if isinstance(rk, RegionKnowledge) and rk.region_name == region_name:
            return rk
    return None

def location_sells_food(location):
    if not location:
        return False

    # Explicit capability beats tags
    if hasattr(location, "items_available") and location.items_available:#this doesnt check if specifically food is available
        return True

    # Tag-based fallback
    tags = getattr(location, "tags", [])
    return "food" in tags or "restaurant" in tags or "cafe" in tags
