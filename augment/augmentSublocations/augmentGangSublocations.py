#augment.augmentSublocations.augmentGangSublocations.py
from augment.augmentSublocations.augmentSublocations import add_office_furniture
from world.place_objects import place_object
from objects.furniture import CafeChair
from augment.augmentWithPlants import add_classy_plants

def augment_gang_hq_sublocations(boss_office):

    add_office_furniture(boss_office)
    add_classy_plants(boss_office)

    for c in range(8):#not in its own function
        chair = CafeChair(
            name=f"Chair {c+1}"
        )

        place_object(
            chair,
            boss_office
        )

