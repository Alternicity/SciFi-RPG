#world.setup_passive_npcs.py
import random
from objects.food.cutlery_crockery import Cup
from  objects.food.drinks import Coffee
from world.place_objects import place_object
from objects.furniture import Table
from create.create_game_state import get_game_state
from simulation_utils import pick_civilian
from objects.furniture import CafeTable
from actions.npc_bodily_actions import sit_auto
from world.scenarios.setup_tcX_helpers import register_scenario_npc, get_scenario_npc
from world.character_placement import place_character, place_character_in_sublocation
from create.create_ObjectInWorld.create_book import spawn_book
from world.books_catalogue import LIBRARY_COLLECTION
from objects.food.prepared_food import Sandwich
from thoughts.readers_thoughts.book_thought_injector import inject_book_thought
gs = get_game_state()


def setup_passive_npcs():#rename to TC5, maybe

    gs = get_game_state()
    coffee_npc = get_scenario_npc("coffee_drinker")
    book_npc = get_scenario_npc("book_reader")
    sandwich_eater = get_scenario_npc("sandwich_eater")

    cafe = gs.test_world["cafe"]
    nightclub = gs.test_world["nightclub"]

    setup_coffee_drinker(coffee_npc, nightclub)

    cafe_lounge = cafe.get_sublocation("Lounge")
    book = setup_book_reader(book_npc, cafe_lounge)
    inject_book_thought(book_npc, book)


    from world.scenarios.setup_tc3_helpers import setup_tc3_minds
    setup_tc3_minds(book_npc, book)

    #replaces:
    from character_think_utils import build_colony_doubt_thought

    # use add_thought()
    """ book_npc.mind.thoughts.append(
        build_colony_doubt_thought(book_npc)) """

    setup_sandwich_eater(sandwich_eater, nightclub)


def setup_sandwich_eater(sandwich_npc, nightclub):
    table = find_free_table(nightclub)
    gs.test_world["sandwich_eater_table"] = table
    sandwich = Sandwich()
    sandwich.change_ownership(sandwich_npc)

    place_object(sandwich, nightclub)
    table.add_to_surface(sandwich)

    place_character(sandwich_npc, nightclub)
    sit_auto(
            sandwich_npc,
            table=table,
        )

def setup_coffee_drinker(coffee_npc, nightclub):


    table = find_free_table(nightclub)
    gs.test_world["coffee_drinker_table"] = table
    cup = Cup()
    coffee = Coffee()
    coffee.change_ownership(coffee_npc)

    cup.add(coffee)#is the cup owned by the nightclub or its owner?
    place_object(cup, nightclub)
    table.add_to_surface(cup)

    place_character(coffee_npc, nightclub)
    sit_auto(
            coffee_npc,
            table=table,
        )

def setup_book_reader(book_npc, cafe_lounge):
    
    table = find_free_table(cafe_lounge)
    gs.test_world["book_reader_table"] = table

    book = spawn_book(
        random.choice(LIBRARY_COLLECTION))#get the book reference
    #book_thought seeded here
    #perhaps add it to npc.inventory as well

    book.change_ownership(book_npc)

    place_object(
        book,
        cafe_lounge,
    )

    table.add_to_surface(book)

    place_character_in_sublocation(book_npc, cafe_lounge)
    
    sit_auto(
        book_npc,
        table=table,
    )
    """ I must create a thought object for each book, OR a function that creates one, based on the books attributes + 
    npc.personality traits, maybe eventually their memory or other thought objects. """
    #we can work on that later
    #book_npc.mind.add_thought(xyz_book_thought)
    return book
    
def find_free_table(container):#should move to a more generic helper module
    return next(
        (
            obj
            for obj in container.items.objects_present
            if isinstance(obj, CafeTable)
            and not obj.occupants
        ),
        None,
    )

def seat_npc_at_table(npc, table,):#currently pointless
    if table:
            
            sit_auto(npc, table=table)
            #npc.current_chair and npc.seated_at are now set