#memory.memory_builders.gang_memory_builder.py
from memory.memory_entry import MemoryEntry

from world.scenarios.scenario_helpers import reserve_test_faction, select_unused_gang

def build_pistol_capture_memory(
    npc,
    boss,
    pistol,
    rival_boss,
    rival_gang
):
    #So perhaps we should be injecting to xyz npc memory here istead of returning a memory
    return MemoryEntry(
        subject=boss.name,
        object_="Gold Plated Pistol",

        subject_ref=boss,
        object_ref=pistol,

        details=(
            f"I remember when {boss.name} took that pistol "
            f"from the dead {rival_boss.name}, boss of the {rival_gang.name}."#rival boss needs creating. rival_gang currently marked not defined
        ),
        owner=npc,#unsure if this is correct
        source=npc,#later, investigate this
        tags=[
            "gang",
            "weapon",
            "captured",
            "trophy",
        ],
        type="observation",
        initial_memory_type="episodic",
        importance=6,
        confidence=10,
    )

def build_boss_office_memory(npc, boss, bosses_office):

    return MemoryEntry(
        subject=boss.name,
        object_=bosses_office.name,

        subject_ref=boss,
        object_ref=bosses_office,

        details=(
            f"I've been here before, in {boss.name}'s "
            f"{bosses_office.name}."
        ),

        owner=npc,
        source=npc,

        tags=[
            "gang",
            "place",
            "office",
        ],

        type="place",
        initial_memory_type="semantic",
        importance=6,
        confidence=10,
    )