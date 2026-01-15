# memory/ambience_utils.py

from memory.ambient_scene_memory import AmbientSceneMemory
from narrative.vectors import ambience_to_vector


def update_ambient_scene_memory(
    *,
    char,
    loc,
    perceived_ambience: dict,
    peak_tag: str,
    peak_power: float,
    social_data: dict,
    current_day: int | None = None,
    current_hour: int | None = None,
):
    """
    Create or update a single AmbientSceneMemory for a character + location.
    """

    vector = ambience_to_vector(perceived_ambience)

    semantic = char.mind.memory.semantic
    scenes = semantic.setdefault("ambient_scenes", [])

    # Try to find existing scene memory for this location
    existing = next(
        (m for m in scenes
         if isinstance(m, AmbientSceneMemory)
         and m.location == loc.name),
        None
    )

    if existing:
        existing.update_from_observation(
            perceived_ambience,
            vector,
            social_data,
            current_day=current_day,
            current_hour=current_hour,
        )
        return existing

    # Otherwise create a new one
    scene = AmbientSceneMemory(#line 46
        subject=char.name,
        object_=loc.name,
        verb="experienced",
        details=f"The atmosphere of {loc.name}",
        location=loc.name,
        dominant_vibes={peak_tag: peak_power},
        narrative_vector=vector,
        tags=["ambient_scene", peak_tag],
        type="ambient_scene",
        initial_memory_type="semantic",
        owner=char,
        source=loc,
        first_observed_day=current_day,
        first_observed_hour=current_hour,
        last_updated_day=current_day,
        last_updated_hour=current_hour,
        visit_count=1,
        exposure_count=1,
        )

    scenes.append(scene)
    return scene
