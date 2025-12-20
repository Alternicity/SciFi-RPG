#character_mind.py
from collections import deque
from dataclasses import dataclass, field
import time
from typing import Optional, List, Any
import random
from character_thought import Thought
from character_memory import Memory
from debug_utils import debug_print

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
        self.default_focus = None #baseline
        self.attention_focus = None #momentary concern

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

    def remove_thoughts_with_tag(self, tag):
        self.thoughts = [t for t in self.thoughts if tag not in t.tags]

    def deduplicate_thoughts(self, npc):#eventually ditch the npc
        seen = {}
        unique_thoughts = []
        for t in npc.mind.thoughts:
            if t.content not in seen:
                seen[t.content] = t
                unique_thoughts.append(t)
            else:
                # Optionally increment a counter
                seen[t.content].repetition_count = getattr(seen[t.content], "repetition_count", 1) + 1
        from collections import deque
        npc.mind.thoughts = deque(unique_thoughts, maxlen=getattr(npc.mind.thoughts, "maxlen", 10))

    def remove_thought_by_predicate(self, predicate):
        removed = []
        for t in list(self.thoughts):
            if predicate(t):
                self.thoughts.remove(t)
                removed.append(t)

        for t in removed:
            debug_print(self.owner, f"[MIND] Removed thought: {t.content}", "think")


    def has_thought_content(self, content_substring: str) -> bool:
        """
        Returns True if any current thought's content matches or contains the given substring.
        """
        for thought in self.thoughts:
            if content_substring in thought.content:
                debug_print(f"[THOUGHT CHECK] {self.owner.name} checking for thought containing: '{content_substring}'", category="think")
                return True
        return False


    def find_thought_by_tag(self, tag: str):
        """
        Returns the first thought containing a given tag.
        Useful for debugging salience loops or repeated anchors.
        """
        for thought in self.thoughts:
            if tag in thought.tags:
                return thought
        return None

    def regain_focus(self):
        if not self.attention_focus and self.default_focus:
            if random.random() < self.concentration / 10:
                self.attention_focus = self.default_focus
                print(f"[FOCUS] {self.owner.name} is regaining attention focus on: {self.default_focus}")


    def get_episodic(self):
        return self.memory.episodic
    
    def get_all(self):
        return list(self.thoughts)

    def clear(self):
        self.thoughts.clear()

    def remove_thought_by_content(self, content: str):
        # Determine capacity safely (if list, fall back to default)
        maxlen = getattr(self.thoughts, "maxlen", None) or 10  # or your default capacity
        filtered = [t for t in self.thoughts if t.content.lower() != content.lower()]
        self.thoughts = deque(filtered, maxlen=maxlen)

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

        print("[DEBUG] add_thought called; content repr:", repr(thought.content))

        # ensure mind knows its owner
        owner = getattr(self, "owner", None)
        debug_print(f"[MIND] add_thought to owner={getattr(owner,'name',None)} id={id(owner)}: {thought.content}", category="think")

        for existing in self.thoughts:
            if existing.content == thought.content:
                # Update urgency if new one is stronger
                if thought.urgency > existing.urgency:
                    existing.urgency = thought.urgency
                    existing.timestamp = thought.timestamp
                return  # Don't add duplicate content

        self.thoughts.append(thought)

        from focus_utils import set_attention_focus
        set_attention_focus(self.owner, thought=thought)
        
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

    def clear_stale_percepts(self):
        """Placeholder: future logic will remove percepts that no longer reflect the game world."""
        debug_print(self.owner, "[MIND] clear_stale_percepts() called — no action (placeholder)", "percept")
        # In the future, check if any percept's object no longer exists or changed region/location.
        return
        #Is mind the right place for this? Where are percepts stored?

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