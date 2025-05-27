#character_mind.py
from collections import deque
from character_thought import Thought

class Mind:
    def __init__(self, owner=None, capacity=None):

        self.owner = owner #is this setting to None?
        capacity = capacity if capacity is not None else getattr(owner, 'intelligence', 10)
        self.thoughts = deque(maxlen=capacity)
        self.episodic = []   # recent personal experiences (MemoryEntry objects)
        self.semantic = []   # general knowledge (MemoryEntry objects)

    def add_episodic(self, memory_entry):
        self.episodic.append(memory_entry)

    def add_semantic(self, memory_entry):
        self.semantic.append(memory_entry)

    def get_all(self):
        return list(self.thoughts)

    def clear(self):
        self.thoughts.clear()

    def __iter__(self):
        return iter(self.thoughts)

    def urgent(self, min_urgency):
        return [t for t in self.thoughts if t.urgency >= min_urgency]

    """ keep urgent() in Mind.
Heres why:
The mind owns the thoughts and should manage querying/filtering them.
It respects the Single Responsibility Principle: GangMemberAI can ask 
the mind for urgent thoughts but shouldnt know how to filter them.
Keeps AI logic decoupled from low-level data structure logic. 
If AI needs more complex logic, you can subclass or extend it — but basic filtering is a data responsibility."""
