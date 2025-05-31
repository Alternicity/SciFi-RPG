#ai_utility.py
from ai_base import BaseAI
from motivation import Motivation
from character_thought import Thought
from characterActions import rob, steal, visit_location, exit_location, idle

class UtilityAI(BaseAI):
    def choose_action(self, region):
        npc = self.npc
        if region is None:
            #print(f"\n[UtilityAI] No region given for {self.npc.name}")
            return {"name": "Idle"}
        
        #verbose
        #print(f"\n[UtilityAI] Evaluating actions for {self.npc.name} in {region.name}...")

        if not npc.motivation_manager.get_motivations():
            print(f"[Decision] {npc.name} has no strong motivations. Idling.")
            return {"name": "Idle"}

        return None # Placeholder
    
    def execute_action(self, action, region):
        """
        Dispatch action to the correct function in characterActions.py
        """
        npc = self.npc

        if not isinstance(action, dict):
            print(f"[ERROR] Action must be a dict, got: {action}")
            return

        action_name = action.get("name")
        params = action.get("params", {})
        
        action_map = {
            "Rob": rob,
            "Steal": steal,
            "Visit": visit_location,
            "Idle": idle,
        }

        action_func = action_map.get(action_name)

        if action_func:
            action_func(npc, region, **params)
        else:
            print(f"[UtilityAI] {npc.name} has no valid action to execute ({action_name}).")

    #requires a list of propsed actions to work?
    def score_action(self, action_type, context):
        if action_type == "expand_territory":
            return 10 if context["rival_presence"] > 5 else 3
        elif action_type == "recruit":
            return 8 if context["faction_strength"] < 50 else 2
        return 1

    def promote_thoughts(self):
        npc = self.npc
        urgent_thoughts = [t for t in npc.mind if t.urgency >= 5]

        for thought in urgent_thoughts:
            if "rob" in thought.content.lower():
                motivation = Motivation("rob", strength=thought.urgency, tags=["crime", "money"])

                npc.motivation_manager.update_motivations(motivation.type, motivation.urgency, source=thought)

                #npc.mind.remove(thought)
                print(f"[THINK] {npc.name} promoted to motivation: {motivation}")

            elif "obtain" in thought.content.lower() and "weapon" in thought.tags:
                motivation = Motivation("obtain_ranged_weapon", strength=thought.urgency, tags=["weapon"])
                npc.motivation_manager.update_motivations(motivation.type, motivation.urgency, source=thought)

                #npc.mind.remove(thought)
                print(f"[THINK] {npc.name} promoted to motivation: {motivation}")

        # Set attention focus to most urgent remaining thought, does this code need to be indented further?
        if npc.mind:
            npc.attention_focus = max(npc.mind, key=lambda t: t.urgency)
            print(f"[FOCUS] {npc.name}'s attention focused on: {npc.attention_focus}")
        else:
            npc.attention_focus = None

    def think(self, region):
        npc = self.npc
        self.npc.observe(region=region, location=self.npc.location)
        print(f"UtilitAI Percepts after  observe called from think(): {self._percepts}")
        print(f"\n--- {self.name} is thinking ---")

        if npc.percepts_updated:
            if self.npc.is_test_npc:
                print(f"[OBSERVE] B4 generate_thoughts_from_percepts {self.npc.name} perceived: {[v.get('description', v['type']) for v in self.npc._percepts.values()]}")
            self.generate_thoughts_from_percepts()
            npc.percepts_updated = False
            #new thoughts are only generated when percepts have changed — decoupling perception and cognition

        print(f"UtilitAI Percepts after generate_thoughts_from_percepts: {self._percepts}")

        print(f"[DEBUG] from UtilityAI think() {self.owner.name} thinking with {len(self.owner.memory.episodic)} episodic memories")

        # Promote urgent thoughts to motivations
        for thought in list(npc.mind):
            if thought.urgency >= 5:
                if "rob" in thought.content:
                    m = Motivation("rob", strength=thought.urgency, tags=["money", "weapon"]) #weapon seems a bit GangMember specific, posibly legacy here
                    npc.motivation_manager.update_motivations(m.type, m.urgency)

                    print(f"[THINK] {npc.name} promotes thought to motivation: {m}")
                    #npc.mind.remove(thought)

                # Optionally update attention focus to most urgent thought
                if npc.mind:
                    npc.attention_focus = max(npc.mind, key=lambda t: t.urgency)
                else:
                    npc.attention_focus = None

        return "Idle"
    
    def generate_thoughts_from_percepts(self):
        npc = self.npc  # shortcut

        for key, value in npc.percepts.items():
            data = value["data"]
            salience = value["salience"]

            # Avoid duplicate thoughts (optional but good)
            existing = [t.content for t in npc.mind]
            if data["description"] not in existing:
                thought = Thought(
                    content=data["description"],
                    urgency=salience,
                    source=data["origin"]
                )
                npc.mind.add(thought)
                print(f"[THOUGHT GEN] {npc.name} adds thought: {thought}")