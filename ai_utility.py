#ai_utility.py
from ai_base import BaseAI
from motivation import Motivation
from character_thought import Thought
from npc_actions import rob_auto, steal_auto, visit_location_auto, idle_auto
from character_memory import Memory
from time import time
from salience import compute_salience, compute_character_salience
from collections import defaultdict
from worldQueries import get_region_knowledge

class UtilityAI(BaseAI):
    def __init__(self, npc):
    #Core cognitive pipeline.
        self.npc = npc

    """ Filtering episodic memories and tagging/promoting important ones into thoughts.
        Generating motivations from urgent thoughts.
        Managing the “thinking” lifecycle. """

    def compute_salience_for_motivation(self, percept_data, motivation):
        tags = percept_data.get("tags", [])
        
        if motivation == "rob":
            if "ranged_weapon" in tags or "weapon" in tags:
                return 10
            elif "shop" in tags:
                return 7
        elif motivation == "steal":
            if "weapon" in tags:
                return 9
        elif motivation == "earn_money":
            if "cash" in tags:
                return 6
            if "trade" in tags:
                return 5
        # fallback salience
        return 1

    def choose_action(self, region):
        npc = self.npc

        #prevent herding
        if not getattr(npc, "isTestNPC", False):
            return {"name": "idle"}

        motivations = npc.motivation_manager.get_motivations()
        if not motivations:
            return {"name": "idle"}

        percepts = list(npc.get_percepts())
        #percepts here is not accessed

        memories = []
        for memory_list in npc.mind.memory.semantic.values():
            memories.extend(memory_list)


        actions = []

        for m in motivations:
            m_type = m.type

            # Visit shops known to have weapons
            for memory in memories:
                if "weapon" in memory.tags and "shop" in memory.tags:
                    location = memory.source
                    if location and location != npc.location:
                        actions.append({
                            "name": "visit_location",
                            "params": {"location": location},
                            "motivation": m_type
                        })

            # Steal item in current location
            if npc.location:
                for item in npc.location.objects_present:
                    if "weapon" in item.tags:
                        actions.append({
                            "name": "steal",
                            "params": {"location": npc.location, "target_item": item},
                            "motivation": m_type
                        })

            # Rob the location if it's a shop or high value
            if npc.location and "shop" in npc.location.tags:
                actions.append({
                    "name": "rob",
                    "params": {"location": npc.location},
                    "motivation": m_type
                })

            # Leave scene of crime or after acquiring item
            from inventory import Inventory
            #print(f"DEBUG: npc.inventory type is {type(npc.inventory)}")
            if not isinstance(npc.inventory, Inventory):
                raise TypeError(f"npc.inventory is {type(npc.inventory)}, expected Inventory")
            if npc.inventory.has_illegal_items():
                actions.append({
                    "name": "exit_location",
                    "params": {},
                    "motivation": "escape"
                })

        # Basic needs fallback
        if npc.hunger > 7:
            actions.append({
                "name": "eat",
                "params": {},
                "motivation": "satisfy_hunger"
            })

        if not actions:
            return {"name": "idle"}

        # Score and choose
        scored = [(self.score_action(a), a) for a in actions]
        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_action = scored[0]
        print(f"[UtilityAI] {npc.name} chose {best_action['name']} with score {best_score}")
        return best_action

    
    def execute_action(self, action, region):
        """
        Dispatch NPC actions to npc_actions.py functions.
        """
        npc = self.npc

        if not isinstance(action, dict):
            print(f"[ERROR] Action must be a dict, got: {action}")
            return

        action_name = action.get("name")
        params = action.get("params", {})

        # Action routing for NPCs (clean, lowercase names)
        from npc_actions import (
            visit_location_auto,
            steal_auto,
            rob_auto,
            exit_location_auto,
            eat_auto,
            idle_auto
        )

        action_map = {
            "visit_location": visit_location_auto,
            "steal": steal_auto,
            "rob": rob_auto,
            "exit_location": exit_location_auto,
            "eat": eat_auto,
            "idle": idle_auto
        }

        action_func = action_map.get(action_name.lower())

        if action_func:
            try:
                action_func(npc, **params)
            except Exception as e:
                print(f"[ERROR] Executing action {action_name}: {e}")
        else:
            print(f"[UtilityAI] {npc.name} has no valid action to execute ({action_name}).")

    def score_action(self, action: dict, context: dict = None) -> int:
        #can be replaced by a registry-based design or use decorators to register scorers by action['name']
        context = context or {}
        npc = self.npc
        score = 0

        name = action.get("name")
        motivation = action.get("motivation", "")
        location = action.get("params", {}).get("location")
        target_item = action.get("params", {}).get("target_item")

        # Base motivations
        if name == "visit_location":
            if location and location != npc.location:
                score = 5
                if motivation == "obtain_weapon":
                    score += 5

        elif name == "steal":
            score = 10
            if "weapon" in target_item.tags:
                score += 5
            if hasattr(target_item, "salience"):
                score += int(target_item.salience)

        elif name == "rob":
            score = 7
            if location and getattr(location, "value", 0) > 50:
                score += 3
            if hasattr(location, "salience"):
                score += int(location.salience)

        elif name == "exit_location" and npc.location and npc.location.name in ["Shop", "Heist Site"]:
            score = 6

        elif name == "eat":
            score = 8 if npc.hunger > 7 else 2
            
        urgency = npc.motivation_manager.get_urgency(motivation)
        return score * urgency #REVIST.

    def promote_thoughts(self):
        npc = self.npc
        mind = npc.mind
        thoughts = mind.thoughts

        if not thoughts:
            npc.attention_focus = None
            #print here, saying why not attention focus?
            return

        for thought in self.npc.mind.thoughts:
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
            #print(f"[FOCUS] {npc.name}'s attention focused on: {npc.attention_focus.summary()}")
            #for mmore info uncomment the following line
            #print(f"[FOCUS] {npc.name}'s attention focused on: {npc.attention_focus.summary(include_source=True, include_time=True)}")
        else:
            npc.attention_focus = None

    def examine_episodic_memory(self, episodic_memories):
        event_counts = defaultdict(int)
        for m in episodic_memories:
            key = (m.subject, m.object_, m.verb, m.event_type)
            event_counts[key] += 1
            if event_counts[key] >= 3:
                print(f"[Insight]: {m.subject} has done {m.verb} {event_counts[key]} times.")
                # You could generate a new belief, goal, or trait here

    def deduplicate_thoughts_by_type(thoughts):
        #call it: After thoughts are generated from percepts, before promotions happen

        seen = {}
        for t in thoughts:
            if t.type not in seen or t.urgency > seen[t.type].urgency:
                seen[t.type] = t
        return list(seen.values())

    

    def think(self, region):
        from location import Region
        #tmp if/print block for debug
        if not isinstance(region, Region):
            print(f"[DEBUG] {self.npc.name} UtilityAI def think calling observe with region={region}, location={self.npc.location}")
            print(f"[UtilityAI] Bad region: {region} ({type(region).__name__}) for {self.npc.name}")

        #observe calls have moved to the game loop tick  
        #self.npc.observe(region=region, location=self.npc.location)

        region_knowledge = get_region_knowledge(self.npc.mind.memory.semantic, region.name)
        if region_knowledge:
            turf_status = self.evaluate_turf_war_status(self.npc, region_knowledge)  # Base awareness
        self.promote_thoughts()

        motivations = self.npc.motivation_manager.get_urgent_motivations()
        if not motivations:
            #print(f"[THINK] {self.npc.name} has no urgent motivations.")
            return
        
        # Examine episodic memory for repeated events
        episodic_memories = self.npc.mind.memory.get_episodic()
        self.examine_episodic_memory(episodic_memories)
        #logic to do something with them

        percepts = list(self.npc.get_percepts().values()) #get_percepts.values? Re check this
        candidate_thoughts = []
        for motivation in motivations:
            for percept in percepts:
                if self.matches_motivation(percept, motivation):
                    salience = self.compute_salience_for_percepts(percept, motivation)

                    #Should line below use mind.add_thought(self, thought: Thought):
                    thought = Thought(
                        content = str(percept["description"] if "description" in percept else percept["origin"]),
                        urgency=salience,
                        source=str(percept["description"],
                        tags=percept[("tags", [])],
                    ))
                    self.npc.mind.add_thought(thought)
                    #added
                    thoughts = self.npc.mind.get_all()
                    self.deduplicate_thoughts_by_type(thoughts)
        

        self.promote_thoughts()


        self.compute_salience_for_percepts() # pass motivations here? Also characters percepts, then return salient percepts
        #also this function does not yet exist.

        #You can skip generate_thoughts_from_percepts() entirely unless you need to run an extra pass on percepts 
        # not handled via motivations. I will, there will be other factors like eventually tasks.
        self.generate_thoughts_from_percepts()#can we then just add the salient percepts to the parameters here?

        self.promote_thoughts()
        #flow needs to pass to score_action, then choose_action then execute_action

    def evaluate_turf_war_status(self, region_knowledge):
        # Basic version — maybe no-op or minimal response
        return None
    
    def generate_thoughts_from_percepts(self):
        npc = self.npc  # shortcut

        for key, value in npc.percepts.items():
            salience = value.get("salience", 1)  # default to 1 if missing
            description = value.get("description", str(value.get("origin")))
            origin = value.get("origin", None)
            tags = value.get("tags", [])
            urgency = value.get("urgency", salience)

            # Avoid duplicate thoughts
            existing = [t.content for t in npc.mind.thoughts]
            if description not in existing:
                thought = Thought(
                    content=description,
                    urgency=urgency,
                    source=origin,
                    tags=tags
                )
                npc.mind.add_thought(thought)
                print(f"[THOUGHT GEN] {npc.name} adds thought: {thought}")

    def compute_salience_for_percepts(self, percept, motivation):
        score = 1
        if "tags" in percept and motivation.type in percept["tags"]:
        #alt version
        #if motivation.type in percept.get("tags", []):
            score += 10
        if str(["location"]) == self.npc.location.name:

            score += 5
        score *= motivation.urgency
        return score
    
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

    def evaluate_memory_for_threats(self, memory):
        npc = self.npc
        # Check if any enemy gangs are in the memory
        if hasattr(memory, "tags") and "region" in memory.tags:
            region_gangs = getattr(memory, "region_gangs", [])
            for gang in region_gangs:
                if gang != npc.faction and gang in npc.faction.enemies:
                    thought = Thought(
                        content=f"{gang} controls this region. They are enemies!",
                        origin=memory.name,
                        urgency=8,
                        tags=["enemy", "threat", "gang", "region"],
                        timestamp=time.time(),
                        source="SemanticMemory",
                        weight=7
                    )
                    npc.mind.add(thought)
                    npc.is_alert = True
                    print(f"[THREAT] {npc.name} became alert due to memory: {memory.name}")

    def evaluate_thought_for_threats(self, thought):
        npc = self.npc

        if "hostile" in thought.tags and "gang" in thought.tags:
            inferred = Thought(
                content=f"{npc.name} infers immediate danger from enemy gangs.",
                origin=thought.origin,
                urgency=7,
                tags=["alert", "retreat", "priority"],
                source="UtilityAI.Inference",
                timestamp=time.time(),
                weight=8
            )
            npc.mind.add(inferred)
            npc.is_alert = True
            #print(f"[INFERENCE] {npc.name} escalated alertness based on: {thought.content}")

    def faction_observation_logic(npc, region, content, subject, origin, urgency, source, weight, timestamp, resolved, corollary ): #A general function to handle faction characers observation of other factions

#not sure if this func will be called automatically to appraise rival factions, or on a triggered in code when a rival 
# faction does something. Maybe both? Thought can be update or have corollories?
#a generalized version of def gang_observation_logic

        appraise_rival = Thought(
            content="So, they are xyz",
            subject=subject,
            origin=region.name,
            urgency=urgency or 10,
            tags=["compete", "danger", "faction"],
            source="Observation",
            weight = weight or 10, # How impactful (can be salience or derived)
            timestamp=time.time(),
            resolved= resolved,
            corollary = corollary or []
        )
        npc.mind.add(appraise_rival)
        if hasattr(npc, 'utility_ai'):
            npc.utility_ai.evaluate_thought_for_threats(appraise_rival)