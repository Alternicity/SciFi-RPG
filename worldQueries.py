#worldQueries.py
#location searches, filtering targets, etc.

from memory_entry import RegionKnowledge
from typing import Dict, List, Optional

def get_viable_robbery_targets(region):
    return [
        loc for loc in region.locations
        if getattr(loc, "robbable", False)
        and getattr(loc, "is_open", False)
        and not getattr(loc, "has_security", lambda: False)()
    ]

def get_nearby_objects(npc, region=None, location=None):
    if location is None:
        print(f"[DEBUG] {npc.name} has no valid location. No objects to observe.")
        return []

    nearby = []

    if location:
        # All characters at same location, except self
        nearby.extend([c for c in location.characters_there if c is not npc])

        # Objects at location
        if hasattr(location, "objects_present"):
            nearby.extend(location.objects_present)

        # Static structures like cash register, shop structure
        if hasattr(location, "cash_register"):
            nearby.append(location.cash_register)

        # Add location itself if needed (e.g. a perceptible building)
        nearby.append(location)

    return nearby

def observe_location(self, loc):
    #print(f"[Observe] {self.name} observes {loc.name}")
    perceptibles = getattr(loc, "list_perceptibles", lambda exclude=None: [])(exclude=[self])
    for obj in perceptibles:
        #add to self._percepts?
        #perhaps just hand this off to UtilityAI compute_salience_for_percepts()
        return
    
def get_region_knowledge(semantic_memory: Dict[str, List], region_name: str) -> Optional[RegionKnowledge]:
    region_knowledge_entries = semantic_memory.get("region_knowledge", [])
    for rk in region_knowledge_entries:
        if isinstance(rk, RegionKnowledge) and rk.region_name == region_name:
            return rk
    return None
