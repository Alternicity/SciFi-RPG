#character_mind.py
from collections import deque
from character_thought import Thought
from character_memory import Memory

class Mind:
    def __init__(self, owner=None, capacity=None):
        #Not responsible for judgment — it just holds the data
        self.owner = owner #is this setting to None?

        capacity = capacity if capacity is not None else getattr(owner, 'intelligence', 10)
        self.thoughts = deque(maxlen=capacity)
        self.corollaries = deque(maxlen=capacity)
        self.memory = Memory()
        self.max_thinks_per_tick=1
        #Consider syncing Character.social_connections["enemies"] with mind.memory.semantic["enemies"] at periodic intervals

        # encapsulate both episodic + semantic
        #adding this here should probably deprecate the self.memory = Memory() in class Character
        #this will necessitate refactoring all code that writes to charcter.memory
        #and move functions from Mind to memory that affect memories

        """ deque prevents memory bloat. 
        It mimics short-term/working memory: older thoughts are automatically discarded. """

    def get_all(self):
        return list(self.thoughts)

    def clear(self):
        self.thoughts.clear()

    def __iter__(self):
        return iter(self.thoughts)

    def urgent(self, min_urgency):
        return sorted(
            [t for t in self.thoughts if hasattr(t, 'urgency') and t.urgency >= min_urgency],
            key=lambda t: t.urgency,
            reverse=True
        )

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
        
    def add_thought_to_enemies(self, thought):
        self.memory.semantic.setdefault("enemies", []).append(thought)

    def store_corollary(character, thought):
        """Store a corollary Thought if it's not already remembered."""
        existing = [t.content for t in character.mind.corollaries]
        if thought.content not in existing:
            character.mind.corollaries.append(thought)

    """ keep urgent() in Mind.
Heres why:
The mind owns the thoughts and should manage querying/filtering them.
It respects the Single Responsibility Principle: GangMemberAI can ask 
the mind for urgent thoughts but shouldnt know how to filter them.
Keeps AI logic decoupled from low-level data structure logic. 
If AI needs more complex logic, you can subclass or extend it — but basic filtering is a data responsibility."""

class Curiosity:
    def __init__(self, base_score=10):
        self.base = base_score  # General openness
        self.interests = {}     # Specific: {"geometry": 14, "sound": 8}

    def increase(self, topic, amount=1):
        self.interests[topic] = self.interests.get(topic, 0) + amount

    def decrease(self, topic, amount=-1):
        self.interests[topic] = self.interests.get(topic, 0) + amount

    def get(self, topic):
        return self.interests.get(topic, self.base)