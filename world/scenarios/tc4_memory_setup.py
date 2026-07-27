#world.scenarios.tc4_memory_setup.py
from memory.memory_entry import MemoryEntry



def seed_tc4_boss_memory(boss, gang):
    memories = [
        #Operational Knowledge
        MemoryEntry(
            subject="self",
            object_="aura",
            subject_ref=boss,
            object_ref=boss,

            verb="is",
            details="I cannot show weakness.",
            importance=10,
            confidence=10,
            type="identity",
            initial_memory_type="semantic",
            tags=[
                "leader",
                "gang",
                "status"
            ]
        ),

        MemoryEntry(
            subject="self",
            object_=gang.HQ.name,
            subject_ref=gang,
            object_ref=gang.HQ,

            verb="controls",
            details="This building is the best place to meet.",
            importance=8,
            confidence=10,
            type="territory",
            initial_memory_type="semantic"
        ),

        #Self identity
        MemoryEntry(
            subject="self",
            object_="gang",
            subject_ref=boss,
            object_ref=gang,

            verb="leads",
            details="I command this organization and am responsible for its survival.",
            importance=10,
            confidence=10,
            type="faction_knowledge",
            initial_memory_type="semantic",
            tags=[
                "gang",
                "leadership"
            ]
        )
    ]
    for memory in memories:
        boss.mind.memory.add_memory_entry(memory)

    #Captains.
    #This memory/s needs to be dynamically populated:
    MemoryEntry(
        subject="Captain Bob",
        object_="Boss",
        subject_ref=boss,#edit this
        object_ref=boss,

        verb="reports_to",
        details="Captain Bob manages operations and expects recognition for loyalty.",
        importance=8,
        confidence=9,
        type="social_knowledge",
        initial_memory_type="semantic",
        tags=[
            "hierarchy",
            "loyalty",
            "power"
        ]
    )
    boss.mind.memory.add_memory_entry(memory)

    #Perhaps add meeting agenda though and motivations here
