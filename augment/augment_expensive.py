#augment.augment_expensive.py
from objects.expensive_furniture import OrnateChair, ExpensiveDesk

from world.place_objects import place_object

def add_expensive_furniture(sublocation):

    desk = place_object(
        ExpensiveDesk(),
        sublocation,
    )

    chair = place_object(
        OrnateChair(),
        sublocation,
    )

    sublocation.desk = desk
    sublocation.chair = chair

    return {
        "desk": desk,
        "chair": chair,
    }