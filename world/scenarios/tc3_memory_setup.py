#world.scenarios.tc3_memory_setup.py

from memory.memory_entry import MemoryEntry
from character_thought import Thought
def setup_tc3_assassin_vip_minds(assassin, vip):
    seed_tc3_assassin_enemy_memory(assassin, vip)
    seed_tc3_vip_enemy_memory(vip, assassin)

    inject_assassin_surveillance_thought(assassin, vip)
    inject_vip_threat_thought(vip, assassin)


def setup_tc3_boss_pair_minds(boss1, boss2):
    seed_tc3_boss1_enemy_memory(boss1, boss2)
    seed_tc3_boss2_enemy_memory(boss2, boss1)

    inject_tc3_boss1_rival_thought(boss1, boss2)
    inject_tc3_boss2_rival_thought(boss2, boss1)


def seed_tc3_boss1_enemy_memory(boss1, boss2):
    memories = [
        MemoryEntry(
            subject="self",
            object_=boss2.name,
            subject_ref=boss1,
            object_ref=boss2,
            verb="am watching",
            details=(
                f"{boss2.name} is moving on my territory. "
                "They are not to be trusted, and not to be left alone."
            ),
            importance=9,
            confidence=9,
            type="territory",
            initial_memory_type="semantic",
            tags=["enemy", "rival", "territory", "leadership"],
        ),
    ]
    for memory in memories:
        boss1.mind.memory.add_memory_entry(memory)


def seed_tc3_boss2_enemy_memory(boss2, boss1):
    #Boss2's memory confidence 8, boss1's 9 — boss2 is slightly less certain 
    # ("circling my people" is inference; "has been circling" is observed).
    memories = [
        MemoryEntry(
            subject="self",
            object_=boss1.name,
            subject_ref=boss2,
            object_ref=boss1,
            verb="am watching",
            details=(
                f"{boss1.name} has been circling my people. "
                "They want what I have, and they will not ask for it."
            ),
            importance=9,
            confidence=8,
            type="territory",
            initial_memory_type="semantic",
            tags=["enemy", "rival", "territory", "leadership"],
        ),
    ]
    for memory in memories:
        boss2.mind.memory.add_memory_entry(memory)


def build_tc3_boss1_rival_thought(boss1, boss2):
    return Thought(
        subject=boss2.name,
        content=(
            f"{boss2.name} is in the room. They are smiling. "
            "That has never once been good for me."
        ),
        urgency=14,
        tags=["enemy", "rival", "leadership"],
        source="seeded_debug_thought",
    )


def build_tc3_boss2_rival_thought(boss2, boss1):
    return Thought(
        subject=boss1.name,
        content=(
            f"{boss1.name} is here, in my city, under my roof. "
            "They are counting my people. I am counting theirs."
        ),
        urgency=16,
        tags=["enemy", "rival", "leadership"],
        source="seeded_debug_thought",
    )


def inject_tc3_boss1_rival_thought(boss1, boss2):
    boss1.mind.add_thought(build_tc3_boss1_rival_thought(boss1, boss2))


def inject_tc3_boss2_rival_thought(boss2, boss1):
    boss2.mind.add_thought(build_tc3_boss2_rival_thought(boss2, boss1))


def seed_tc3_assassin_enemy_memory(assassin, vip):
    memories = [
        MemoryEntry(
            subject="self",
            object_=vip.name,
            subject_ref=assassin,
            object_ref=vip,
            verb="am watching",
            details=f"I have been surveilling {vip.name}. They are a target.",
            importance=10,
            confidence=10,
            type="threat",
            initial_memory_type="semantic",
            tags=["enemy", "target", "surveillance"],
        ),
    ]
    for memory in memories:
        assassin.mind.memory.add_memory_entry(memory)


def seed_tc3_vip_enemy_memory(vip, assassin):
    memories = [
        MemoryEntry(
            subject="self",
            object_=assassin.name,
            subject_ref=vip,
            object_ref=assassin,
            verb="fear",
            details=f"{assassin.name} is dangerous. I must not be alone with them.",
            importance=9,
            confidence=7,
            type="threat",
            initial_memory_type="semantic",
            tags=["enemy", "fear", "danger"],
        ),
    ]
    for memory in memories:
        vip.mind.memory.add_memory_entry(memory)


def build_assassin_surveillance_thought(npc, vip):#should thought functions be in a parallel file?
    return Thought(
        subject=vip.name,
        content=f"{vip.name} is in the lounge. My target is in reach.",
        urgency=12,
        tags=["enemy", "target", "surveillance"],
        source="seeded_debug_thought",
    )


def build_vip_threat_thought(npc, assassin):
    return Thought(
        subject=assassin.name,
        content=f"{assassin.name} is here. I should not have come tonight.",
        urgency=15,
        tags=["enemy", "fear", "danger"],
        source="seeded_debug_thought",
    )

#injectors
def inject_assassin_surveillance_thought(npc, vip):
    npc.mind.add_thought(build_assassin_surveillance_thought(npc, vip))


def inject_vip_threat_thought(npc, assassin):
    npc.mind.add_thought(build_vip_threat_thought(npc, assassin))