#ai_utility.py
from ai_base import BaseAI
from motivation import Motivation
from character_thought import Thought
from characterActions import rob, steal, visit_location, exit_location, idle
from time import time
from salience import compute_salience, compute_character_salience

class UtilityAI(BaseAI):
    def __init__(self, npc):
    #Core cognitive pipeline.
        self.npc = npc

    """ Filtering episodic memories and tagging/promoting important ones into thoughts.
        Salience/motivation scoring.
        Generating motivations from urgent thoughts.
        Managing the “thinking” lifecycle. """

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
        
        for memory in npc.mind.semantic:
                    if "weapon" in memory.tags and "shop" in memory.tags:
                        location = memory.source or "shop"
                        return {"name": "visit_location", "params": {"location": location}}

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
        
        action_map = { #this seems very specific, and criminal, perhaps deprecate or move to GangMemberAI?
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
        mind = npc.mind
        thoughts = mind.thoughts

        if not thoughts:
            print(f"[THINK] {npc.name} has no thoughts to promote.")
            npc.attention_focus = None
            return

        for thought in list(thoughts):
            if not isinstance(thought, Thought):
                print(f"[THINK] Skipping invalid thought in {npc.name}'s mind: {thought}")
                continue

            content_lower = thought.content.lower()

            if "obtain" in content_lower and "weapon" in thought.tags:
                motivation = Motivation("obtain_ranged_weapon", strength=thought.urgency, tags=["weapon"], source=thought)
                npc.motivation_manager.update_motivations(motivation.type, motivation.urgency, source=thought)
                print(f"[THINK] {npc.name} promoted to motivation: {motivation}")

            # Add more general-purpose thought promotions here as needed

        # Set attention focus to most urgent thought
        if thoughts:
            npc.attention_focus = max(thoughts, key=lambda t: t.urgency)
            print(f"[FOCUS] {npc.name}'s attention focused on: {npc.attention_focus}")
        else:
            npc.attention_focus = None

    def think(self, region):
        npc = self.npc
        self.npc.observe(region=region, location=self.npc.location)
        print(f"UtilitAI Percepts after  observe called from think(): {self.npc._percepts}")

        for obj in self.npc._percepts:
            salience = compute_salience(obj, self.npc)
            # sort, pick top N, update attention model etc.

        print(f"\n--- {self.npc.name} is thinking ---")

        if npc.percepts_updated:
            if self.npc.is_test_npc:
                print(f"[OBSERVE] B4 generate_thoughts_from_percepts {self.npc.name} perceived: {[v.get('description', v['type']) for v in self.npc._percepts.values()]}")
            self.generate_thoughts_from_percepts()
            npc.percepts_updated = False
            #new thoughts are only generated when percepts have changed — decoupling perception and cognition

        print(f"UtilitAI Percepts after generate_thoughts_from_percepts: {self.npc._percepts}")

        print(f"[DEBUG] from UtilityAI think() {self.npc.name} thinking with {len(self.npc.memory.episodic)} episodic memories")

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
                    #@attention_focus.setter

        return "Idle"
    
    def generate_thoughts_from_percepts(self):
        npc = self.npc  # shortcut

        for key, value in npc.percepts.items():
            salience = value.get("salience", 1)  # default to 1 if missing
            description = value.get("description", str(value.get("origin")))
            origin = value.get("origin", None)
            tags = value.get("tags", [])
            urgency = value.get("urgency", salience)

            # Avoid duplicate thoughts
            existing = [t.content for t in npc.mind]
            if description not in existing:
                thought = Thought(
                    content=description,
                    urgency=urgency,
                    source=origin,
                    tags=tags
                )
        npc.mind.add_thought(thought)
        print(f"[THOUGHT GEN] {npc.name} adds thought: {thought}")

    def resolve_obtain_weapon_target(self, region):
        # Return a location from percepts or memory
        npc = self.npc  # Access from self


        # # Step 1: Check immediate percepts
        weapons = [p["origin"] for p in npc.percepts if "weapon" in p.get("tags", [])]
        if weapons:
            weapon = weapons[0]
            print(f"[AI] {npc.name} trying to steal {weapon.name}")
            steal(npc, weapon.location, target_item=weapon)

            return {"name": "steal", "params": {"item": weapon.name}}

        known_weapon_locations = [
    m for m in npc.memory.semantic
    if "weapon" in getattr(m, "tags", []) and "shop" in getattr(m, "tags", [])
]

        print(f"[DEBUG] {npc.name} has memory: {[m.tags for m in npc.memory.semantic]}")
        print(f"[DEBUG] Known weapon locations: {known_weapon_locations}")

        if known_weapon_locations:
            memory = known_weapon_locations[0]
            location = npc.memory.semantic or "shop"
            print(f"[AI] {npc.name} remembers a shop with weapons: {location}")
            return {"name": "visit_location", "params": {"location": location}}


        # Step 3: No weapons visible or remembered, add a thought and let AI re-evaluate later
        #Shouldnt this thought form IF the character remembers that shops have weapons
        new_thought = Thought(
            content="Maybe I should rob a shop to get a weapon.",
            origin="General knowledge?",
            urgency=7,
            tags=["rob", "shop", "weapon"],
            timestamp=time.time(),
            source="Instinct",
            weight=7
        )
        npc.mind.add(new_thought)
        npc.motivation_manager.increase("rob", 1.0)
        print(f"[THOUGHT] {npc.name} had a new thought: {new_thought.content}")

        return {"name": "idle", "params": {}}

    def evaluate_thoughts(self):
        """
        Loop through unresolved thoughts and increase motivations accordingly.
        """
        for thought in self.npc.mind.thoughts:
            if thought.resolved:
                continue

            # You can adjust these based on your thought/tag system
            if "rob" in thought.tags and "weapon" in thought.tags:
                print(f"[THOUGHT EVAL] {self.npc.name} is influenced by thought: {thought.content}")
                self.npc.motivation_manager.increase("rob", thought.weight)
                thought.resolved = True  # Only apply once for now