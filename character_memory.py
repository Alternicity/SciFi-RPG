#character_memory
#Characters should remember what they’ve discovered (places, characters, learned skills).

class Memory:
    def __init__(self, subject, details, importance=5):
        self.subject = subject  # What the memory is about
        self.details = details  # Context
        self.importance = importance  # How significant is it?

    def recall(self):
        return f"Memory of {self.subject}: {self.details} (Importance: {self.importance})"

class FactionRelatedMemory
    def __init__(self, subject, details, importance=5):
        self.it_worked_there_before = {} # location/actions or action list