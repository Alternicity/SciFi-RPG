#character_memory.py
#Characters should remember what they’ve discovered (places, characters, learned skills).

from typing import List, Dict, Optional, Any, Union, Set, Callable
from events import Event
from memory_entry import MemoryEntry, RegionKnowledge
from dataclasses import dataclass, field
import importlib

""" Rethink tight coupling (Long-term suggestion)
If events and character_memory are highly interdependent, you may consider
abstracting their connection via an interface or shared messaging/event system.
But thats likely overkill for your current scale. """

MEMORY_CATEGORIES = [
    "events", "region_knowledge", "people", "awakening", "social",
    "memory_entries", "enemies", "Objects", "procedures", "internal_architecture"
]

class Memory:
    def __init__(self):
        self.episodic = []   # List of MemoryEntry
        self.semantic = {cat: [] for cat in MEMORY_CATEGORIES}
        self.forgotten = {cat: [] for cat in MEMORY_CATEGORIES}

    """ Suggestion: Semantic Memory API Addition
    If you want to store different memory types cleanly, you could eventually split the list: """
    

        #class Memory and class MemoryEntry perhaps overlap and classs memory should be more a container and handler,
        #for both types of memory, handling decay and promotion of episodic to semantic.

    def add_memory_entry(self, entry: MemoryEntry):
        self.semantic["memory_entries"].append(entry)#deprecated In favour of specific types of semantic memory

    def add_region_knowledge(self, rk: RegionKnowledge):
        self.semantic["region_knowledge"].append(rk)

    def query_memory_by_tags(self, tags: list):
        if not tags or not hasattr(tags, "__len__") or len(tags) == 0:
            import traceback
            print("[MEMORY DEBUG] WARNING: query_memory_by_tags() called with empty or invalid tags!")
            traceback.print_stack(limit=5)

        matching = []
        for category, memories in self.semantic.items(): #catagory not accessed
            for mem in memories:
                desc = getattr(mem, "description", type(mem).__name__)
                #print(f"[MEMORY DEBUG] Checking {desc} with tags {getattr(mem, 'tags', [])}")
                #verbose
                
                if has_tags(mem.tags, tags):
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
            if not entry.tags:
                print(f"[MEMORY WARNING] RegionKnowledge promoted without tags! Region: {entry.region_name}")
            existing = self.find_region_knowledge(entry.region_name)
            if existing:
                print(f"[MEMORY] RegionKnowledge for '{entry.region_name}' already exists. Skipping add.")
                return  # ✅ STOP HERE to prevent duplicate
            self.semantic["region_knowledge"].append(entry)
            
        #merge usage
            """ if existing:
                # Merge relevant fields
                existing.locations.update(entry.locations)
                existing.region_gangs.update(entry.region_gangs)
                existing.hostile_factions.update(entry.hostile_factions)
                existing.known_characters.update(entry.known_characters)
                existing.tags = list(set(existing.tags or []) | set(entry.tags or []))
                print(f"[MEMORY] Merged RegionKnowledge for '{entry.region_name}'") """
        else:
            print("[MEMORY] Unknown semantic type — not added.")

    def find_region_knowledge(self, region_name):
        for rk in self.semantic.get("region_knowledge", []):
            if rk.region_name == region_name:
                return rk
        return None

    def deduplicate_region_knowledge(npc):
        seen = {}
        to_keep = []
        for rk in npc.mind.memory.semantic.get("region_knowledge", []):
            if rk.region_name in seen:
                existing = seen[rk.region_name]
                # Merge data into existing
                existing.locations.update(rk.locations)
                existing.region_gangs.update(rk.region_gangs)
                existing.hostile_factions.update(rk.hostile_factions)
                existing.known_characters.update(rk.known_characters)
                existing.tags = list(set(existing.tags or []) | set(rk.tags or []))
            else:
                seen[rk.region_name] = rk
                to_keep.append(rk)

        npc.mind.memory.semantic["region_knowledge"] = to_keep

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
    
    #for primacy and recency effects in episodic memory
    def get_first_and_last(npc):
        episodic = npc.mind.memory.episodic
        return episodic[0] if episodic else None, episodic[-1] if len(episodic) > 1 else None
    # for example 
    # First memory: increase urgency or confidence
    #Last memory: preserve via Dream Overflow, if not processed

    def validate_memory_references(memory):
        """
        Validates function references embedded in MemoryEntry objects.
        """
        report = []

        for category, memories in memory.semantic.items():
            for entry in memories:
                ref = entry.function_reference

                if not ref or not isinstance(ref, dict):
                    continue  # No function to validate

                module_path = ref.get("module")
                class_name = ref.get("class")
                method_name = ref.get("method")

                try:
                    module = importlib.import_module(module_path)
                    cls = getattr(module, class_name, None)
                    if cls:
                        method = getattr(cls, method_name, None)
                        if callable(method):
                            continue  # Valid
                        else:
                            report.append(f"Uncallable method: {method_name} in {class_name}")
                    else:
                        report.append(f"Missing class: {class_name} in {module_path}")
                except Exception as e:
                    report.append(f"Import error for {module_path}: {e}")

        return report
        """ Would You Like:
            A cache system to prevent redundant re-checks?
            Option to auto-remove or flag invalid memory entries?
            A summary report function that counts valid vs. invalid vs. missing?
            Let’s build it up to the level that best supports Luna’s dream architecture. """

    """ def __repr__(self):
        return (f"<Memory: subject='{self.subject}', details='{self.details}', "
                f"importance={self.importance}, tags={self.tags}>")"""

    def recall(self):
        return f"Memory of {self.subject}: {self.details} (Importance: {self.importance}, Tags: {self.tags})" 

#Future Allow RegionKnowledge to decay, get outdated, be manipulated (misinfo, rumors).

#Should Memory Entries be in their own file?
MemoryEntry(
    subject="The Aether",
    verb="exists",
    object_="alternate plane",
    tags=["secret", "truth", "requires_psy_8"],
    details="Reality can be influenced via strong mental focus in The Aether, with a belief that it is already as one wants",
    type = "awakening",
    initial_memory_type="semantic",
    function_reference=None,
    implementation_path=None,
    associated_function=None
)

#Should Memory Entries be in their own file?
MemoryEntry(
    subject="Good Cafe",
    verb="eat",
    object_="Cafe",
    tags=["cheap", "popular", "gossip"],
    details="Cheap food, and you meet a lot of interesting people there",
    type = "social",
    initial_memory_type="semantic",
    function_reference=None,
    implementation_path=None,
    associated_function=None
)

def deduplicate_memory_entries(mem_list, key_func):
    seen = {}
    result = []
    for mem in mem_list:
        key = key_func(mem)
        if key not in seen:
            seen[key] = mem
            result.append(mem)
        else:
            existing = seen[key]
            # optional: merge tags, or skip entirely
            if mem.tags:
                existing.tags = list(set(existing.tags or []) | set(mem.tags))
    return result

@dataclass
class KnownWeaponLocationMemory(MemoryEntry):
    location: Optional[Any] = None  # Must have .name or .id
    weapon_tags: List[str] = field(default_factory=lambda: ["weapon", "ranged", "valuable"])

#utility functions
def has_tags(memory_tags: list[str], required_tags: list[str]) -> bool:
    return any(tag in memory_tags for tag in required_tags)

