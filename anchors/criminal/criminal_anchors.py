#anchors.criminal.criminal_anchors.py

from anchors.anchor import Anchor

class RobberyAnchor(Anchor):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "rob")
        kwargs.setdefault("type", "motivation")
        kwargs.setdefault("tags", ["robbery", "crime", "weapon"])
        kwargs.setdefault("desired_tags", ["ranged_weapon", "gun", "weapon"])
        kwargs.setdefault("disfavored_tags", ["security", "police", "alert_employee"])
        #"rival_faction" could figure in here, depending on a gangs violence_disposition

        # kwargs.setdefault(...) only sets a default if the key is not already present,
        # avoiding conflicts when name="rob" is already in kwargs.
        # Set default tag_weights if not already defined
        kwargs.setdefault("tag_weights", {
            "weapon": 0.5,
            "ranged_weapon": 0.7,#it’s a weighting factor, not a subtraction, 0.7 adds to total salience.
            "shop": 0.3,
            "security": -0.4,
            "police": -0.6,
            "alert_employee": -0.5,
        })

        super().__init__(**kwargs)

    def compute_salience_for(self, percept_data, npc) -> float:
        percept = self._coerce_to_percept(percept_data, npc)
        obj = percept.get("object")
        tags  = percept.get("tags", []) or []
        name = percept.get("name", "<unnamed>")

        # Ignore NPCs, events, etc.
        from events import Event
        if obj is npc or isinstance(obj, Event) or isinstance(obj, npc.__class__):
            return 0.0

        # base score from Anchor
        score = super().compute_salience_for(percept, npc)

        # Weapon-based adjustments
        if npc.inventory.has_ranged_weapon():
            score -= 0.4
        elif "ranged_weapon" in tags:
            score += 0.3
        elif "melee_weapon" in tags:
            score += 0.1

        # Extract robbery target name
        target_name = None
        content = getattr(obj, "content", None)
        if isinstance(content, str):
            import re
            m = re.search(r"rob\s+([A-Za-z0-9_'\-]+)", content, flags=re.IGNORECASE)
            if m:
                target_name = m.group(1)
                
        # Suppress turf-war salience logs
        if tags and "turf_war" in tags:
            return

        return round(score, 2)