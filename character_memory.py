#character_memory.py
#Characters should remember what they’ve discovered (places, characters, learned skills).
import time

class Memory:
    def __init__(self, subject, details, importance=5, timestamp=None, tags=None):
        self.subject = subject  # What the memory is about
        self.details = details  # Context
        self.importance = importance  # How significant is it?
        self.timestamp = timestamp or "now"  # You can use actual datetime later
        self.tags = tags or []
        self.approx_identity = None #CHECK this one

        #now you need episodic memory (what they saw before) and optionally semantic memory (learned facts)
        #class Memory and class MemoryEntry perhaps overlap and classs memory should be more a container and handler,
        #for both types of memory, handling decay and promotion of episodic to semantic.


    def recall(self):
        return f"Memory of {self.subject}: {self.details} (Importance: {self.importance}, Tags: {self.tags})"
    
class MemoryEntry:
    def __init__(self, event_type, target, description, timestamp=None, **kwargs):
        self.event_type = event_type  # "robbery", "conversation", "sighting"
        self.target = target  # Could be a character or location
        self.description = description
        self.timestamp = timestamp or time.time()
        self.further_realizations = [] # when character think() about this memory, they might unlock an insight here
        self.similarMemories = [] #for pattern spotting. "Shes done this before..."
    """ Memory Decay System
    for memory in character.memory:
    memory.importance -= 1
    character.memory = [m for m in character.memory if m.importance > 0] """

class FactionRelatedMemory(Memory):
    """ Knowledge of how the world works, and how this relates to the faction. Entries known by 
    all cahracter in a factions self.members """
    def __init__(self, subject, details, importance=5):
        self.it_worked_there_before = {} # location/actions or action list