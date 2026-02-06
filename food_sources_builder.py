#food_sources_builder
#DEPRECATED, but contains details for the future
from character_memory import RegionKnowledge, FoodSources, FoodSourceMemory
def build_food_sourcesDEPRECATED(self, npc):
    sources = FoodSources()

    for loc in npc.region.locations:
        if not loc.has_tag("food"):
            continue

        entry = FoodSourceMemory(
            subject=npc.name,
            verb="knows_food_source",
            object_=loc.name,
            details=f"{npc.name} knows {loc.name} is a place to get food.",
            initial_memory_type="semantic",
            type="knowledge",
            tags=["food_source", loc.type],

            location_ref=loc,
            base_preference=loc.base_food_quality,
            fun_factor=loc.fun_value,
            ambience_factor=loc.ambience_value,
            nutrition_value=loc.nutrition_value,

            considers_fun=npc.fun_seeking,
            considers_ambience=npc.ambience_sensitive,
            considers_nutrition=True,

            is_home_option=(loc == npc.home),
            is_shop_option=loc.has_tag("shop"),
            partner_present=npc.partner_is_home,
            can_expect_partner=npc.expecting_partner_to_return,
        )

        sources.entries[loc.name] = entry

    return sources
