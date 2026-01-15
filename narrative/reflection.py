def reflect_on_ambient_memories(character):
    scenes = character.mind.memory.semantic.get("ambient_scenes", [])
    if not scenes:
        return

    avg_vector = [0, 0, 0, 0]
    for s in scenes[-5:]:
        for i, v in enumerate(s["summary"]["narrative_vector"]):
            avg_vector[i] += v

    # normalize
    avg_vector = [v / 5 for v in avg_vector]

    if avg_vector[0] < -0.5:
        character.mind.add_thought(Thought(
            subject="Reflection",
            content="I feel drawn to calmer places lately.",
            urgency=2,
            tags=["reflection", "mood"]
        ))
