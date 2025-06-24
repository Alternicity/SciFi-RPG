#dream_and_thoughts.py
import uuid
from dream import Dream, DreamEntity
from memory_entry import MemoryEntry

she_held_my_hand = MemoryEntry(
    subject="Ava",
    object_="U7s",
    verb="touched",
    details="She shouldn't have, she was married, but she held my hand and told me she loves me.",
    importance=9,
    confidence=19,
    timestamp="before",
    tags=["social", "event", "connection", "disloyal", "nice", "desire"],
    type="flirtation",
    initial_memory_type="semantic",
    description="Nice, a taste of something we both wanted.",
    payload={"themes": ["sexual", "love", "flirtation"]},
    further_realizations=["We wanted more"],
    similarMemories=[],
    target="U7s"
)

she_held_my_hand = Dream(
    id=str(uuid.uuid4()),
    dreamer=None,  # Will be set when Luna experiences it
    theme="Status Touch",
    clarity=0.9,
    tone="confident",
    symbols=["temptation", "hands", "social", "forbidden", "gossip", "love"],
    entities=[
        DreamEntity(name="Ava", role="Flirt", tags=["forbidden", "hand", "touch"]),
        DreamEntity(name="U7s", role="Friend", tags=["uplift", "wounded", "backup"]),
        DreamEntity(name="John", role="Witness", tags=["intrigue"])
    ],
    source_memories=[she_held_my_hand],  # Optional linkage to specific MemoryEntries
    spawn_memories=[my_adepta],
    interpretation="Loyal to her emotions, she loved me that day, and I liked it.",
    sanskrit_insight="nishiddhah sparshah, forbidden touch.",
    is_precognitive=False,
    is_aetheric=True
)


