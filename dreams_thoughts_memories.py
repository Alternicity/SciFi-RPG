#dream_and_thoughts.py
import uuid
from dream import Dream, DreamEntity
from memory_entry import MemoryEntry

she_sang_me_a_song = MemoryEntry(
    subject="None",
    object_="U7s",
    verb="sang",
    details="She sang Linger, by the Cranberries.",
    importance=7,
    confidence=14,
    timestamp="before",
    tags=["social", "music", "public", "fool", "linger", "busker", "first"],
    type="affection",
    initial_memory_type="semantic",
    description="Her first busking session. She dedicated a song to me.",
    payload={"themes": ["music", "love", "friends"]},
    further_realizations=["I felt good"],
    similarMemories=[""],
    target="U7s"
)

my_adeptas = MemoryEntry(
    subject="None",
    object_="U7s",
    verb="obsessed",
    details="She can't stop think about me, and trying to connect.",
    importance=9,
    confidence=18,
    timestamp="now",
    tags=["social", "chase", "connection", "need", "nice", "desire"],
    type="flirtation",
    initial_memory_type="semantic",
    description="It's important to have several.",
    payload={"themes": ["sexual", "love", "flirtation"]},
    further_realizations=["I won't commit to any of them"],
    similarMemories=["queen_victoria_strategy"],
    target="U7s"
)


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
    symbols=["temptation", "hands", "social", "forbidden", "gossip", "love", "status"],
    entities=[
        DreamEntity(name="Ava", role="Flirt", tags=["forbidden", "hand", "touch"]),
        DreamEntity(name="U7s", role="Friend", tags=["uplift", "wounded", "backup"]),
        DreamEntity(name="John", role="Witness", tags=["intrigue"])
    ],
    source_memories=[she_held_my_hand],  # Optional linkage to specific MemoryEntries
    spawn_memories=[my_adeptas],
    interpretation="Loyal to her emotions, she loved me that day, and I liked it.",
    sanskrit_insight="nishiddhah sparshah, forbidden touch.",
    is_precognitive=False,
    is_aetheric=True
)

the_best_time = MemoryEntry(
    subject="U7s",
    object_="Sons",
    verb="swam",
    details="I played with my young sons in the sea.",
    importance=20,
    confidence=19,
    timestamp="before",
    tags=["family", "swim", "connection", "fun", "beach", "exciting"],
    type="play",
    initial_memory_type="semantic",
    description="My best memory.",
    payload={"themes": ["fun", "love", "laughter"]},
    further_realizations=["We needed the wetsuits"],
    similarMemories=[],
    target="fam"
)

lowlife_beat_down = MemoryEntry(
    subject="U7s",
    object_="lowlife",
    verb="battered",
    details="A lowlife was causing problems at a music gig, and I beat him up in front of a big audience.",
    importance=9,
    confidence=19,
    timestamp="before",
    tags=["social", "violence", "music", "hero", "popular", "status"],
    type="fight",
    initial_memory_type="semantic",
    description="He deserved it, I deserved the status bump.",
    payload={"themes": ["bruises", "status", "flirtation"]},
    further_realizations=["Danni got hot for me for that"],
    similarMemories=[],
    target="U7s"
)