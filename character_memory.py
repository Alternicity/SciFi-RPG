#character_memory.py
#Characters should remember what they’ve discovered (places, characters, learned skills).

from typing import List, Dict, Optional, Any, Union, Set, Callable
from events import Event
from memory_entry import MemoryEntry, RegionKnowledge

""" Rethink tight coupling (Long-term suggestion)
If events and character_memory are highly interdependent, you may consider
abstracting their connection via an interface or shared messaging/event system.
But thats likely overkill for your current scale. """

class Memory:
    def __init__(self):
        self.episodic = []   # List of MemoryEntry

        self.semantic = {
        "events": [],
        "region_knowledge": [],
        "people": [],
        "awakening": [],
        "social": [],
        "memory_entries": [],
        "enemies": [],
    }

    """ Suggestion: Semantic Memory API Addition
    If you want to store different memory types cleanly, you could eventually split the list: """
    

        #class Memory and class MemoryEntry perhaps overlap and classs memory should be more a container and handler,
        #for both types of memory, handling decay and promotion of episodic to semantic.

    def add_memory_entry(self, entry: MemoryEntry):
        self.semantic["memory_entries"].append(entry)#deprecated In favour of specific types of semantic memory

    def add_region_knowledge(self, rk: RegionKnowledge):
        self.semantic["region_knowledge"].append(rk)

    def query_memory_by_tags(self, tags: list):
        matching = []
        for category, memories in self.semantic.items():
            for mem in memories:
                if all(tag in mem.tags for tag in tags):
                    matching.append(mem)
        return matching

    def get_all_memories(self):
        #gets both episodic and semantic memories
        pass #possibly deprecate, maybe useful for big memory copying

    def promote_to_semantic(self, entry):
        if entry in self.episodic:
            print(f"[MEMORY] Promoted to semantic: '{entry.description}' about {getattr(entry.target, 'name', entry.target)}. Tags: {entry.tags}. Importance: {entry.importance}.")
        if isinstance(entry, MemoryEntry):
            self.semantic["memory_entries"].append(entry)
        elif isinstance(entry, RegionKnowledge):
            self.semantic["region_knowledge"].append(entry)
        else:
            print("[MEMORY] Unknown semantic type — not added.")

    def recent(self, count=5):
        return sorted(self.episodic, key=lambda e: e.timestamp, reverse=True)[:count]

    def all_facts(self):
        return self.semantic #deprecate

    def get_episodic(self):
        return self.episodic
    
    def get_semantic(self):
        for memories in self.semantic.values():
            for memory in memories:
                yield memory #Now this will only return MemoryEntry objects, not dict keys.

    def add_semantic(self, memory_entry: MemoryEntry, category="memory_entries"):
        if not isinstance(memory_entry, MemoryEntry):
            raise TypeError(f"[ERROR] Tried to add non-MemoryEntry to semantic memory: {memory_entry}")

        self.semantic.setdefault(category, [])

        for mem in self.semantic[category]:
            if (
                mem.subject == memory_entry.subject and
                mem.object_ == memory_entry.object_ and
                mem.verb == memory_entry.verb and
                set(mem.tags) == set(memory_entry.tags)
            ):
                return  # Duplicate

        self.semantic[category].append(memory_entry)

    def add_episodic(self, memory_entry: MemoryEntry):
        # Accept all entries, but optionally tally them by key
        self.episodic.append(memory_entry)
        # Hook: could notify utility/thinking AI
        # self.check_for_pattern(memory_entry)
        #"Thats the third time Fido asked to go for a walk"

    def all_semantic(self): #return flattened data
        return [entry for entries in self.semantic.values() for entry in entries] 

    """ def __repr__(self):
        return (f"<Memory: subject='{self.subject}', details='{self.details}', "
                f"importance={self.importance}, tags={self.tags}>")

    def recall(self):
        return f"Memory of {self.subject}: {self.details} (Importance: {self.importance}, Tags: {self.tags})" """
    
#Future Allow RegionKnowledge to decay, get outdated, be manipulated (misinfo, rumors).

#Should Memory Entries be in their own file?
MemoryEntry(
    subject="The Aether",
    verb="exists",
    object_="alternate plane",
    tags=["secret", "truth", "requires_psy_8"],
    details="Reality can be influenced via strong mental focus in The Aether, with a belief that it is already as one wants",
    type = "awakening",
    initial_memory_type="semantic"
)

#Should Memory Entries be in their own file?
MemoryEntry(
    subject="Good Cafe",
    verb="eat",
    object_="Cafe",
    tags=["cheap", "popular", "gossip"],
    details="Cheap food, and you meet a lot of interesting people there",
    type = "social",
    initial_memory_type="semantic"
)

