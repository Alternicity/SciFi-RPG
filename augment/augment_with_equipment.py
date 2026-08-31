#augment.augment_with_equipment.py
from objects.InWorldObjects import AdvancedMedkit
from objects.unique_objects import SecretLaptop
from world.place_objects import place_object
from create.create_game_state import get_game_state
gs = get_game_state()

def setup_equipment():
    #needs to discern if parameter is a location or a sublocation, ie the Nightclub or the Boss Office
    test_world = gs.test_world
    gang = test_world["gang"]
    hq = gang.HQ
    boss = gang.boss
    boss_office = hq.boss_office
    desk = boss_office.desk#is O(1) No searching.
    advancedmedkit = AdvancedMedkit()
    advancedmedkit.change_ownership(boss)
    place_object(advancedmedkit, boss_office)
    desk.add_to_surface(advancedmedkit)

    #NOTE or we could set up a bosses_office entry in gs.test_world in augment_gang_hq_sublocations

    #then a block here to add the SecretLaptop to the VIP Lounge in the test Nightclub
            