#augment.augment_locations.augment_library.py
from location.locations import Library
from objects.furniture import Table, Chair, Sofa, Bench
from objects.InWorldObjects import Pot, CashRegister, Toughness, ItemType, Size
from objects.trees_and_plants import BonsaiTree
from base.location import Sublocation
from world.place_objects import place_object
from world.books import Book

def seed_library_furniture(all_locations):
    for loc in all_locations:
        if not isinstance(loc, Library):
            continue
        if any(isinstance(o, Table) for o in loc.items.objects_present):
            continue  # already seeded

        for t in range(4):  # 4 reading tables
            table = Table(
                name=f"Reading Table {t+1}",
                size=Size.LARGE,
                seating_capacity=2,  # intimate, focused
                toughness=Toughness.DURABLE,
            )
            place_object(table, loc)

            for c in range(2):
                chair = Chair(name=f"Reading Chair {t+1}-{c+1}")
                place_object(chair, loc)
                table.chairs.append(chair)

from create.create_ObjectInWorld.create_book import spawn_book

def seed_library_books(all_locations):
    from world.books_catalogue import LIBRARY_COLLECTION
    for loc in all_locations:
        if not isinstance(loc, Library):
            continue
        for template in LIBRARY_COLLECTION:
            place_object(spawn_book(template), loc)#So a function parameter can itself be a function call with its own paramter?


