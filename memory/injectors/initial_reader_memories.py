#memory.injectors.initial_reader_memories.py
from memory.memory_builders.reader_memory_builder import build_reading_room_memory
def inject_reading_room_memory(npc, reading_room):

    memory = build_reading_room_memory(#build_reading_room_memory not defined
        npc,
        reading_room
    )

    print("=== TC5 READING ROOM MEMORY INJECTION ===")
    print("NPC:", npc.name)
    print("Memory:", memory.details)
    print("Type:", memory.initial_memory_type)

    npc.mind.memory.add_semantic_unique(
        "place",
        memory
    )