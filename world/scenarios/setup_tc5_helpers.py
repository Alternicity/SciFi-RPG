#world.scenarios.setup_tc5_helpers.py
from create.create_game_state import get_game_state
from world.scenarios.setup_tcX_helpers import available_for_scenario, register_scenario_npc
from world.scenarios.tc5_data import TC5_READERS
gs = get_game_state()


def get_test_library():
    region = gs.test_world.get("region")
    if region is not None:
        for loc in getattr(region, "locations", []):
            if loc.__class__.__name__ == "Library":
                return loc
    for loc in getattr(gs, "all_locations", []):
        if loc.__class__.__name__ == "Library":
            return loc
    return None


def get_reading_room(library):
    for sub in getattr(library, "sublocations", []):
        if sub.name in ("Reading Room", "RedingRoom"):
            return sub
    return None


def spawn_tc5_books():
    from world.books_catalogue import LIBRARY_COLLECTION
    from create.create_ObjectInWorld.create_book import spawn_book
    return [spawn_book(t) for t in LIBRARY_COLLECTION]

def select_tc5_readers(n=5):
    
    candidates = [c for c in gs.civilians if available_for_scenario(c)]

    if len(candidates) < n:
        print(
            f"[TC5] Only {len(candidates)} candidates available, "
            f"need {n}."
        )

    readers = sorted(candidates, key=lambda c: c.name)[:n]

    for reader, (role, intel, psy) in zip(readers, TC5_READERS):#intel, psy not yet uesd, but they will be eventually
        #is role acutally doing anything here?
        reader.scenario_role = role
        #register_scenario_npc(reader, f"TC5 Reader ({role})")
        #this line was commented out at some point

    return readers

""" def select_tc5_readers(n=5):

    candidates = []

    for civ in gs.civilians:

        if not available_for_scenario(civ):
            continue

        candidates.append(civ)

    if len(candidates) < n:
        print(
            f"[TC5] Only {len(candidates)} candidates available, "
            f"need {n}."
        )

    readers = sorted(
        candidates,
        key=lambda c: c.name
    )[:n]

    for reader in readers:
        register_scenario_npc(
            reader,
            "TC5 Reader"
        )

    return readers """


# Intelligence/psy distribution matched to corollary thresholds.
# (name_role, intelligence, psy)
""" READER_PROFILES = [
    ("DullReader",      8,  5),
    ("AverageReader",  11,  8),
    ("SharpReader",    13, 10),
    ("BrilliantReader",15, 12),
    ("PsyReader",      13, 18),
] """
def assign_reader_intelligences(readers):
    by_role = {role: (intel, psy) for role, intel, psy in TC5_READERS}
    for reader in readers:
        role = getattr(reader, "scenario_role", None)
        if role is None or role not in by_role:
            print(f"[TC5] {reader.name} role {role!r} unmapped; skipping.")
            continue
        reader.intelligence, reader.psy = by_role[role]
        if hasattr(reader.mind, "refresh_capacity"):
            reader.mind.refresh_capacity()

from memory.injectors.initial_reader_memories import inject_reading_room_memory
def setup_tc5_minds(readers, reading_room):

    for npc in readers:#Do we need t oget an npc2 here?
        inject_reading_room_memory(npc, reading_room)
        
        #inject_reader_social_memory(...)