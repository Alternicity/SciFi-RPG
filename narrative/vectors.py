VIBE_VECTORS = {
    "peace":        (-1,  1,  0,  1),
    "order":        ( 0,  1,  1,  1),
    "clarity":      ( 0,  1,  0,  1),
    "social":       ( 0,  0,  1,  0),
    "psy":          ( 1,  0,  1,  1),
}

def ambience_to_vector(ambience: dict[str, float]) -> tuple[float, ...]:
    vector = [0.0] * 4
    for vibe, mag in ambience.items():
        if vibe in VIBE_VECTORS:
            for i, component in enumerate(VIBE_VECTORS[vibe]):
                vector[i] += component * mag
    return tuple(vector)
