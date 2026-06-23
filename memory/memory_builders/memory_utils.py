#memory.memory_builders.memory_utils.py

def best_food_location(npc):

    food_kbs = npc.mind.memory.semantic.get("food_locations", [])
    if not food_kbs:
        return None

    #sanity fallback
    region = (
        getattr(npc.location, "region", None)
        or npc.region
    )

    food_kb = food_kbs[0]  # later: choose by salience / region

    if not food_kb:
        return None

    candidates = []

    for loc in region.locations:
        if loc.name not in food_kb.locations:
            continue

        tags = getattr(loc, "tags", [])
        score = 0

        if "prepared_food" in tags:
            score += 3
        if "cafe" in tags:
            score += 9  # was 3, now higher than restaurant
        if "restaurant" in tags:
            score += 3
        if "groceries" in tags or "shop" in tags:
            score += 1

        candidates.append((score, loc))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]




