#memory.memory_builders.shop_knowledge_builder.py
#Builders should ALWAYS take a single region or a single source object.
from base.core_types import KnowledgeBase

def build_shop_knowledge(region):
    shops = []
    food_shops = []

    for loc in region.locations:
        tags = getattr(loc, "tags", [])

        if "shop" in tags:
            shops.append(loc.name)

        if "food" in tags:
            food_shops.append(loc.name)#what if both shop and food tags are present?

    return KnowledgeBase(
        type="shop_knowledge",
        region=region.name,
        shops=shops,
        food_shops=food_shops,
    )