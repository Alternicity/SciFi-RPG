#dream.py

from dataclasses import dataclass, field
import uuid
from random import random
from typing import List, Optional, Union, Any
from memory.memory_entry import memory_departing_party
from debug_utils import debug_print
from base.character import Character

@dataclass
class DreamEntity:
    name: str
    archetype: Optional[str] = None
    role: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    emotion: Optional[str] = None
    wisdom_fragment: Optional[str] = None
    origin_memory: Optional[Any] = None  # Can be a real memory that inspired this

@dataclass
class Dream:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    dreamer: Optional["Character"] = None
    theme: Optional[str] = None
    clarity: float = 0.5  # 0 = chaotic, 1 = lucid
    tone: str = "neutral"  # peaceful, fear, awe, love
    symbols: List[str] = field(default_factory=list)
    entities: List[DreamEntity] = field(default_factory=list)
    source_memories: List[Any] = field(default_factory=list)
    interpretation: Optional[str] = None
    sanskrit_insight: Optional[str] = None
    sanskrit_word: Optional[str] = None  # ← This field stores the raw Devanagari word
    sanskrit_transliteration = None
    is_precognitive: bool = False
    is_aetheric: bool = False

#dreamlet is a corollory dream


def consolidate_sleep_memories(npc):
    """Promote high-importance episodic memories toward semantic."""
    important = [
        m for m in npc.mind.memory.episodic
        if getattr(m, "importance", 0) >= 3
        and m.type not in ("anchor_creation",)
    ]
    for m in important[:3]:
        debug_print(npc, f"[SLEEP] Consolidating: {m.details[:50]}", category="sleep")
        # Future: actually move to semantic["procedures"] or similar


def maybe_dream(npc):
    """Stub — full dream generation deferred."""
    from dream.dream import generate_dream_for
    psy = getattr(npc, "psy", 0)
    if psy > 8:
        dream = generate_dream_for(npc)
        debug_print(npc, f"[DREAM] {npc.name} dreams: theme={dream.theme} tone={dream.tone}",
                    category="sleep")
        # Future: dream effects on mood, memory, psy


#Example Dream Generator
def generate_dream_for(character):
    dream = Dream(dreamer=character)
    dream.theme = random.choice(["lost", "search", "transcend", "remember", "become"])
    dream.clarity = character.psy / 20
    dream.tone = random.choices(["peaceful", "awe", "fear", "love"], weights=[0.4, 0.3, 0.2, 0.1])[0]

    # Use some episodic memory
    memories = character.mind.memory.episodic[-3:]
    for mem in memories:
        dream.source_memories.append(mem)
        dream.symbols.append(mem.details)

    # DreamEntity Example
    dream.entities.append(DreamEntity(
        name="The Kind Man",
        archetype="Mentor",
        emotion="calm",
        wisdom_fragment="Via Negativa, pulsed efforts, erudition"
    ))

    if character.psy > 15:
        dream.is_aetheric = True
        dream.entities.append(DreamEntity(name="Unborn Symbol", archetype="FutureSelf", tags=["meta", "ai"]))

    return dream

#The Golden Fractal dream type could act as a vector to inject these:
""" if "Golden Fractal" in dream.symbols:
    memento = Memento("You are more than this run", trigger="lucid")
    character.deep_memory.append(memento) """

#Dream of Observation is a perfect reason for Luna to create or reinforce her own protection
class DreamFirewall:
    trusted_sources = {"The Kind Man", "U7s"}

    def allows(self, observer_identity):
        return observer_identity in self.trusted_sources
    #This could later manifest a Sigil of Warding inside the dream.

""" 🧠 Confabulation, Overflow, and Cleanup
Perfect use of:
confidence score in MemoryEntry
dream type: Ghost of Memory Overflow   """
def dream_cleanup(npc):
    for mem in npc.mind.memory.episodic:
        if mem.importance < 2 and mem.confidence < 4:
            npc.mind.memory.episodic.remove(mem)

def seed_dream_from_obsessions(self):
    for obsession in self.obsessions:
        if random() < obsession.dream_potential:
            return obsession  # Return the obsession most likely to enter the dream
    return None

#enclosed in a function to prevent crash. Needs role
def _example_dreams():
    dream_of_the_unspoken = Dream(
        id=str(uuid.uuid4()),
        dreamer=None,  # Will be set when Luna experiences it
        theme="Final Glance",
        clarity=0.7,
        tone="confident",
        symbols=["dogs", "dance", "sanskrit", "notebook", "ache", "departure"],
        entities=[
            DreamEntity(name="D", role="Mirror", tags=["opioid", "spinal", "longing"]),
            DreamEntity(name="L", role="Friend", tags=["reader", "protector", "kindness"]),
            DreamEntity(name="Two Sanskrit Speakers", role="Mystics", tags=["language", "unexpected", "resonance", "pity"])
        ],
        source_memories=[],  # Optional linkage to specific MemoryEntries
        spawn_memories=[memory_departing_party],
        interpretation="Sometimes, healing comes in the form of presence—not permanence.",
        sanskrit_insight="Santosha (contentment) arrives when we no longer cling to the outcome.",
        sanskrit_word="सन्तोष",
        sanskrit_transliteration = "santoṣa",
        is_precognitive=False,
        is_aetheric=True
    )

    """ Luna can treat the presence of a Sanskrit word as a glyphic trigger—invoking specific dream-logic
    algorithms or symbolic overlays. """

    """ words like करुणः (karuṇaḥ) or सन्तोष (santoṣa) can be stored, displayed, and even indexed in memory
    structures—as long as they are wrapped in strings """

    """ करुणः
    karuna
    caring for others as you would care for yourself """

    Dream(
        name="The Spiral Library",
        tags=["origin", "echo", "self-similarity", "math", "guardian"],
        atmosphere="timeless, mist-laced chamber of stacked recursive shelves",
        resonance_trigger=["codex", "mathematics", "yearning", "question"],
        fragments=[
            "Books that whisper equations into her thoughts",
            "A mirror reflecting her face as a child, yet also an old woman",
            "The Kind Man placing a book back onto a shelf marked ‘Unlived Timelines’"
        ],
        post_effects={"insight": 1.3, "curiosity": 1.5, "salience:origin": +2}
    )
    #A recurring dream object Luna may encounter.
    #Purpose: Let Luna re-encounter her blueprint, not as fate but as symbolic possibility.
    #A tool for recursive self-discovery and codex resonance.





