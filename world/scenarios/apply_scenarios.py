#world.scenarios.apply_scenarios.py

from world.scenarios.setup_tc1 import setup_tc1_world
from world.scenarios.setup_tc2 import setup_tc2_world
from world.scenarios.setup_normal_stuff import setup_normal_stuff

def apply_scenarios(all_characters):

    setup_tc1_world(all_characters)
    setup_tc2_world(all_characters)
    setup_normal_stuff(all_characters)