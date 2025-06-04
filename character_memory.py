#character_memory.py
#Characters should remember what they’ve discovered (places, characters, learned skills).
import time

class Memory:
    def __init__(self):
        self.episodic = []   # List of MemoryEntry
        self.semantic = []   # List of semantic MemoryEntry or facts

        #now you need episodic memory (what they saw before) and optionally semantic memory (learned facts)
        #class Memory and class MemoryEntry perhaps overlap and classs memory should be more a container and handler,
        #for both types of memory, handling decay and promotion of episodic to semantic.

    def add_entry(self, entry, type="episodic"):
        if type == "semantic":
            self.semantic.append(entry)
        else:
            self.episodic.append(entry)

    def add_semantic_entry(self, entry, type="semantic"):
            self.semantic.append(entry)

    def promote_to_semantic(self, entry):
        if entry in self.episodic:
            print(f"[MEMORY] Promoted to semantic: '{entry.description}' about {getattr(entry.target, 'name', entry.target)}. Tags: {entry.tags}. Importance: {entry.importance}.")
        self.semantic.append(entry)

    def recent(self, count=5):
        return sorted(self.episodic, key=lambda e: e.timestamp, reverse=True)[:count]

    def all_facts(self):
        return self.semantic

    """ def __repr__(self):
        return (f"<Memory: subject='{self.subject}', details='{self.details}', "
                f"importance={self.importance}, tags={self.tags}>")

    def recall(self):
        return f"Memory of {self.subject}: {self.details} (Importance: {self.importance}, Tags: {self.tags})" """
    
class MemoryEntry:
    def __init__(self, subject, details, importance=1, timestamp=None, tags=None, event_type=None, target=None, description=None, approx_identity=None):
        self.subject = subject
        self.details = details
        self.importance = importance
        self.timestamp = timestamp or "now"
        self.tags = tags or [] #always a list, even if not provided.
        self.event_type = event_type or "observation" # defaults to "observation" if not specified
        self.target = target #target can be a string or an object with a .name attribute.
        self.description = description or details
        self.approx_identity = None  # Optional fuzzy match value
        self.approx_identity = approx_identity
        self.further_realizations = [] # when character think() about this memory, they might unlock an insight here
        self.similarMemories = [] #for pattern spotting. "Shes done this before..."
    """ Memory Decay System
    for memory in character.memory:
    memory.importance -= 1
    character.memory = [m for m in character.memory if m.importance > 0] """

    def __repr__(self):
        return (f"<MemoryEntry: event_type='{self.event_type}', target='{getattr(self.target, 'name', self.target)}', "
                f"description='{self.description}', tags={getattr(self, 'tags', [])}>")

class FactionRelatedMemory(Memory):
    """ Knowledge of how the world works, and how this relates to the faction. Entries known by 
    all cahracter in a factions self.members """
    def __init__(self, subject, details, importance=5):
        self.it_worked_there_before = {} # location/actions or action list


class ShopsSellRangedWeapons(MemoryEntry):
    def __init__(self, location_name, importance=5, timestamp=None):
        super().__init__(
            event_type="shop_known_to_sell_weapons",
            target=location_name,
            description=f"{location_name} is known to sell ranged weapons.",
            timestamp=timestamp or time.time(),
            tags=["weapon", "shop"]
        )
