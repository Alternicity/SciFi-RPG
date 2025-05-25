from ai_utility import UtilityAI

from ai_utility import UtilityAI
from worldQueries import get_viable_robbery_targets
import characterActions as actions


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
        npc = self.npc

        if action == "GoStealWeapon":
            weapons = [p["origin"] for p in npc.percepts if "weapon" in p.get("tags", [])]
            if weapons:
                weapon = weapons[0]
                print(f"[AI] {npc.name} trying to steal {weapon.name}")
                actions.steal(npc, weapon.location, target_item=weapon)

        elif action == "Rob":
            targets = get_viable_robbery_targets(region)
            if targets:
                target = targets[0]
                print(f"[AI] {npc.name} attempts robbery at {target.name}")
                actions.rob(npc, target)

        elif action == "Idle":
            print(f"[AI] {npc.name} is idling.")




