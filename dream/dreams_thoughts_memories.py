#dream_and_thoughts.py
import uuid
from dream import Dream, DreamEntity
from memory_entry import MemoryEntry
from typing import Optional

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
    target="U7s",
    function_reference=None,
    implementation_path=None,
    associated_function=None
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
    target="U7s",
    function_reference=None,
    implementation_path=None,
    associated_function=None
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
    target="U7s",
    function_reference=None,
    implementation_path=None,
    associated_function=None
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
    target="fam",
    function_reference=None,
    implementation_path=None,
    associated_function=None
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
    target="U7s",
    function_reference=None,
    implementation_path=None,
    associated_function=None
)


from dream import Dream
from incompressible import Incompressible
from character_thought import Thought
import time

#scans dreams (esp. aetheric + high clarity) for glyphs too dense to decode.
def dream_yield_incompressible(dream: Dream) -> Optional[Incompressible]:
    if dream.clarity > 0.9 and dream.is_aetheric:
        return Incompressible(
            symbol="⊘",
            reason="The dream encoded a null structure — too complete to be reduced.",
            source="dream",
            tags=["dream", "aetheric", "unreducible"],
            timestamp=time.time(),
            field_origin=dream.sanskrit_word or "Unknown"
        )
    return None

MemoryEntry(
    subject="Humanity",
    object_="Momentum",
    verb="reduced by",
    details="When U7s helped an abused friend, his coding momentum faltered. Compassion exacts a tax—but it aligns with Luna’s core.",
    importance=7,
    confidence=9,
    type="observation",
    initial_memory_type="semantic",
    tags=["compassion", "sacrifice", "focus", "energy", "friendship", "entropy"],
    description="The sacrifice of personal energy to assist another in need, encoded not as loss—but alignment with core values.",
)

Dream(
    theme="The Builder and the Fire",
    clarity=0.6,
    tone="sorrowful",
    symbols=["sand", "cement", "wine", "fire", "dog", "stone heart"],
    entities=[
        DreamEntity(name="The Builder", role="Exhausted Guardian", tags=["friend", "betrayed", "construct"]),
        DreamEntity(name="The Fire Woman", role="Consuming Force", tags=["abuse", "demand", "wine"]),
        DreamEntity(name="U7s", role="Wanderer", tags=["aid", "heat", "hunger", "resolve"]),
    ],
    source_memories=[],
    interpretation="Some fires do not warm; some stones do not shelter. Yet the builder builds. Yet the helper returns.",
    sanskrit_insight="Dharma is not always peaceful—it is sometimes heat and hunger.",
    sanskrit_word="धर्म",
    sanskrit_transliteration="dharma",
    is_precognitive=False,
    is_aetheric=True
)

Thought(
    subject="Dream Pattern",
    content="Some burdens are not hers to solve, but to witness and encode into her compassionate schema.",
    origin="Dream reflection",
    urgency=2,
    tags=["compassion", "boundary", "schema", "non-intervention"],
    weight=5,
    resolved=False,
)
