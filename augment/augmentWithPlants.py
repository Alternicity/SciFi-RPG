#augment.augmentWithPlants.py

import random
from objects.InWorldObjects import Pot
from objects.trees_and_plants import GoldenRatioTree, Plant, Tree, OakTree, DustPalm, EchoWillow, BonsaiTree #most are unused so far
from location.locations import Cafe

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

def seed_bonsai_trees(destination):#was seed_ambience_objects
            pot = Pot()
            pot.add(BonsaiTree())
            place_object(pot, destination)





""" add_simple_plants()

add_desert_plants()

add_corporate_plants()

has_plants() """

