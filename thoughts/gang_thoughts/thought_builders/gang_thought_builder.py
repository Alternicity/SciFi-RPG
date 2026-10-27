#thoughts.gang_thoughts.thought_builders.gang_thought_builder.py
from character_thought import Thought


def build_pistol_capture_thought(
    npc,
    boss,
    pistol,
    rival_boss,
    rival_gang
):
    return Thought(
        subject=boss.name,
        content=(
            f"{boss.name} took the gold plated pistol "
            f"from the dead {rival_boss.name}, boss of the "
            f"{rival_gang.name}."
        ),
        urgency=20,
        tags=["gang", "weapon", "captured", "trophy"],
        source="seeded_debug_thought"
    )