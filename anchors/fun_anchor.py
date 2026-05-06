#anchors.fun_anchor.py
from anchors.anchor import Anchor
from debug_utils import debug_print

class FunAnchor(Anchor):
    type = "leisure"
    name = "have_fun"
    desired_tags = ["social", "fun"]

    def is_valid(self):
        npc = self.owner
        return not npc.motivation_manager.is_suppressed("have_fun")

    def requires_movement(self):
        npc = self.owner
        target = self.resolve_target_location()
        if target is None:
            return False
        return target != npc.location

    def resolve_target_location(self):
        npc = self.owner
        recent_locs = {id(loc) for loc, _ in getattr(npc, "recently_visited", [])}

        PREF_MAP = {
            "Park": "nature",
            "SportsCentre": "sport",
            "Library": "learning",
            "Cafe": "social",
        }

        prefs = getattr(npc, "fun_prefs", None)
        best = None
        best_score = -999
        scores = []

        # Primary pass — exclude recently visited
        for loc in npc.region.locations:
            if loc == npc.location:
                continue
            if id(loc) in recent_locs:
                continue
            if loc.__class__.__name__ not in PREF_MAP:
                continue

            base_fun = getattr(loc, "fun", 0)
            pref_key = PREF_MAP[loc.__class__.__name__]
            pref_bonus = getattr(prefs, pref_key, 0) if prefs else 0
            score = base_fun + pref_bonus
            scores.append((loc.name, score))

            if score > best_score:
                best_score = score
                best = loc

        # Fallback pass — all fun locations recently visited, ignore recency
        if best is None:
            npc.recently_visited.clear()
            for loc in npc.region.locations:
                if loc == npc.location:
                    continue
                if loc.__class__.__name__ not in PREF_MAP:
                    continue

                base_fun = getattr(loc, "fun", 0)
                pref_key = PREF_MAP[loc.__class__.__name__]
                pref_bonus = getattr(prefs, pref_key, 0) if prefs else 0
                score = base_fun + pref_bonus
                scores.append((loc.name, score))

                if score > best_score:
                    best_score = score
                    best = loc

        scores.sort(key=lambda x: -x[1])
        summary = " | ".join(f"{name}={sc}" for name, sc in scores)
        debug_print(npc, f"[FUN TARGET] {summary} → {best.name if best else 'None'}",
                    category="fun")
        return best
