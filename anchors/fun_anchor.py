#anchors.fun_anchor.py
from anchors.anchor import Anchor

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
        #When you do add NPC-as-fun-source later, it fits naturally as a second resolver 
        npc = self.owner
        if not hasattr(npc, "fun_prefs") or npc.fun_prefs is None:
            # Fallback: any location tagged fun that isn't current
            candidates = [
                loc for loc in npc.region.locations
                if "fun" in getattr(loc, "tags", [])
                and loc != npc.location
            ]
            return candidates[0] if candidates else None

        best = None
        best_score = -999
        prefs = npc.fun_prefs

        # Map location classes to preference attributes
        PREF_MAP = {
            "Park": "nature",
            "SportsCentre": "sport", 
            "Library": "learning",
            "Park": "social",
        }

        for loc in npc.region.locations:
            if loc == npc.location:
                continue
            base_fun = getattr(loc, "fun", 0)
            class_name = loc.__class__.__name__
            pref_key = PREF_MAP.get(class_name, None)
            pref_bonus = getattr(prefs, pref_key, 0) if pref_key else 0
            score = base_fun + pref_bonus

            if score > best_score:
                best_score = score
                best = loc

        return best
