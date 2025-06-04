#character_thought.py
import time

class Thought:
    def __init__(self, subject, content, origin=None, urgency=1, tags=None, source=None, weight=0, timestamp=None, resolved=False, corollary=None):
        self.subject = subject              #The object the thought is about. Character, faction, event, ObjectInWorld etc
        self.content = content              # Description of the thought (str or object)
        self.origin = origin                # What caused it (e.g., percept source)
        self.urgency = urgency              # How pressing it is
        self.tags = tags or []              # Useful for filtering (e.g., ["crime", "money"])
        self.source = source                # Who/what told them (e.g., another character)
        self.weight = weight                # How impactful (can be salience or derived)
        self.timestamp = timestamp or time.time()
        self.resolved = resolved
        self.corollary = corollary or []  # list of strings or callables, Functions or object

    def mark_resolved(self):
        self.resolved = True

    def spawn_corollary_thoughts(self, character):
        #Later you can replace .corollary with a LinkedCorollary object.
        thoughts = []
        if not self.corollary:
            return thoughts
        
        # simple rule-based system
        for i, cor in enumerate(self.corollary):
            if character.intelligence > (13 + i * 2):

                """ loop through corollary thoughts indexed by i.
                A character will "unlock" more advanced corollaries if their intelligence is higher.
                The thresholds are staggered: int 13, 15, 17 """

                new_thought = Thought(
                    content=f"Corollary goal: {cor.replace('_', ' ').title()}",
                    origin="CorollaryEngine",
                    urgency=self.urgency - 1,
                    tags=["corollary", "goal"],
                    source="CorollaryThought",
                )
                thoughts.append(new_thought)
        return thoughts

    def compute_salience(self, observer):
        if hasattr(self, 'memory') and self.memory:
            return self.memory.origin.compute_salience(observer)
        return 0

    def summary(self, include_source=False, include_time=False):
        parts = [
            f"'{self.content}'",
            f"origin='{getattr(self.origin, 'name', self.origin)}'",
            f"urgency={self.urgency}",
            f"tags={self.tags}"
        ]
        if include_source:
            parts.append(f"source='{getattr(self.source, 'name', self.source)}'")
        if include_time:
            parts.append(f"time={int(self.timestamp)}")
        return f"<Thought: {', '.join(parts)}>"

    def __repr__(self):
        return (f"<Thought: '{self.content}' | origin='{getattr(self.origin, 'name', self.origin)}', "
                f"source='{getattr(self.source, 'name', self.source)}', urgency={self.urgency}, "
                f"tags={self.tags}, time={int(self.timestamp)}>")
    
    """ Minor optional tweaks for clarity or future-proofing:

Add timestamp if needed later (you’ve used it before in the namedtuple)

Add a .to_dict() or .summarize() method for UI/debug/logging, if needed

Add __eq__ or __hash__ methods if you'll compare or de-duplicate thoughts """