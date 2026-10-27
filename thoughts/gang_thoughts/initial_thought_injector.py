#thoughts.gang_thoughts.initial_thought_injector.py
from thoughts.gang_thoughts.thought_builders.gang_thought_builder import build_pistol_capture_thought
#not contained in the tc4 structure, but is part of it
def inject_pistol_capture_thought(
    npc,
    boss,
    pistol,
    rival_boss,
    rival_gang
):
    thought = build_pistol_capture_thought(
        npc,
        boss,
        pistol,
        rival_boss,
        rival_gang
    )

    npc.mind.add_thought(thought)