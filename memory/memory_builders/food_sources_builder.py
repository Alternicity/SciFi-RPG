#memory.memory_builders.food_sources_builder.py
#Builders should ALWAYS take a single region or a single source object.
from base.core_types import KnowledgeBase

#SEE ALSO def build_food_sourcesDEPRECATED

def build_food_sources(region):
    food_locations = []

    for loc in region.locations:
        tags = getattr(loc, "tags", [])

        if "food" in tags:
            food_locations.append(loc.name)

    return KnowledgeBase(
        type="food_sources",
        region=region.name,
        locations=food_locations,
    )
