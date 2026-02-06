def reflect_on_ambient_scenes(char):
    scenes = char.mind.memory.semantic.get("ambient_scenes", [])
    if len(scenes) < 3:
        return

    avg = [0.0] * len(NARRATIVE_AXES)
    for s in scenes[-5:]:
        for i, v in enumerate(s["vector"]):
            avg[i] += v
    avg = [v / 5 for v in avg]

    dominant_axis = max(range(len(avg)), key=lambda i: abs(avg[i]))
    axis_name = NARRATIVE_AXES[dominant_axis]

    char.mind.add_thought(Thought(
        subject="Reflection",
        content=f"Things lately feel tilted toward {axis_name.replace('_', ' ')}",
        urgency=3,
        tags=["reflection", "ambient"]
    ))
