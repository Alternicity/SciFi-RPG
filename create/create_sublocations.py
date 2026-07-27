#create.create_sublocations.py
from base.location import Sublocation
from augment.augmentWithPlants import add_classy_plants

def setup_hq_sublocations(hq, faction_type):

    if hq.sublocations:
        return

    if faction_type == "gang":
        create_boss_office(hq)

    elif faction_type == "corporate":
        create_executive_office(hq)

def create_boss_office(hq):
    boss_office = Sublocation(
            name="Boss Office",
            perceptible_from_parent=False
        )
    boss_office.parent_location = hq
    boss_office.can_see_parent_location = True
    boss_office.region = hq.region
    boss_office.visible_roles = ["Boss", "Captain", "GangMember"]#These need checking
    boss_office.accessible_roles = ["Boss", "Captain", "GangMember"]#
    
    hq.sublocations.append(boss_office)

    #tag doesnt exist yet
    if hasattr(hq, "has_tag") and hq.has_tag("classy"):
        add_classy_plants(boss_office)
    
    return boss_office

def create_executive_office(location):
    pass

