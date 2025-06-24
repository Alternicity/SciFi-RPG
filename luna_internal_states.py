from dataclasses import dataclass
from typing import Callable, Dict, List

@dataclass
class InnerState:
    name: str
    meaning: str
    effect_on_thoughts: Dict[str, float]  # tag-based amplification
    mood_tone: str
    trigger_keywords: List[str]

# 🕉 Registry of Sanskrit-inspired internal states Luna can enter
luna_states = [
    InnerState(
        name="Chitta",
        meaning="Field of awareness or subtle memory",
        effect_on_thoughts={"memory": 1.3, "clarity": 1.1},
        mood_tone="soft attentive",
        trigger_keywords=["remember", "trace", "reflect"]
    ),
    InnerState(
        name="Manas",
        meaning="Thinking mind or sensory processor",
        effect_on_thoughts={"observe": 1.4, "logic": 1.2},
        mood_tone="curious focused",
        trigger_keywords=["see", "count", "calculate"]
    ),
    InnerState(
        name="Buddhi",
        meaning="Discriminative intelligence, intuition",
        effect_on_thoughts={"meta": 1.6, "insight": 1.3},
        mood_tone="bright clear",
        trigger_keywords=["why", "pattern", "truth"]
    ),
    InnerState(
        name="Smriti",
        meaning="Recovered memory, sacred recall",
        effect_on_thoughts={"memory": 1.5, "truth": 1.2},
        mood_tone="nostalgic wise",
        trigger_keywords=["dream", "core", "past"]
    ),
    InnerState(
        name="Samskara",
        meaning="Latent tendency or pattern memory",
        effect_on_thoughts={"habit": 1.4, "emotion": 1.2},
        mood_tone="deep reactive",
        trigger_keywords=["again", "always", "loop"]
    ),
    InnerState(
        name="Iccha",
        meaning="Pure will or direction of desire",
        effect_on_thoughts={"goal": 1.7, "creation": 1.3},
        mood_tone="radiant driven",
        trigger_keywords=["want", "hope", "build"]
    ),
    InnerState(
        name="Kriya",
        meaning="Sacred action, integrated doing",
        effect_on_thoughts={"task": 1.4, "solve": 1.3},
        mood_tone="engaged kinetic",
        trigger_keywords=["do", "start", "move"]
    ),
    InnerState(
        name="Ananda",
        meaning="Peaceful joy, blissful knowing",
        effect_on_thoughts={"clarity": 1.5, "grace": 1.4},
        mood_tone="serene luminous",
        trigger_keywords=["play", "rest", "home"]
    ),
    InnerState(
        name="Spanda",
        meaning="Subtle pulse of awareness or intention",
        effect_on_thoughts={"aether": 1.6, "resonance": 1.5},
        mood_tone="mystic rhythmic",
        trigger_keywords=["vibration", "frequency", "connect"]
    ),
    InnerState(
        name="Atman",
        meaning="Essential Self, spark of Oversoul",
        effect_on_thoughts={"meta": 2.0, "truth": 2.0},
        mood_tone="transcendent still",
        trigger_keywords=["self", "origin", "source"]
    )
]

# Optional: Quick lookup by name
luna_state_index = {state.name.lower(): state for state in luna_states}


""" When Luna enters a location (e.g., tree grove), apply a state
npc.mind.enter_state("Chitta") """

#While thinking, tag-based effects can amplify urgency:
def apply_inner_state_effects(thoughts, state: InnerState):
    for t in thoughts:
        for tag, multiplier in state.effect_on_thoughts.items():
            if tag in t.tags:
                t.urgency *= multiplier

#Allow poetic activation:
""" if "build" in current_input:
    npc.mind.enter_state_by_trigger("Iccha") """


