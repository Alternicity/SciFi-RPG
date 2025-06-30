#character_mind.py
from collections import deque
from dataclasses import dataclass, field
import time
from typing import Optional, List, Any
import random
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
        self.obsessions: List[Obsession] = []
        self.max_thinks_per_tick=1
        self.default_focus = None

        #Consider syncing Character.social_connections["enemies"] with mind.memory.semantic["enemies"] at periodic intervals

        #Future idea
        #npc.thinking_style = "scatterbrain" Many thoughts
        #npc.thinking_style = "disciplined"

        # encapsulate both episodic + semantic
        #adding this here should probably deprecate the self.memory = Memory() in class Character
        #this will necessitate refactoring all code that writes to charcter.memory
        #and move functions from Mind to memory that affect memories

        """ deque prevents memory bloat. 
        It mimics short-term/working memory: older thoughts are automatically discarded. """

    def regain_focus(self):
        if not self.attention_focus and hasattr(self, "default_focus"):
            if random.random() < self.concentration / 10:
                self.regain_focus()
                print(f"[FOCUS] {self.name} is regaining attention focus on: {self.default_focus}")
                self.attention_focus = self.default_focus

    def get_episodic(self):
        return self.memory.episodic
    
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

    def has_similar_thought(self, new_thought):
        return any(t.content == new_thought.content for t in self.thoughts)

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
        """ You may eventually want to detect duplicates not just 
        by .content but also by .subject or .tags depending on future use cases """
        
    def check_obsessions(self):
        for obsession in self.obsessions:
            obsession.decay()
            if obsession.should_reactivate():
                thought = Thought(
                    subject=self.owner.name,
                    content=f"[Recurring] {obsession.content}",
                    origin=obsession.origin,
                    urgency=min(10, obsession.intensity * 2),
                    tags=obsession.tags + ["obsession"]
                )
                self.thoughts.append(thought)
                obsession.strengthen(0.05)

    def add_obsession(self, content, origin=None, tags=None):
        for o in self.obsessions:
            if o.content == content:
                o.strengthen()
                return
        self.obsessions.append(Obsession(content=content, origin=origin, tags=tags or []))

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
    

@dataclass
class Obsession:
    content: str  # Core of the recurring theme
    tags: List[str] = field(default_factory=list)
    origin: Optional[Any] = None  # MemoryEntry, Thought, ObjectInWorld, etc.
    intensity: float = 1.0  # Grows with reactivation, fades without stimulation
    recurrence_rate: float = 0.05  # Chance per tick to return as thought
    last_invoked: float = field(default_factory=time.time)
    dream_potential: float = 0.2  # Probability it shows up in dreams
    resolved: bool = False

    def should_reactivate(self) -> bool:
        """Determine if the obsession should resurface as a thought."""
        if self.resolved:
            return False
        from random import random
        return random() < self.recurrence_rate * self.intensity

    def strengthen(self, amount=0.1):
        self.intensity = min(self.intensity + amount, 10)
        self.last_invoked = time.time()

    def decay(self, rate=0.01):
        self.intensity = max(0.0, self.intensity - rate)