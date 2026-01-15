#memory.ambient_scene_memory.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from memory.memory_entry import MemoryEntry

@dataclass
class AmbientSceneMemory(MemoryEntry):
    """
    A compressed semantic memory representing how a location feels over time.
    """

    location: Optional[str] = None

    # Raw aggregated ambience (post-psy filtering)
    dominant_vibes: Dict[str, float] = field(default_factory=dict)

    # Narrative-space compression
    narrative_vector: Optional[tuple] = None

    # Time
    first_observed_day: Optional[int] = None
    first_observed_hour: Optional[int] = None
    last_updated_day: Optional[int] = None
    last_updated_hour: Optional[int] = None

    # Social context
    social_context: Dict[str, List[str]] = field(default_factory=dict)

    # Long-term compressed social memory
    friends_seen: List[str] = field(default_factory=list)
    enemies_seen: List[str] = field(default_factory=list)
    allies_seen: List[str] = field(default_factory=list)
    others_present: List[str] = field(default_factory=list)

    # Exposure metrics
    visit_count: int = 0          # distinct visits
    exposure_count: int = 0       # cumulative updates while present

    def update_from_observation(
        self,
        perceived_ambience: Dict[str, float],
        narrative_vector: tuple,
        social_context: Dict[str, List[str]],
        *,
        current_day: int | None = None,
        current_hour: int | None = None,
    ):
        """
        Merge a new ambient perception into this scene memory.
        """

        # --- Exposure bookkeeping ---
        self.exposure_count += 1

        # --- Blend dominant vibes (EMA-style) ---
        for k, v in perceived_ambience.items():
            prev = self.dominant_vibes.get(k, 0.0)
            self.dominant_vibes[k] = (prev * 0.7) + (v * 0.3)

        # --- Narrative vector accumulation ---
        if self.narrative_vector is None:
            self.narrative_vector = narrative_vector
        else:
            self.narrative_vector = tuple(
                a + b for a, b in zip(self.narrative_vector, narrative_vector)
            )

        # --- Social context ---
        self.social_context = social_context

        for key in ("friends_seen", "enemies_seen", "allies_seen"):
            existing = set(getattr(self, key))
            existing.update(social_context.get(key, []))
            setattr(self, key, list(existing))

        self.others_present = list(
            set(self.others_present).union(
                social_context.get("others_present", [])
            )
        )

        # --- Temporal update ---
        self.last_updated_day = current_day
        self.last_updated_hour = current_hour




