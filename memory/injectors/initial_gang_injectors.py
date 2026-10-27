#memory.injectors.initial_gang_injectors.py

from memory.memory_builders.gang_memory_builder import build_pistol_capture_memory, build_boss_office_memory

def inject_pistol_capture_memory(
    npc,
    boss,
    pistol,
    rival_boss,
    rival_gang
):
    memory = build_pistol_capture_memory(#should we follow this pattern?
        npc,
        boss,
        pistol,
        rival_boss,
        rival_gang
    )

    print("=== TC4 MEMORY INJECTION ===")
    print("NPC:", npc.name)
    print("Memory:", memory.description)
    print("Type:", memory.initial_memory_type)

    npc.mind.memory.add_entry_if_new(memory)



def inject_boss_office_memory(npc, boss, bosses_office):

    memory = build_boss_office_memory(
        npc,
        boss,
        bosses_office
    )

    print("=== TC4 BOSS OFFICE MEMORY INJECTION ===")
    print("NPC:", npc.name)
    print("Memory:", memory.details)
    print("Type:", memory.initial_memory_type)

    npc.mind.memory.add_semantic_unique(
        "place",
        memory
    )

        
