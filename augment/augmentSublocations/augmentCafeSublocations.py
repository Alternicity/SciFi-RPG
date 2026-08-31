#augment.augmentSublocations.augmentCafeSublocations.py
from world.place_objects import place_object
from world.setup_passive_npcs import find_free_table
from objects.furniture import CafeTable, CafeChair

def augment_cafe_sublocations(lounge):
    seed_cafe_lounge_furniture(lounge)

def seed_cafe_lounge_furniture(lounge):
    
    table = CafeTable(name="Lounge Table")

    place_object(table, lounge)

    for i in range(4):
        chair = CafeChair(name=f"Lounge Chair {i+1}")

        place_object(chair, lounge)

        chair.table = table
        table.chairs.append(chair)