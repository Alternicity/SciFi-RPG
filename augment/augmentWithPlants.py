#augment.augmentWithPlants.py

import random
from objects.InWorldObjects import Pot
from objects.trees_and_plants import GoldenRatioTree, Plant, Tree, OakTree, DustPalm, EchoWillow


from world.place_objects import place_object

def add_classy_plants(destination):

    count = random.randint(2, 5)

    for _ in range(count):

        pot = Pot()
        tree = GoldenRatioTree()

        pot.add(tree)

        place_object(
            pot,
            destination
        )