# world/location_names.py
import random
LIBRARY_NAMES = [
    "The Voss Archive",        # named after fictional author
    "The Meridian Collection",
    "Eastwall Public Library",
    "The Redacted Stacks",     # lore-flavored
    "The Memory Hall",
]

PARK_NAMES = [
    "Founder's Green",
    "The Spiral Garden",       # references GoldenRatioTree
    "Dust & Bloom Park",       # colony-world flavor
    "The Quiet Reach",
]

CAFE_PREFIXES = ["The", "Old", "New", "Little"]
CAFE_SUFFIXES = ["Cup", "Corner", "Table", "Common", "Grounds"]

def generate_cafe_name(family_name=None):
    if family_name and random.random() < 0.5:
        return f"{family_name}'s Cafe"
    prefix = random.choice(CAFE_PREFIXES)
    suffix = random.choice(CAFE_SUFFIXES)
    return f"{prefix} {suffix}"