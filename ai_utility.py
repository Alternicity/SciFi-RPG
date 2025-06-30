#ai_utility.py
import random
from dataclasses import dataclass, field
from typing import Literal, List, Optional
from ai_base import BaseAI
from motivation import Motivation
from character_thought import Thought
from npc_actions import rob_auto, steal_auto, visit_location_auto, idle_auto
from character_memory import Memory
from time import time
from salience import compute_salience, compute_character_salience, compute_salience_for_percept_with_anchor
from anchor_utils import Anchor, create_anchor_from_motivation, create_anchor_from_thought, create_anchor_from_motivation
from collections import defaultdict
from worldQueries import get_region_knowledge
from memory_entry import MemoryEntry



class UtilityAI(BaseAI):
    def __init__(self, npc):
    #Core cognitive pipeline.
        self.npc = npc

    """ Filtering episodic memories and tagging/promoting important ones into thoughts.
        Generating motivations from urgent thoughts.
        Managing the “thinking” lifecycle. """

    def choose_action(self, region):
        npc = self.npc

        #prevent herding
        if not getattr(npc, "isTestNPC", False):
            return {"name": "idle"}

        anchors = [create_anchor_from_motivation(m) for m in npc.motivation_manager.get_motivations()]
        if not motivations:#motivations is not defined here
            return {"name": "idle"}

        percepts = list(npc.get_percepts())
        #percepts here is not accessed

        memories = []
        for memory_list in npc.mind.memory.semantic.values():#this is direct acces, not via a getter
            memories.extend(memory_list)

        actions = []

        for anchor in anchors:
            anchor_type = anchor.type

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
        motivation = action.get("motivation", anchor.name if anchor else "")
        if "motivation" in action and "anchor" not in action:
            print(f"[LEGACY] Action is using legacy motivation string: '{motivation}'")

        location = action.get("params", {}).get("location")
        target_item = action.get("params", {}).get("target_item")

        # Base motivations
        if name == "visit_location":
            if location and location != npc.location:
                score = 5
                if motivation == "obtain_weapon":#motivation is needed here
                    score += 5

        elif name == "exit_location" and npc.location and npc.location.name in ["Shop", "Heist Site"]:
            score = 6

        elif name == "eat":
            score = 8 if npc.hunger > 7 else 2
        from ai_utility_thought_tools import extract_anchor_from_action
        anchor = extract_anchor_from_action(action)#line 141 extract_anchor_from_action is marked not defined
        urgency = anchor.weight if anchor else 1.0
        return score * urgency

    def create_anchor_from_thought(self, thought: Thought, name: str, type_: str = "motivation") -> Anchor:
        return Anchor(name=name, type=type_, weight=thought.urgency, source=thought, tags=thought.tags)

    """ Best sequence:
1. Anchor from Thought
2. Add Anchor to Episodic Memory
3. Add (or reinforce) Thought in mind
4. Promote to Semantic later (based on usage) """

    def promote_thoughts(self):
        npc = self.npc
        mind = npc.mind
        thoughts = mind.thoughts
        anchor = None

        if not thoughts:
            npc.attention_focus = None
            print(f"[FOCUS] {npc.name} has no thoughts to process.")
            return

        for thought in thoughts:
            if not isinstance(thought, Thought):
                print(f"[THINK] Skipping invalid thought in {npc.name}'s mind: {thought}")
                continue

            content_lower = thought.content.lower()

            # Example general trigger
            if "obtain" in content_lower and "weapon" in thought.tags:
                anchor = self.create_anchor_from_thought(thought, "obtain_ranged_weapon", type="motivation", weight=thought.urgency)
                
        if anchor and not npc.default_focus:
            npc.default_focus = anchor  # Could also be the thought or memory_entry

            #anchor = Anchor(name="obtain_ranged_weapon", type="motivation", weight=thought.urgency)
            npc.motivation_manager.update_motivations(anchor.name, urgency=anchor.weight, source=thought)
            print(f"[THINK] {npc.name} promoted to motivation: {anchor}")

            memory_entry = MemoryEntry(
                subject=npc.name,
                object_="anchor",
                verb="generated",
                details=f"Anchor {anchor.name} was created from thought '{thought.content}'",
                tags=["anchor", "thought"],
                target=anchor,
                importance=thought.urgency,
                type="anchor_creation",
                initial_memory_type="episodic"
            )
            npc.mind.memory.add_episodic(memory_entry)
            #anchors are important, promte to semantic here
            #Later logic could be time passed, number of times reinforced, used successfully in decision-making

    

        # Set attention focus
        npc.attention_focus = max(thoughts, key=lambda t: t.urgency)
        #set npc.default_focus here as well

        if self.npc.is_test_npc:
            print(f"[FOCUS] {npc.name}'s attention focused on: {npc.attention_focus.summary(include_source=True, include_time=True)}")


    def examine_episodic_memory(self, episodic_memories):
        event_counts = defaultdict(int)
        for m in episodic_memories:
            key = (m.subject, m.object_, m.verb, m.event_type)
            event_counts[key] += 1
            if event_counts[key] >= 3:
                print(f"[Insight]: {m.subject} has done {m.verb} {event_counts[key]} times.")
                # I could generate a Anchor, new belief, goal, or trait here, and return it

    def deduplicate_thoughts_by_type(thoughts):
        #call it: After thoughts are generated from percepts, before promotions happen

        seen = {}
        for t in thoughts:
            if t.type not in seen or t.urgency > seen[t.type].urgency:
                seen[t.type] = t
        return list(seen.values())

    def matches_motivation(self, percept: dict, motivation) -> bool:
        """
        Returns True if the percept is relevant to the given motivation.
        """
        if not isinstance(percept, dict):
            print(f"[BUG] Expected percept to be dict, got {type(percept)}: {percept}")
            return False
        
        percept_tags = percept.get("tags", [])
        m_type = getattr(motivation, "type", str(motivation)).lower()  # Handle both Motivation objects and strings

        # Example logic: match if motivation type appears in tags or matches known aliases
        if m_type in percept_tags:
            return True

        known_matches = {
            "rob": ["shop", "cash", "loot"],
            "steal": ["valuable", "item", "weapon"],
            "obtain_ranged_weapon": ["weapon", "gun", "ranged"],
            "violence": ["blood", "enemy", "gunshot"]
        }

        if m_type in known_matches:
            for tag in known_matches[m_type]:
                if tag in percept_tags:
                    return True

        """ You might later improve it with:
        Salience thresholds.
        Anchors (e.g., matches_anchor(percept, anchor)).
        NPC role sensitivity (e.g., cops prioritize violence tags, merchants focus on trade).
        """
        return False


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

        percepts = list(self.npc.get_percepts()) #get_percepts.values? Re check this

        for i, percept in enumerate(percepts):
            print(f"[DEBUG] From UtilityAI, think() Percept[{i}]: {type(percept)} {percept}")

        candidate_thoughts = [] #not accesssed
        for motivation in motivations:
            anchor = create_anchor_from_motivation(motivation)#both these lines?
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
        
        score = compute_salience_for_percept_with_anchor(percept, anchor) #anchor now defined, but score not accessed
       
        self.generate_thoughts_from_percepts()#can we then just add the salient percepts to the parameters here?
        self.promote_thoughts()
        #flow needs to pass to score_action, then choose_action then execute_action

        print(f"[DEBUG] From UtilityAI, def think()")
        print(f"[DEBUG] {self.npc.name} in {self.npc.location.name}")
        print(f"[DEBUG] Percepts: {[p['data'].get('description') for p in percepts]}")
        print(f"[DEBUG] Thoughts: {[str(t) for t in self.npc.mind.thoughts]}")

        
    def evaluate_turf_war_status(self, region_knowledge):
        # Basic version — maybe no-op or minimal response
        return None
    
    

    def generate_thoughts_from_percepts(self):
        npc = self.npc
        percepts = list(npc._percepts.values())  # direct access, safe in this context

        motivations = npc.motivation_manager.get_urgent_motivations()
        if not motivations:
            return

        for motivation in motivations:
            anchor = create_anchor_from_motivation(motivation)

            for percept in percepts:
                
                origin_obj = percept.get("origin")
                if origin_obj is None:
                    continue

                try:
                    salience = compute_salience(origin_obj, npc, anchor)
                except Exception as e:
                    print(f"[SALIENCE ERROR] {npc.name} computing salience for {origin_obj}: {e}")
                    continue

                if salience < 5:
                    continue

                description = percept.get("description", str(origin_obj))
                tags = percept.get("tags", [])
                urgency = salience  # or: urgency = max(anchor.weight, salience)

                thought = Thought(
                    subject=npc.name,
                    content=description,
                    origin=origin_obj,
                    urgency=urgency,
                    tags=tags,
                    source=anchor  # useful for later motivation tracking
                )

                if not npc.mind.has_similar_thought(thought):
                    npc.mind.add_thought(thought)
                    print(f"[THOUGHT GEN] {npc.name} thought about {description} (salience={salience}, anchor={anchor.name})")



    
    
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

    def get_salience(self, item):
        return item.salience_for(self.npc)
    #Usage
    #salient_thoughts = sorted(relevant_thoughts, key=self.get_salience, reverse=True)


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