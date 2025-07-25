#region_knowledge_builder.py
from location import Region
from character_memory import RegionKnowledge
from base_classes import Character,Faction
from typing import Union

def build_region_knowledge(region: Region, character_or_faction: Union["Character", "Faction"]) -> RegionKnowledge:
    knowledge = RegionKnowledge(
        region_name=region.name,
        character_or_faction=character_or_faction,
        region_gangs={g.name for g in region.region_gangs},
        is_street_gang=any(getattr(g, "is_street_gang", False) for g in region.region_gangs),
        friendly_factions=set(),
        hostile_factions=set(),
        locations={loc.name for loc in region.locations},
        shops={loc.name for loc in region.shops},
        known_characters={c.name for c in region.characters_there},
        active_events=region.active_regional_events.copy(),
        recent_regional_events=region.recent_regional_events.copy(),
        historical_regional_events=region.historical_regional_events.copy(),
        gossip=[],  # maybe fill this later through social observation
        economic_info={},  # optionally parse from region or simulation systems
        tags=["region", "region_knowledge"] + [g.name for g in region.region_gangs],

    )

    print(f"[BUILD RK DEBUG] {region.name} has shops: {[loc.name for loc in region.shops]}")

    # Relationship tagging could be added later based on Faction/Character relations
    return knowledge

