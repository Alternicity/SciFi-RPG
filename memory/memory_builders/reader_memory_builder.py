#memory.memory_builders.reader_memory_builder.py

from memory.memory_entry import MemoryEntry
from world.scenarios.tc5_data import TC5_READERS
#all provisional here

def build_reading_room_memory(reader, reading_room):

    return MemoryEntry(
        subject=reading_room.name,
        object_="Reading Room",

        subject_ref=reading_room,
        object_ref=reading_room,

        details=(
            f"I know the {reading_room.name}. "
            f"I've spent time here before."
        ),

        owner=reader,
        source=reader,

        tags=[
            "place",
            "library",
            "reading_room",
        ],

        type="place",
        initial_memory_type="semantic",
        importance=5,
        confidence=10,
    )


def build_library_memory(reader, library):

    return MemoryEntry(
        subject=library.name,
        object_="library",

        subject_ref=library,
        object_ref=library,

        details=(
            f"I know the {library.name}. "
            f"I've been here before."
        ),

        owner=reader,
        source=reader,

        tags=[
            "place",
            "library",
        ],

        type="place",
        initial_memory_type="semantic",
        importance=5,
        confidence=10,
    )


def build_reader_social_memory(reader, other_npc):#needs updating , line 66

    return MemoryEntry(
        subject=reader.name,
        object_=other_npc.name,

        subject_ref=reader,
        object_ref=other_npc,

        details=(
            f"I know {other_npc.name}. "
            f"I've talked with them before."
        ),

        owner=reader,
        source=reader,

        tags=[
            "social",
            "reader",
        ],

        type="social",
        initial_memory_type="semantic",
        importance=5,
        confidence=8,
    )
