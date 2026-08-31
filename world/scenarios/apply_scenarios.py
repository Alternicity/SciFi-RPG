#world.scenarios.apply_scenarios.py

from world.scenarios.setup_tc1 import setup_tc1_world
from world.scenarios.setup_tc2 import setup_tc2_world
from world.scenarios.setup_tc3 import setup_tc3_world
from world.scenarios.setup_tc4 import setup_tc4_world
from world.scenarios.setup_tc4_helpers import select_tc4_gang

from world.scenarios.setup_normal_stuff import setup_normal_stuff
from world.scenarios.economy.setup_normal_economy import setup_normal_economy
from world.scenarios.setup_debug_npcs import setup_debug_npcs
from world.setup_passive_npcs import setup_passive_npcs
from world.scenarios.setup_test_world import select_test_world
from augment.augment_with_equipment import setup_equipment

def apply_scenarios(all_characters):#consider removing all_characters from these:
    select_test_world()

    setup_debug_npcs(all_characters)

    setup_tc1_world(all_characters)
    setup_tc2_world(all_characters)
    
    setup_normal_stuff(all_characters)
    setup_normal_economy(all_characters)

    setup_tc3_world()
    setup_passive_npcs()

    select_tc4_gang()
    setup_tc4_world(all_characters)
    setup_equipment()