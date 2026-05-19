#simulation.py
import random
from characters import GangMember, Civilian
from debug_utils import debug_print, init_log_file, close_log_file
from display.display import display_top_motivations
from simulation_utils import non_shop_or_cafe_locations, pick_civilian, assign_fallback_location
from create.create_game_state import get_game_state
game_state = get_game_state()
""" from employment.roles import CAFE_MANAGER, WAITRESS """

#from world.TC2_presets import setup_tc2_worker, get_tc2_cafe, place_tc2_npc, setup_tc2_civilian_liberty, assign_tc2_staging_location, place_tc2_passive_npc



from Family import assign_initial_location_from_family
from augment.augmentLocations import reassign_shop_names_after_character_creation
from world.placement import place_character#not accessed

""" from memory.memory_builders.food_sources_builder import build_food_sources
from memory.memory_builders.shop_knowledge_builder import build_shop_knowledge
from memory.memory_builders.region_knowledge_builder import build_region_knowledge """
from memory.injectors.initial_memory_injectors import inject_initial_region_knowledge, inject_food_location_knowledge, inject_initial_shop_knowledge, inject_fun_prefs
from population.population import summarize_civilians

def run_simulation(all_characters, num_ticks=10):
    from simulate_day import simulate_hours
    from location.locations import Shop
    
    init_log_file()
    try:
    
        debug_print(None, f"\nRunning simulation for {num_ticks} ticks...\n", category="simulation")

        #legacy block
        civilians = game_state.civilians 
        all_regions = game_state.all_regions
        summarize_civilians(civilians, all_regions)

        

        simulate_hours(all_characters, num_ticks=num_ticks, debug_character=None)
        
    finally:
        close_log_file()  # closes cleanly even if sim crashes
    print("\nSimulation complete.")


def pick_random_npc(characters, cls, exclude=None):
    return next((c for c in characters
                 if isinstance(c, cls) and c is not exclude),
                None)

def ensure_initial_placement(npc, *, fallback_region):#perhaps we dont call this for the civilian_passive
    #You do NOT need to call ensure_initial_placement() for background civilians anymore.
    #They are already placed in assign_families_and_homes().
    if getattr(npc, "placement_locked", False):
        return  # 🔥 DO NOTHING

    if assign_initial_location_from_family(npc):
        return

    assign_fallback_location(npc, fallback_region)
