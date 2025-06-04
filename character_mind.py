#character_mind.py
from collections import deque
from character_thought import Thought

class Mind:
    def __init__(self, owner=None, capacity=None):
        #Not responsible for judgment — it just holds the data

        self.owner = owner #is this setting to None?
        capacity = capacity if capacity is not None else getattr(owner, 'intelligence', 10)
        self.thoughts = deque(maxlen=capacity)
        """ deque prevents memory bloat. 
        It mimics short-term/working memory: older thoughts are automatically discarded. """

        self.episodic = []   # recent personal experiences (MemoryEntry objects), should this be a deque as well?

        self.semantic = []   # general knowledge (MemoryEntry objects)

    def add_episodic(self, memory_entry):
        self.episodic.append(memory_entry)

    def add_semantic(self, memory_entry):
        self.semantic.append(memory_entry)

    def get_all(self):
        return list(self.thoughts)

    def get_all_episodic(self):
        return list(self.episodic)

    def get_all_semantic(self):
        return list(self.semantic)

    def clear(self):
        self.thoughts.clear()

    def __iter__(self):
        return iter(self.thoughts)

    def urgent(self, min_urgency):
        return [t for t in self.thoughts if t.urgency >= min_urgency]

    def add_thought(self, thought: Thought):
        """
        Adds a thought to the mind, avoiding duplicates by content.
        Optionally, can be enhanced to merge/update existing thoughts.
        """
        for existing in self.thoughts:
            if existing.content == thought.content:
                # Update urgency if new one is stronger
                if thought.urgency > existing.urgency:
                    existing.urgency = thought.urgency
                    existing.timestamp = thought.timestamp
                return  # Don't add duplicate content

        self.thoughts.append(thought)
        #print(f"[MIND] Added thought: {thought.content}")
        
    """ keep urgent() in Mind.
Heres why:
The mind owns the thoughts and should manage querying/filtering them.
It respects the Single Responsibility Principle: GangMemberAI can ask 
the mind for urgent thoughts but shouldnt know how to filter them.
Keeps AI logic decoupled from low-level data structure logic. 
If AI needs more complex logic, you can subclass or extend it — but basic filtering is a data responsibility."""
