#world.scenarios.setup_test_world.py
from create.create_game_state import get_game_state
gs = get_game_state()
from world.scenarios.setup_tc4_helpers import select_tc4_gang, select_unused_gang
def select_test_world():
    #pick region - its hard coded to downtown for now
    test_region = next(
            (
                r for r in gs.all_regions
                if r.name == "downtown"
            ),
            None
        )
    #test_region = select_test_region()
    #no, this function does not exist

    gs.test_world["region"] = test_region

    #pick cafe - TC2
    cafe = next(
            (loc for loc in test_region.locations if loc.__class__.__name__ == "Cafe"),
            None
        )

    #cafe = select_test_cafe(region)
    #plausible alternative..except the function doesnt exist

    gs.test_world["cafe"] = cafe

    #pick nightclub - TC3
    nightclub = next(
        (n for n in test_region.locations if n.__class__.__name__ == "Nightclub"),
                None
    )

    #nightclub = select_test_nightclub(region)
    #plausible alternative

    #Is it worth extracting the three next blocks above in to function/s select_test_XYZ()

    nightclub.is_tc3_nightclub = True
    gs.test_world["nightclub"] = nightclub

    #pick gang
    gang = select_tc4_gang()#see prompt reference code
    gs.test_world["gang"] = gang

    #pick HQ
    #This HQ has to be the one owned by the Gang or Gang Boss being instantiated in it:
    hq = gang.HQ
    #Or:
    #gs.test_world["hq"] = gang.HQ
    print("Test World")
    print(gs.test_world)
#I must check the TCx setup files/functions and world.setup_passive_npcs for stale code  that used to do these things 
# to be deleted


""" No NPCs.

No furniture.

No placement.

Just references. """