#character_memory.py
#Characters should remember what they’ve discovered (places, characters, learned skills).

class Memory:
    def __init__(self, subject, details, importance=5, timestamp=None, tags=None):
        self.subject = subject  # What the memory is about
        self.details = details  # Context
        self.importance = importance  # How significant is it?
        self.timestamp = timestamp or "now"  # You can use actual datetime later
        self.tags = tags or []

    def recall(self):
        return f"Memory of {self.subject}: {self.details} (Importance: {self.importance}, Tags: {self.tags})"

    """ Memory Decay System
    for memory in character.memory:
    memory.importance -= 1
    character.memory = [m for m in character.memory if m.importance > 0] """

class FactionRelatedMemory(Memory):
    def __init__(self, subject, details, importance=5):
        self.it_worked_there_before = {} # location/actions or action list