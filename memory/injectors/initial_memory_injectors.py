#memory.injectors.initial_memory_injectors.py
from memory.memory_builders.region_knowledge_builder import build_region_knowledge
from memory.memory_builders.shop_knowledge_builder import build_shop_knowledge
from memory.memory_builders.food_sources_builder import build_food_sources

from memory.encoders.shop_memory_encoder import encode_shop_knowledge

from create.create_game_state import get_game_state
game_state = get_game_state()
#Injectors should iterate through game_state.all_regions

def inject_initial_region_knowledge(npc):
    for region in game_state.all_regions:
        rk = build_region_knowledge(region, npc)
        npc.mind.memory.semantic["region_knowledge"].append(rk)

#When shops are more specialized, npcs will need to know which shop sells what.
#I will have to build also an encode_XYZ_shop_memory()

def inject_initial_shop_knowledge(npc):
    for region in game_state.all_regions:
        kb = build_shop_knowledge(region)
        mem = encode_shop_knowledge(kb, npc)
        npc.mind.memory.add_semantic_unique(
            "shop_knowledge",
            mem,
            dedupe_key="details"
        )

def inject_food_location_knowledge(npc):
    for region in game_state.all_regions:
        mem = build_food_sources(region)
        npc.mind.memory.semantic["food_locations"].append(mem)