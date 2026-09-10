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
from world.placement import place_character, place_character_in_sublocation
from create.create_ObjectInWorld.create_book import spawn_book
from world.books_catalogue import LIBRARY_COLLECTION
gs = get_game_state()


def setup_passive_npcs():

    gs = get_game_state()

    #coffee_npc = gs.debug_npcs["coffee_drinker"]

    #I am not sure this will work this early in flow
    #coffee_npc = get_scenario_npc("coffee_drinker")

    coffee_npc = get_scenario_npc("coffee_drinker")

    #book_npc = gs.debug_npcs["book_reader"]
    book_npc = get_scenario_npc("book_reader")

    from character_think_utils import build_colony_doubt_thought
    book_npc.mind.thoughts.append(
        build_colony_doubt_thought(book_npc))

    cafe = gs.test_world["cafe"]

    

    nightclub = gs.test_world["nightclub"]

    setup_coffee_drinker(coffee_npc, nightclub)

    cafe_lounge = cafe.get_sublocation("Lounge")
    setup_book_reader(book_npc, cafe_lounge)

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
        random.choice(LIBRARY_COLLECTION))

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
    
def find_free_table(container):
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