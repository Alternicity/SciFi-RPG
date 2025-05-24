#ai_utility.py → If using Utility AI, scoring logic goes here.


from ai_base import BaseAI

class UtilityAI(BaseAI):
    def choose_action(self, npc, region):
        print(f"\n[UtilityAI] Evaluating actions for {npc.name} in {region.name}...")

        for percept in npc.percepts:
            tags = percept.get("tags", [])
            origin = percept.get("origin")
            print(f"[Percept] Found percept: {percept.get('description')} with tags: {tags}")

            if "weapon" in tags and "steal" in npc.motivations:
                if not npc.has_weapon():
                    print(f"[Decision] {npc.name} has motivation to steal and no weapon. Decides to GoStealWeapon.")
                    return "GoStealWeapon"

            if "shop" in tags and "robbery" in npc.motivations:
                if npc.has_weapon():
                    print(f"[Decision] {npc.name} is armed and motivated. Decides to Rob.")
                    return "Rob"

        print(f"[Decision] No strong motivation or percepts. {npc.name} will Idle.")
        return "Idle"


    def score_action(self, action_type, context):
        """Assigns a score to an action based on context."""
        if action_type == "expand_territory":
            return 10 if context["rival_presence"] > 5 else 3
        elif action_type == "recruit":
            return 8 if context["faction_strength"] < 50 else 2
        return 1
    
    def get_viable_robbery_targets(npc, region):
        return [
            loc for loc in region.locations
            if getattr(loc, "robbable", False)  # Only robbable locations
            and getattr(loc, "is_open", False)  # Optional: shop must be open
            and not getattr(loc, "has_security", lambda: False)()  # Optional: avoid secured locations
        ]
    
    def execute_gostealweapon(self, npc, region):
        print(f"\n[Action] {npc.name} attempting to GoStealWeapon in {region.name}...")

        weapon_objs = [
            p["origin"] for p in npc.percepts
            if "weapon" in p.get("tags", [])
        ]

        if not weapon_objs:
            print("[Action] No percepts with tag 'weapon' found. Action aborted.")
            return

        target_weapon = weapon_objs[0]  # Pick first for now
        print(f"[Target] Target weapon identified: {target_weapon.name} at {target_weapon.location.name}")

        if npc.location != target_weapon.location:
            print(f"[Move] {npc.name} is not at {target_weapon.location.name}. Moving now...")
            npc.move_to(target_weapon.location)
            return
        else:
            print(f"[Theft] {npc.name} has arrived at {target_weapon.location.name} and attempts to steal {target_weapon.name}.")
            theft = Theft(thief=npc, item=target_weapon)
            theft.execute()