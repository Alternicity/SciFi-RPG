#create.create_sublocations.py
from base.location import Sublocation
from augment.augmentWithPlants import add_classy_plants
from location.locations import Cafe, Nightclub, HQ, SportsCenter
from augment.augmentSublocations.augmentCafeSublocations import augment_cafe_sublocations
def setup_location_sublocations(location):

    builder = SUBLOCATION_BUILDERS.get(type(location))

    if builder is None:
        return

    builder(location)

def add_sublocation(parent, sublocation):

    if sublocation in parent.sublocations:#prevent repeated calls adding extra sublocs
        return sublocation#raises the question: How will we add 10 cubicles?

    sublocation.parent_location = parent

    sublocation.location = parent

    sublocation.region = parent.region

    parent.sublocations.append(sublocation)

    return sublocation

def create_hq_sublocations(hq):
    pass
    """ if hq.faction.type == "gang":
        ...

    elif hq.faction.type == "corporation":
        ... """

def create_cafe_sublocations(location):
    cafe = location
    lounge = add_sublocation(
            cafe,
            Sublocation(
                name="Lounge",
                perceptible_from_parent=True
            )
        )
    #print("Creating cafe lounge")
    augment_cafe_sublocations(lounge)
    lounge.can_see_parent_location = True

    #these values just copied from VIP Lounge for now
    """ lounge.visible_roles = ["VIP", "Babe"]
    lounge.accessible_roles = ["VIP", "Babe"] """
    #needs to be everyone here, if used at all

def create_gang_hq_sublocations():
    pass

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
    hq.boss_office = boss_office

    """ Now you have two access patterns:
    hq.sublocations
    for iteration
    and
    hq.boss_office
    for the important room. """

    #tag doesnt exist yet
    if hasattr(hq, "has_tag") and hq.has_tag("classy"):
        add_classy_plants(boss_office)
    
    return boss_office

def create_nightclub_sublocations(nightclub):

    vip_lounge = add_sublocation(
        nightclub,
        Sublocation(
            name="VIP Lounge",
            perceptible_from_parent=False
        )
    )

    vip_lounge.can_see_parent_location = True

    vip_lounge.visible_roles = ["VIP", "Babe"]#added, but this should not be role based. A vip outside the lounge would also not be able to see into it.
    vip_lounge.accessible_roles = ["VIP", "Babe"]#need to ensure the test npcs have this, and gui accurately shows their ability to access
    

    """ if nightclub.has_tag("classy"):
        add_classy_plants(vip_lounge) """

def create_corporate_hq_sublocations():
    pass

def create_executive_office(location):
    pass

def create_sports_center_sublocations(sportsclub):
    pass

SUBLOCATION_BUILDERS = {

    Cafe: create_cafe_sublocations,

    Nightclub: create_nightclub_sublocations,

    HQ: create_hq_sublocations,

    SportsCenter: create_sports_center_sublocations,#SportsCenter marked as not defined for some reason
}
