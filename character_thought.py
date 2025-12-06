#character_thought.py
import time

from LunaMath import FractalRoot
from typing import Optional, Any, List

# ✅ Import the actual game state accessor, not the class
from create.create_game_state import get_game_state
from debug_utils import debug_print  # optional, if you want to log failures


class Thought:
    def __init__(self, subject, content, origin=None, urgency=1, tags=None, source=None, anchored=False, weight=0, timestamp=None, resolved=False, corollary=None):
        self.subject = subject              #The object the thought is about. Character, faction, event, ObjectInWorld etc
        self.content = content              # Description of the thought (str or object)
        self.origin = origin                # What caused it (e.g., percept source)
        self.urgency = urgency              # How pressing it is
        self.tags = tags or []              # Useful for filtering (e.g., ["crime", "money"])
        self.source = source                # Who/what told them (e.g., another character)
        self.anchored = anchored
        self.weight = weight                # How impactful (can be salience or derived)
        self.timestamp = timestamp or time.time()

        # Simulation time (safe and optional)
        try:
            state = get_game_state()
            self.tick = getattr(state, "tick", None)
            self.day = getattr(state, "day", None)
        except Exception as e:
            self.tick = None
            self.day = None
            # Optional debug: only print in development / debug mode
            debug_print(
                None,
                f"[THOUGHT INIT] Warning: Could not access game state: {e}",
                category="think"
            )

        self.resolved = resolved
        self.corollary_of = None
        self.corollary = corollary or []  # a corollary will probably be another thought object

        self.function_reference = {}
        self.associated_function = None

    
    def primary_tag(self) -> Optional[str]:
        """Return the most characteristic or first tag."""
        if not self.tags:
            return None
        return self.tags[0]

    def mark_resolved(self):
        self.resolved = True

    def spawn_corollary_thoughts(self, character):
        results = []
        if not self.corollary:
            return results

        for i, cor_thought in enumerate(self.corollary):
            if character.intelligence >= (13 + i * 2):
                new = Thought(
                    content=f"Corollary derived: {cor_thought.content}",
                    origin="CorollaryMemory",
                    urgency=self.urgency - 1,
                    tags=["corollary"] + cor_thought.tags,
                    source=cor_thought
                )
                results.append(new)
        return results
    
    def salience_for(self, observer, anchor=None):
        """
        Computes how salient this thought is to the observer.
        Anchor is optional and should compute salience relative to itself.
        """
        if anchor is None:
            anchor = getattr(observer, "current_anchor", None)
        # Prefer anchor-driven computation:
        if anchor is not None and hasattr(anchor, "compute_salience_for"):
            return anchor.compute_salience_for(self, observer)
        
        # Fallback to global compute_salience helper
        from ai.ai_utility import compute_salience
        return compute_salience(self, observer, anchor)

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

    def __str__(self):
        return self.content
        #return f"'{self.content}' (urgency: {self.urgency})"


    def __repr__(self):
        return (f"<Thought: '{self.content}' | origin='{getattr(self.origin, 'name', self.origin)}', "
                f"source='{getattr(self.source, 'name', self.source)}', urgency={self.urgency}, "
                f"tags={self.tags}, time={int(self.timestamp)}>")
    
    """ Minor optional tweaks for clarity or future-proofing:

Add timestamp if needed later (you’ve used it before in the namedtuple)

Add a .to_dict() or .summarize() method for UI/debug/logging, if needed

Add __eq__ or __hash__ methods if you'll compare or de-duplicate thoughts """

class FailedThought(Thought):
    def __init__(self, content, cause=None, **kwargs):
        super().__init__(content=content, tags=["error", "fail"], **kwargs)
        self.cause = cause

    #usage
    """ try:
        result = build_triangle()
    except Exception as e:
        self.npc.mind.add_thought(FailedThought("Couldn't build triangle", cause=str(e))) """
    
class ThoughtTools():
    pass

class FractalThought:
    def __init__(self, signal, amplitude):
        self.signal = signal
        self.amplitude = amplitude
        self.fractal_root = FractalRoot(amplitude)

    def encoded_geometry(self):
        upper, lower = self.fractal_root.pair()
        return {
            'constructive_wave': upper,
            'destructive_wave': lower,
            'resonant_value': self.fractal_root.product()
        }
    """ Given the Codex's framing of thought as structured wave interference
    and memory as phase-locked resonance patterns, a FractalRoot can be woven
    into these objects to encode field coherence or symbolic weight. """
