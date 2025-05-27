import time
from ai_utility import UtilityAI
from worldQueries import get_viable_robbery_targets
from characterActions import steal, rob
from character_thought import Thought
from worldQueries import get_viable_robbery_targets
from motivation import Motivation

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

    def choose_action(self, region):
        npc = self.npc

        # Motivation check — what's urgent?
        motivations = npc.mind.motivations.sorted_by_urgency()

        # Step 1: Do we want to rob?
        if npc.has_motivation("rob"):
            # Step 2: Do we have a high-salience weapon?
            if not npc.has_ranged_weapon():
                # Step 3: Can we remember where to get one?
                for memory in npc.mind.semantic:
                    if "weapon" in memory.tags and "shop" in memory.tags:
                        location = memory.source or "shop"
                        return {"name": "visit_location", "params": {"location": location}}

            # Step 4: If we’re already at the right shop with a pistol
            if npc.location and npc.location.has_item("pistol"):
                return {"name": "steal", "params": {"item": "pistol"}}

            if npc.has_ranged_weapon():
                return {"name": "rob", "params": {"target": npc.location or "shop"}}

        # If we’re not sure what to do — idle
        return {"name": "idle", "params": {}}

    def execute_action(self, action, region):
        npc = self.npc #should this just be npc = self  ?

        if action == "obtain_ranged_weapon":
            weapons = [p["origin"] for p in npc.percepts if "weapon" in p.get("tags", [])]
            if weapons:
                weapon = weapons[0]
                print(f"[AI] {npc.name} trying to steal {weapon.name}")
                steal(npc, weapon.location, target_item=weapon)
            else:
                # Search memory for weapon info
                known_weapon_locations = [
                    m for m in npc.memory
                    if "weapon" in getattr(m, "tags", []) and "shop" in getattr(m, "tags", [])
                ]
                print(f"[DEBUG] From GangMemberAI, def execute_action before if known_weapon_locations condition {npc.name} memory: {[m.tags for m in npc.memory]}")

                print(f"[DEBUG] {npc.name} has memory: {[m.tags for m in npc.memory]}")
                print(f"[DEBUG] BEFORE if known_weapon_locations: {known_weapon_locations}")

                if known_weapon_locations:
                    print(f"[MEMORY] {npc.name} remembers shops with weapons.")
                    print(f"[DEBUG] AFTER if known_weapon_locations: {known_weapon_locations}")

                    new_thought = (Thought(
                        content="Maybe I should rob a shop to get a weapon.",
                        origin="General knowledge?",
                        urgency=7,
                        tags=["rob", "shop", "weapon"],
                        timestamp=time.time(),
                        source="Other Characters",
                        weight=7
                    ))
                    npc.mind.add(new_thought)

                # TEMP: Convert memory entries to thoughts(debug_gang_npc)
                    """ print(f"\n[DEBUG] Generating thoughts from memory for {npc.name}...")
                    for mem in npc.memory.episodic + npc.memory.semantic:
                        thought = f"Recall: {mem.details} (tags: {', '.join(mem.tags)})"
                        npc.mind.add(thought)# ⚠️ this is a plain string, wrap these strings into Thought(content=...)
                        print(f" - Generated thought: {thought}") """

                    print(f"[ADD THOUGHT] {npc.name} has new thought: {new_thought}")

                    #print(f"[THOUGHT] {npc.name} thinks about robbing a shop.")
                else:
                    print(f"[AI] {npc.name} doesn't know where to find a weapon. Idling.")

        elif action == "Rob": #deprecated I think in favour of passing a rob token to dispatcher in UtilityAI
            targets = get_viable_robbery_targets(region)
            if targets:
                target = targets[0]
                print(f"[AI] {npc.name} attempts robbery at {target.name}")
                rob(npc, target)
            else:
                print(f"[AI] {npc.name} found no robbery targets.")

        elif action == "Idle":
            print(f"[AI] {npc.name} is idling.")

        print(f"[MIND DUMP] from end of GangMemberAI execute_action {npc.name} current thoughts: {[str(t) for t in npc.mind]}")

    def think(self, region): #should this be renamed GangMemberThink for clarity?
        print(f"\n--- from GangMemberAI, {self.npc.name} is about to think ---")
        print(f"GangMember think> Percepts before thinking: {self.npc._percepts}")

        self.npc.mind.thoughts.clear()

        for memory in self.npc.mind.semantic:
            if "weapon" in memory.tags or "weapons" in memory.description.lower():
                thought = f"I could rob a shop because: {memory.description}"
                self.npc.mind.thoughts.append(thought)

        if not self.npc.mind.thoughts:
            self.npc.mind.thoughts.append(
                Thought(content="I don't know what to do.", urgency=1, tags=["confusion"])
    )

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

        print(f"[MIND DUMP] {self.npc.name} current thoughts: {[str(t) for t in self.npc.mind]}")
        print(f"[DEBUG] from def think in GangMemberAI {self.npc.name} thinking with {len(self.npc.memory.episodic)} episodic memories")

        # Use the shared logic
        self.promote_thoughts()
        #print(f"[DEBUG] From GangMemberAI def think {npc.name} current thoughts:")
        #npc not defined here, so commentedd out for now
        """ for thought in npc.mind:
            print(f" - {thought}") """

        print(f"{self.npc.name}'s thoughts after thinking:")
        for t in self.npc.mind:
            print(f" - {t}")
        print(f"From GangMember Attention focus: {self.npc.attention_focus}")

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

    def promote_thoughts(self):
        npc = self.npc
        for thought in list(npc.mind.thoughts):
            if isinstance(thought, Thought):
                if "rob" in thought.content and thought.urgency >= 5:
                    m = Motivation("rob", urgency=thought.urgency, target=thought.source, source=thought)
                    npc.motivation_manager.update_motivations(m.type, m.urgency, target=m.target, source=m.source)
                    print(f"[GANG-AI] {npc.name} promotes robbery: {m}")
            else:
                print(f"[GANG-AI] Skipping invalid thought: {thought}")

