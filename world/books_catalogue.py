# world/books_catalogue.py

from world.books import Book

# Official history — the noble lie
COLONY_FOUNDING_RECORD = Book(
    title="The First Landing: A Colony History",
    author="Colonial Archive Bureau",
    subject_tags=["history", "official", "colony"],
    knowledge_type="history",
    is_redacted=True,  # certain pages missing
    psy_resonance=0.1,
    reading_difficulty=3,
)

# Hints at precursors
ARCHITECTURAL_ANOMALIES = Book(
    title="Unexplained Structures of the Eastern Reaches",
    author="Dr. Maren Voss",#Note Add this to a list of names
    subject_tags=["archaeology", "precursor", "mystery"],
    knowledge_type="science",
    psy_resonance=0.4,
    reading_difficulty=6,
)

# Something that resonates with psy-sensitive NPCs strongly
RESONANCE_CODEX = Book(
    title="The Resonance Codex",
    author="Anonymous",
    subject_tags=["psy", "forbidden", "precursor"],
    knowledge_type="forbidden",
    is_redacted=False,
    psy_resonance=1.8,
    reading_difficulty=9,
)

# Mundane practical knowledge
CIVIC_MANUAL = Book(
    title="Civic Life in the Colony",
    author="Colonial Bureau of Education",
    subject_tags=["civic", "practical", "colony"],
    knowledge_type="general",
    reading_difficulty=1,
)

LIBRARY_COLLECTION = [
    COLONY_FOUNDING_RECORD,
    ARCHITECTURAL_ANOMALIES,
    RESONANCE_CODEX,
    CIVIC_MANUAL,
]