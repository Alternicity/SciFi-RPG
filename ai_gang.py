#ai_gang.py
import time
from ai_utility import UtilityAI
from worldQueries import get_viable_robbery_targets
from characterActions import steal, rob, idle
from character_thought import Thought
from worldQueries import get_viable_robbery_targets
from motivation import Motivation
from summary_utils import summarize_percepts
from location import Shop, Vendor
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
                action = subordinate.ai.choose_action(region)
                if action:
                    subordinate.ai.execute_action(action, region)

    def execute_action(self, action, region):
        super().execute_action(action, region)

class GangMemberAI(UtilityAI):

    """ Here’s where “gang logic” lives.
Custom salience tuning, override functions in UtilityAI
Let UtilityAI produce options, and GangMemberAI choose from them based on gang-specific rules"""

    def choose_action(self, region):
        npc = self.npc

        # Motivation check — what's urgent?
        motivations = npc.motivation_manager.sorted_by_urgency()

        
        if npc.motivation_manager.has_motivation("rob"):
            if not npc.inventory.has_ranged_weapon():
                return self.resolve_obtain_weapon_target(region)

            if npc.location and npc.location.has_item("pistol"):
                return {"name": "steal", "params": {"item": "pistol"}}
            #Should this function just be altering the salience of things sent to UtilityAI now?
            if npc.inventory.has_ranged_weapon():
                return {"name": "rob", "params": {"target": npc.location or "shop"}}

        return {"name": "idle", "params": {}}

    def compute_salience(self, obj):
        base = super().compute_salience(obj)
        if isinstance(obj, Vendor) and "weapon" in obj.inventory.tags: #try both Vendor and Shop
            base += 5
        return base

    def execute_action(self, action, region):
        npc = self.npc #should this just be npc = self  ?

        

        #print(f"[THOUGHT] {npc.name} thinks about robbing a shop.")
                
        if action["name"] == "obtain_ranged_weapon":
            #deprecated I think in favour of passing a rob token to dispatcher in UtilityAI
            
            targets = get_viable_robbery_targets(region)
            if targets:
                target = targets[0]
                print(f"[AI] {npc.name} attempts robbery at {target.name}")
                rob(npc, target)
            else:
                print(f"[AI] {npc.name} found no robbery targets.")

        elif action == "Idle":
            idle(npc, region)

        if self.npc.is_test_npc:
            print(f"[MIND DUMP] from end of GangMemberAI execute_action {npc.name} current thoughts: {[str(t) for t in npc.mind]}")

    def think(self, region):
        self.npc.observe(region=region, location=self.npc.location)
        print(f"\n--- from GangMemberAI, {self.npc.name} is about to think ---")
        print("\n" * 1)

        """ print("\n[DEBUG] Inspecting self.npc before summarize_percepts:")
        print(f"Type: {type(self.npc)}")
        print(f"Attributes: {dir(self.npc)}")
        print(f"Name: {getattr(self.npc, 'name', 'N/A')}")
        print(f"Motivation Manager: {getattr(self.npc, 'motivation_manager', 'MISSING')}") """
        
        print(f"[Percepts Before Thinking] {self.npc.name}:\n{summarize_percepts(self.npc)}")

        print("\n" * 1)

        #self.npc.mind.thoughts.clear()
         #why clear thoughts here?

        for memory in self.npc.mind.semantic:
            if "weapon" in memory.tags or "weapons" in memory.description.lower():
                #this needs to detect the salience of shops for robbery

                #this needs to detect the semantic memory 
                #<MemoryEntry: event_type='observation', target='None', description='Shops usually have weapons', tags=['weapon', 'shop'

                thought = f"I could rob a shop because: {memory.description}" #and because of the salience of shop for robbery, and them having weapons available
                self.npc.mind.thoughts.append(thought)

        if not self.npc.mind.thoughts:

            idk_thought = Thought(
                content="I don't know what to do.",
                origin="GangMemberAI.think",
                urgency=1,
                tags=["confusion"]
            )

            self.npc.mind.thoughts.append(idk_thought)

        for memory in self.npc.mind.semantic:
            if "weapon" in memory.tags:
                score = 0.8  # temporary hardcoded salience
                self.npc.mind.thoughts.append(
                    Thought(
                        content=f"Scored memory: {memory.description}",
                        origin="semantic_memory",
                        urgency=int(score * 10),
                        tags=memory.tags,
                        source=memory
                    )
                )
        if self.npc.is_test_npc:
            print(f"[MIND DUMP] {self.npc.name} current thoughts: {[str(t) for t in self.npc.mind]}")
        print(f"[DEBUG] from def think in GangMemberAI {self.npc.name} thinking with {len(self.npc.memory.episodic)} episodic memories")

        # Use the shared logic
        self.promote_thoughts()
        #print(f"[DEBUG] From GangMemberAI def think {npc.name} current thoughts:")
        #npc not defined here, so commentedd out for now
        """ for thought in npc.mind:
            print(f" - {thought}") """

        """ print(f"{self.npc.name}'s thoughts after thinking:")
        for t in self.npc.mind:
            print(f" - {t}") """
        print(f"From GangMember Attention focus: {self.npc.attention_focus}")

    def custom_action_logic(self, region):
        npc = self.npc
        for percept in npc.percepts:
            tags = percept.get("tags", [])
            origin = percept.get("origin")

            print(f"[Percept] Found percept: {percept.get('description')} with tags: {tags}")

            if "weapon" in tags and any(m.type == "obtain_ranged_weapon" for m in npc.motivation_manager.get_motivations()):

                if not npc.has_weapon():
                    print(f"[Decision] {npc.name} decides to obtain a ranged weapon.")
                    return "obtain_ranged_weapon"

            if "shop" in tags and any(m.type == "rob" for m in npc.motivation_manager.get_motivations()):
                if npc.has_weapon():
                    print(f"[Decision] {npc.name} decides to Rob.")
                    return "Rob"

        return "Idle"

    def promote_thoughts(self):
        super().promote_thoughts()  # Get default generic promotions from UtilityAI

        npc = self.npc
        thoughts = npc.mind.thoughts

        for thought in list(thoughts):
            if not isinstance(thought, Thought):
                continue

            content_lower = thought.content.lower()

            if "rob" in content_lower and thought.urgency >= 5:
                motivation = Motivation("rob", urgency=thought.urgency, target=thought.source, source=thought)
                npc.motivation_manager.update_motivations(motivation.type, motivation.urgency, target=motivation.target, source=thought)
                print(f"[GANG] {npc.name} promotes robbery: {motivation}")

            elif "steal" in content_lower and thought.urgency >= 4:
                motivation = Motivation("steal", urgency=thought.urgency, target=thought.source, source=thought)
                npc.motivation_manager.update_motivations(motivation.type, motivation.urgency, target=motivation.target, source=thought)
                print(f"[GANG] {npc.name} promotes theft: {motivation}")

