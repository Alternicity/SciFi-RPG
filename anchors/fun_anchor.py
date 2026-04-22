#anchors.fun_anchor.py
from anchors.anchor import Anchor

class FunAnchor(Anchor):

    #one anchor, many targets
    type = "fun"
    name = "fun"
    desired_tags = ["social", "fun"]

    def choose_target(self):

        npc = self.owner

        best = None
        best_score = -999

        for loc in npc.region.locations:

            base_fun = getattr(loc, "fun", 0)

            pref_bonus = npc.fun_prefs.get(loc.__class__.__name__, 0)

            score = base_fun + pref_bonus

            if score > best_score:
                best_score = score
                best = loc

        return best