#anchor_visit.py

from dataclasses import dataclass, field
from typing import Optional, Any, Dict, Iterable
from anchor_utils import Anchor
from debug_utils import debug_print

from worldQueries import get_region_knowledge


@dataclass
class VisitAnchor(Anchor):
    """Generic anchor for visit-style motivations."""
    preferred_tags: list[str] = None
    avoid_tags: list[str] = None

    def get_best_target(self, npc) -> Optional[Any]:
        """Scan npc.percepts or npc.memory for locations matching desired tags."""
        candidates = []

        for percept in getattr(npc, "percepts", []):
            tags = percept.get("tags", [])
            obj = percept.get("object")
            
            if obj is None:
                continue

            # Filter by desired tags
            if self.preferred_tags and not any(t in tags for t in self.preferred_tags):
                continue
            if self.avoid_tags and any(t in tags for t in self.avoid_tags):
                continue

            sal = self.compute_salience_for(percept, npc)
            candidates.append((sal, obj))

        if not candidates:
            debug_print(npc, f"[ANCHOR VISIT] No candidates found for {self.name}", category="anchor")
            return None

        candidates.sort(key=lambda x: x[0], reverse=True)
        best_sal, best_obj = candidates[0]
        debug_print(npc, f"[ANCHOR VISIT] Best target = {best_obj} (sal={best_sal})", category="anchor")

        return best_obj

    def compute_salience_for(self, percept_data, npc):
        """
        Optional reinforcement for VisitAnchor.
        Emphasizes locations relevant to the NPC's current motivation
        (e.g., seeking weapons, robbery, or faction alignment).
        """

        debug_print(npc, f"[ANCHOR-SALIENCE] VisitAnchor computing for {percept_data.get('name')}", category="salience")
        debug_print(npc, f"[SALIENCE DEBUG] {self.name} anchor evaluating {obj.name}, tags={getattr(obj, 'tags', None)} -> score={salience}", category="salience")

        tags = percept_data.get("tags", [])
        salience = percept_data.get("salience", 1.0)

        # Boost if the location is associated with relevant motivations
        if npc.motivation_manager.is_active("obtain_ranged_weapon") and "weapon" in tags:
            salience *= 1.5

        if npc.motivation_manager.is_active("rob") and "robbable" in tags:
            salience *= 1.3

        # Rival faction presence can also increase salience slightly
        if "rival_faction" in tags:
            salience *= 1.2

        return salience


        



@dataclass
class VisitToRobAnchor(VisitAnchor):
    """Anchor that evaluates which location is most robbable or weapon-relevant."""
    preferred_tags: list = field(default_factory=lambda: ["shop", "weapon", "cash_register"])
    avoid_tags: list = field(default_factory=lambda: ["police_station", "guard"])
    synergy_matrix: dict = field(default_factory=lambda: {
        ("ranged_weapon", "cash_register"): 3.0,
        ("shop", "robbable"): 1.5,
    })

    def _ensure_percept(self, candidate: Any, npc) -> Dict:
        """
        Accepts either a percept dict or an object (Location/Perceptible).
        Returns a percept-like dict with keys 'object','name','tags','salience',...
        """
        if isinstance(candidate, dict):
            return candidate
        # object path: try to call get_percept_data(observer) if available
        if hasattr(candidate, "get_percept_data"):
            percept = candidate.get_percept_data(observer=npc) or {}
        else:
            percept = {}

        # safe defaults for the fields we use
        percept.setdefault("object", candidate)
        percept.setdefault("name", getattr(candidate, "name", str(candidate)))
        percept.setdefault("tags", getattr(candidate, "tags", []))
        percept.setdefault("salience", percept.get("salience", 1.0))
        # expose helpful booleans
        percept.setdefault("robbable", getattr(candidate, "robbable", False))
        # inventory and security we keep on the object itself, but include quick view
        percept.setdefault("has_pistol", getattr(getattr(candidate, "inventory", None), "has_item", lambda *a, **k: False)("Pistol") if getattr(candidate, "inventory", None) else False)
        percept.setdefault("security_level", getattr(getattr(candidate, "security", None), "level", 0) if getattr(candidate, "security", None) else 0)
        return percept

    def compute_salience_for(self, percept_data: Any, npc) -> float:
        """
        Compute robbery-oriented salience for a single candidate (location or percept dict).
        Returns a scalar float.
        """
        # Defensive: accept either a percept dict or a location object
        percept = self._ensure_percept(percept_data, npc)
        location = percept.get("object")
        debug_print(npc, f"[ANCHOR-SALIENCE] VisitToRobAnchor computing for {percept.get('name')}", category="salience")
        debug_print(npc, f"[SALIENCE DEBUG] {self.name} anchor evaluating {obj.name}, tags={getattr(obj, 'tags', None)} -> score={salience}", category="salience")

        score = 0.0

        # --- 0) Base salience from percept itself (allows designer control) ---
        base_sal = float(percept.get("salience", 1.0))
        score += base_sal

        # --- 1) Region knowledge (memory-local, subjective) ---
        region_name = getattr(getattr(npc, "region", None), "name", None)
        rk = None
        if region_name:
            # prefer npc.mind.memory.find_region_knowledge(...) for subjective knowledge
            try:
                rk = npc.mind.memory.find_region_knowledge(region_name)
            except Exception:
                rk = None

        if rk:
            # If the NPC's region-knowledge lists the candidate as a shop -> boost
            if hasattr(rk, "shops") and getattr(location, "name", None) in getattr(rk, "shops", []):
                score += 2.5
            # Known location listing gives smaller boost
            if hasattr(rk, "locations") and getattr(location, "name", "").lower() in (name.lower() for name in getattr(rk, "locations", [])):
                score += 1.0

        # --- 2) Semantic memory: shop/weapon knowledge (subjective facts) ---
        semantic = getattr(npc.mind, "memory", {}).semantic if getattr(npc.mind, "memory", None) else {}
        shop_memories = semantic.get("shop_knowledge", []) if isinstance(semantic, dict) else []
        for mem in shop_memories:
            if getattr(mem, "source", None) == location:
                tags = getattr(mem, "tags", []) or []
                if any("ranged_weapon" in t for t in tags):
                    score += 3.0
                if "robbable" in tags:
                    score += 2.0

        # --- 3) Thoughts: recent thought-based recall (soft boosts) ---
        for thought in getattr(npc.mind, "thoughts", []) or []:
            # a thought.content may be a string; check name containment defensively
            candidate_name = getattr(location, "name", None)
            if candidate_name and candidate_name in str(getattr(thought, "content", "")):
                thought_tags = getattr(thought, "tags", []) or []
                if "ranged_weapon" in thought_tags:
                    score += 1.5
                if "shop" in thought_tags:
                    score += 0.5
                if "robbable" in thought_tags:
                    score += 1.0

        # --- 4) Direct/percept-level traits (objective layer) ---
        # Use percept booleans we prepared above
        if percept.get("robbable", False):
            score += 2.5
        if percept.get("has_pistol", False):
            score += 2.0

        sec_level = int(percept.get("security_level", 0) or 0)
        if sec_level:
            score -= sec_level * 1.5  # penalize high security

        # --- 5) Tag-based fine tuning and preferred/avoid lists ---
        tags: Iterable[str] = percept.get("tags", []) or []
        for t in tags:
            if t in self.preferred_tags:
                score += 0.5
            if t in self.avoid_tags:
                score -= 0.5
            # any custom tag weight on the anchor
            score += self.tag_weights.get(t, 0.0)

        # --- 6) Synergy bonuses (combinations of tags) ---
        tagset = set(tags)
        for (a, b), bonus in self.synergy_matrix.items():
            if a in tagset and b in tagset:
                score += bonus

        # --- 7) Final weight scaling and clamp ---
        final = round(score * float(getattr(self, "weight", 1.0)), 2)
        # optionally clamp to a sane range (e.g., >= 0)
        if final < 0:
            final = 0.0
        return final