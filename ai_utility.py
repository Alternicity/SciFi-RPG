from ai_base import BaseAI

class UtilityAI(BaseAI):
    def choose_action(self, region):
        npc = self.npc
        print(f"\n[UtilityAI] Evaluating actions for {npc.name} in {region.name}...")

        for percept in npc.percepts:
            tags = percept.get("tags", [])
            origin = percept.get("origin")
            print(f"[Percept] Found percept: {percept.get('description')} with tags: {tags}")

            if "weapon" in tags and "steal" in npc.motivations:
                if not npc.has_weapon():
                    print(f"[Decision] {npc.name} decides to GoStealWeapon.")
                    return "GoStealWeapon"

            if "shop" in tags and "robbery" in npc.motivations:
                if npc.has_weapon():
                    print(f"[Decision] {npc.name} decides to Rob.")
                    return "Rob"

        print(f"[Decision] {npc.name} has no strong motivations. Idling.")
        return "Idle"

    def score_action(self, action_type, context):
        if action_type == "expand_territory":
            return 10 if context["rival_presence"] > 5 else 3
        elif action_type == "recruit":
            return 8 if context["faction_strength"] < 50 else 2
        return 1
