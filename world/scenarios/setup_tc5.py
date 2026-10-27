#world.scenarios.setup_tc5.py
from create.create_game_state import get_game_state
from world.character_placement import place_character_in_sublocation
from world.place_objects import place_object
from actions.npc_bodily_actions import sit_on
from world.scenarios.setup_tcX_helpers import register_scenario_npc

from world.scenarios.setup_tc5_helpers import setup_tc5_minds
from thoughts.readers_thoughts.book_thought_injector import inject_book_thought
from world.scenarios.tc5_data import TC5_READERS, READER_BOOK_MAP
from world.scenarios.setup_tc5_helpers import (
    get_test_library,
    get_reading_room,
    spawn_tc5_books,
    select_tc5_readers,
    assign_reader_intelligences,

)
from social.setup_social import generate_social_network

gs = get_game_state()



# TODO: scenario-spawned NPCs should eventually call a shared
# create_civilian(...) factory extracted from create_civilian_population.
# For now, tc5 pulls from the existing civilian pool to avoid
# duplicating initialization logic

"""Seed the library scenario: readers seated in a reading room with books."""
    #I must exclude reserved Civilians who are used in tc2 via gamestate.is_scenario_npc or debug_npcs
def setup_tc5_world(all_characters=None):
    library = get_test_library()
    if library is None:
        print("[TC5] No library found; aborting.")
        return

    reading_room = get_reading_room(library)
    if reading_room is None:
        print(f"[TC5] '{library.name}' has no Reading Room.")
        return

    readers = select_tc5_readers(n=len(TC5_READERS))
    if not readers:
        return

    assign_reader_intelligences(readers)

    for reader in readers:

        register_scenario_npc(reader, reader.scenario_role)
        place_character_in_sublocation(reader, reading_room)
        reader.faction = gs.factionless
        #build_reader_memories(reader, library, reading_room)
    generate_social_network(readers)
        

    _seat_readers(readers, reading_room)


    catalogue = spawn_tc5_books()
    placed = _place_books(readers, reading_room, catalogue)

    """ assert len(readers) == len(placed), (
        f"[TC5] reader/book count mismatch: {len(readers)} vs {len(placed)}"
    ) """
    
    for reader, book in zip(readers, placed):
        inject_book_thought(reader, book)

    gs.test_world["readers"] = readers
    print(f"[TC5] Seated {len(readers)} readers in '{reading_room.name}'.")

    setup_tc5_minds(readers, reading_room)

    _debug_dump_tc5(readers, reading_room, placed)

def _seat_readers(readers, reading_room):
    chairs = _find_chairs(reading_room)
    for reader, chair in zip(readers, chairs):
        try:
            sit_on(reader, chair)
        except Exception as e:
            print(f"[TC5] Could not seat {reader.name}: {e}")

def _find_chairs(reading_room):
    chairs = []
    items_container = getattr(reading_room, "items", None)
    if items_container is None:
        return chairs
    objects = getattr(items_container, "objects_present", [])
    for obj in objects:
        item_type = getattr(obj, "item_type", None)
        name = getattr(item_type, "name", "") if item_type else ""
        if name == "CHAIR" or obj.__class__.__name__ in (
            "CafeChair", "Chair", "OfficeChair", "OrnateChair",
        ):
            chairs.append(obj)
    return chairs


def _place_books(readers, reading_room, catalogue):
    books_by_title = {b.title: b for b in catalogue}
    placed = []

    for reader in readers:
        role = getattr(reader, "scenario_role", None)
        if role not in READER_BOOK_MAP:
            print(f"[TC5] {reader.name} role {role!r} not in READER_BOOK_MAP; skipping.")
            continue
        title = READER_BOOK_MAP[role]
        if title not in books_by_title:
            print(f"[TC5] Book {title!r} not in catalogue; skipping {reader.name}.")
            continue
        book = books_by_title[title]

        place_object(book, reading_room)
        # book.resting_on = None  # no furniture yet; leave unset
        book.owner = reader
        reader.inventory.add_item(book)
        placed.append(book)

    return placed

def _debug_dump_tc5(readers, reading_room, books):
    #removed for terminal brevity
    """ print("=" * 70)
    print(f"[TC5 DEBUG] Reading room: {reading_room.name}")
    print(f"[TC5 DEBUG]   parent: {getattr(reading_room, 'parent_location', None)}")
    print(f"[TC5 DEBUG]   region: {getattr(reading_room, 'region', None)}") """

    items = getattr(getattr(reading_room, "items", None), "objects_present", []) or []
    #print(f"[TC5 DEBUG]   items.objects_present ({len(items)}):")
    for obj in items:
        """ print(f"[TC5 DEBUG]     - {obj.__class__.__name__} name={getattr(obj, 'name', '?')!r} "
            f"type={getattr(getattr(obj, 'item_type', None), 'name', '?')}") """

    #print(f"[TC5 DEBUG] Readers ({len(readers)}):")
    for r in readers:
        """ print(f"[TC5 DEBUG]   - name={r.name!r} "
            f"race={getattr(r, 'race', '?')} "
            f"sex={getattr(r, 'sex', '?')} "
            f"intel={getattr(r, 'intelligence', '?')} "

            f"scenario_role={getattr(r, 'scenario_role', None)!r} "

            #the line below is marked: Unexpected indentation
            f"psy={getattr(r, 'psy', '?')} "
            f"region={getattr(getattr(r, 'region', None), 'name', None)} "
            f"loc={getattr(getattr(r, 'location', None), 'name', None)} "
            f"subloc={getattr(getattr(r, 'sublocation', None), 'name', None)} "
            f"faction={getattr(getattr(r, 'faction', None), 'name', None)} "
            f"scenario_npc={getattr(r, 'is_scenario_npc', False)}") """

        inv = getattr(r, "inventory", None)
        if inv is None:

            pass
            #print(f"[TC5 DEBUG]     inventory: None")
        else:
            if inv:
                for k, v in inv.items.items():
                    #print(f"[TC5 DEBUG]     inv[{k!r}] -> "
                    pass
                        #f"{v.__class__.__name__} name={getattr(v, 'name', '?')!r}")

        mind = getattr(r, "mind", None)
        thoughts = getattr(mind, "thoughts", None) if mind else None

        for t in (thoughts or []):
            origin = getattr(t, "origin", "?")
            cor_of = getattr(t, "corollary_of", None)
            marker = f" (of: {cor_of.content[:30]!r}...)" if cor_of else ""
            """ print(f"[TC5 DEBUG]       • [{origin}] {t.content!r} "
                  f"[tags: {t.tags}] urg={t.urgency}{marker}") """

        n_primary   = sum(1 for t in (thoughts or []) if getattr(t, "origin", None) == "book")
        n_corollary = sum(1 for t in (thoughts or []) if getattr(t, "origin", None) == "book_corollary")
        #print(f"[TC5 DEBUG]     thoughts: primary={n_primary} "
              #f"corollary={n_corollary} intel={getattr(r, 'intelligence', '?')}")


    #print(f"[TC5 DEBUG] Books ({len(books)}):")
    """ for b in books:
        print(f"[TC5 DEBUG]   - title={b.title!r} "
              f"tags={b.subject_tags} "
              f"owner={getattr(getattr(b, 'owner', None), 'name', None)} "
              f"resting_on={getattr(getattr(b, 'resting_on', None), 'name', None)}") """

    #print("=" * 70)


