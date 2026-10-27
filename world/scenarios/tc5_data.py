#world.scenarios.tc5_data.py


"""Static tc5 scenario data. No imports from other tc5 modules."""

TC5_READERS = [
    ("DullReader",       8,  5),#role, intelligence, psy
    ("AverageReader",   11,  8),
    ("SharpReader",     13, 10),
    ("BrilliantReader", 15, 12),
    ("PsyReader",       13, 18),
]

READER_BOOK_MAP = {
    "DullReader":      "The First Landing: A Colony History",
    "AverageReader":   "Unexplained Structures of the Eastern Reaches",
    "SharpReader":     "The Resonance Codex",
    "BrilliantReader": "Civic Life in the Colony",
    "PsyReader":       "Tuning the Aether",
}