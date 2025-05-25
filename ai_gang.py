import time

from ai_utility import UtilityAI
from worldQueries import get_viable_robbery_targets
import characterActions as actions
from ai_utility import Thought

class GangCaptainAI(UtilityAI):
    def choose_action(self, region):
        # Step 1: Check if subordinates are idle, need tasks
        if self.should_assign_tasks():
            print(f"[CaptainAI] {self.npc.name} decides to assign tasks.")
            self.assign_tasks(region)

        # Step 2: Perform own utility action like a Member
        return super().choose_action(region)

    def should_assign_tasks(self):
        # Very simple rule: assign tasks if at least one subordinate is idle
        return any(not s.current_task for s in self.npc.subordinates)

    def assign_tasks(self, region):
        for subordinate in self.npc.subordinates:
            if not subordinate.current_task:
                print(f"[CaptainAI] Assigning task to {subordinate.name}")
                subordinate.ai.choose_action(region)  # Let them act

    def execute_action(self, action, region):
        # Same as GangMemberAI for now
        super().execute_action(action, region)

class GangMemberAI(UtilityAI):
    def execute_action(self, action, region):
        npc = self
        #self.npc before

        if action == "obtain_ranged_weapon":
            weapons = [p["origin"] for p in npc.percepts if "weapon" in p.get("tags", [])]
            if weapons:
                weapon = weapons[0]
                print(f"[AI] {npc.name} trying to steal {weapon.name}")
                actions.steal(npc, weapon.location, target_item=weapon)

            else:
                # Search memory for semantic knowledge about weapon locations
                known_weapon_locations = [
                    m for m in npc.memory
                    if "weapons" in m.tags and "shop" in m.details.lower()
                ]
                if known_weapon_locations:
                    print(f"[MEMORY] {npc.name} remembers that weapons are available in shops.")
                    npc.thoughts.append(Thought(
                        content="Maybe I should rob a shop to get a weapon.",
                        urgency=7,
                        timestamp=time.time()
                    ))
                    print(f"[THOUGHT] {npc.name} thinks about robbing a shop.")
                    # Optional: Add a "visit" or "plan" system here later
                else:
                    print(f"[AI] {npc.name} doesn't know where to find a weapon. Idling.")

        elif action == "Rob":
            targets = get_viable_robbery_targets(region)
            if targets:
                target = targets[0]
                print(f"[AI] {npc.name} attempts robbery at {target.name}")
                actions.rob(npc, target)
            else:
                print(f"[AI] {npc.name} found no robbery targets.")

        elif action == "Idle":
            print(f"[AI] {npc.name} is idling.")

    def custom_action_logic(self, region):
        npc = self.npc
        for percept in npc.percepts:
            tags = percept.get("tags", [])
            origin = percept.get("origin")

            print(f"[Percept] Found percept: {percept.get('description')} with tags: {tags}")

            if "weapon" in tags and any(m.type == "obtain_ranged_weapon" for m in npc.motivations):
                if not npc.has_weapon():
                    print(f"[Decision] {npc.name} decides to obtain a ranged weapon.")
                    return "obtain_ranged_weapon"

            if "shop" in tags and any(m.type == "rob" for m in npc.motivations):
                if npc.has_weapon():
                    print(f"[Decision] {npc.name} decides to Rob.")
                    return "Rob"

        return "Idle"


