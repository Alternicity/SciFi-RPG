#ambience/scene/npc vibe analysis




if scene_vector[0] > 0.5:  # high conflict
    char.add_anchor(Anchor(
        name="seek_stability",
        priority=scene_vector[0] * 5
    ))
