#memory.memory_builders.memory_utils.py

def best_food_location(npc):
    food_kb = None

    for mem in npc.mind.memory.get_semantic():
        if getattr(mem, "type", None) == "food_sources":
            food_kb = mem
            break

    if not food_kb:
        return None

    region = npc.region
    candidates = []

    for loc in region.locations:
        if loc.name not in food_kb.locations:
            continue

        tags = getattr(loc, "tags", [])
        score = 0

        if "prepared_food" in tags:
            score += 5
        if "cafe" in tags or "restaurant" in tags:
            score += 3
        if "groceries" in tags or "shop" in tags:
            score += 1

        candidates.append((score, loc))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]




