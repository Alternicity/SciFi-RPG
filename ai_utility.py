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
from ai_utility_thought_tools import extract_anchor_from_action


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

        motivations = npc.motivation_manager.get_motivations()
        if not motivations:
            return {"name": "idle"}
        anchors = [create_anchor_from_motivation(m) for m in motivations]

        percepts = list(npc.get_percepts())
        #percepts here is not accessed

        possible_actions = []

        # Basic needs fallback
        if npc.hunger > 7:
            possible_actions.append({
            "name": "eat",
            "params": {},
            "motivation": "satisfy_hunger"
        })

        
        # Add salience-informed actions based on memory
        for anchor in anchors:
            if anchor.name == "obtain_ranged_weapon":
                known_weapon_locations = npc.mind.memory.query_memory_by_tags(["weapons", "shop"])

                for memory in known_weapon_locations:
                    location = memory.target
                    if location:
                        action = {
                            "name": "visit_location",
                            "params": {"location": location},
                            "anchor": anchor
                        }
                        possible_actions.append(action)

        if not possible_actions:
            return {"name": "idle"}
    
        from ai_utility_thought_tools import extract_anchor_from_action

        scored = [(self.score_action(a), a) for a in possible_actions]
        scored.sort(key=lambda x: x[0], reverse=True)

        best_score, best_action = scored[0]

        if npc.is_test_npc:
            print(f"[UtilityAI] {npc.name} chose {best_action['name']} with score {best_score:.2f}")

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

    def score_action(self, action: dict, context: dict = None) -> float:
        npc = self.npc
        context = context or {}

        # Extract anchor from action, fallback to npc.focus
        from ai_utility_thought_tools import extract_anchor_from_action
        anchor = extract_anchor_from_action(action) or npc.mind.attention_focus or npc.default_focus
        if anchor is None:
            print(f"[SCORE] No anchor found for {npc.name}'s action '{action.get('name')}'")
            return 0

        score = 0
        name = action.get("name")
        motivation_type = getattr(anchor, "name", "").lower()

        # === Core Action Types ===
        if name == "visit_location":
            location = action.get("params", {}).get("location")
            if location:
                salience = compute_salience(location, npc, anchor)
                score += salience
                if "shop" in getattr(location, "tags", []):
                    score += 1
                if getattr(location, "contains_weapons", False):
                    score += 2

        elif name == "eat":
            hunger_score = npc.hunger / 10.0  # Normalize to 0–1
            score += hunger_score * anchor.weight  # Amplify by motivational urgency

        elif name == "steal":
            item = action.get("params", {}).get("item")
            if item:
                salience = compute_salience(item, npc, anchor) #this code is depracted anyway
                score += salience

        elif name == "idle":
            # Lowest priority fallback
            score = 0.1

        else:
            print(f"[SCORE] Unknown action type '{name}' for {npc.name}")
            score = 0.1

        print(f"[SCORE] {npc.name} scored action '{name}' as {score:.2f} (anchor: {anchor.name})")
        return score


    def create_anchor_from_thought(self, thought: Thought, name: str, type_: str = "motivation") -> Anchor:
        #is this deprecated there is onelike it in anchor_utils.py
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
            npc.mind.attention_focus = None
            if self.npc.is_test_npc:
                print(f"[UtilityAI] {npc.name} has no thoughts to promote.")
            return

        for thought in thoughts:
            if not isinstance(thought, Thought):
                print(f"[THINK] Skipping invalid thought in {npc.name}'s mind: {thought}")
                continue

            content_lower = thought.content.lower()

            # Example general trigger
            if "obtain" in content_lower and "weapon" in thought.tags:
                anchor = self.create_anchor_from_thought(thought, "obtain_ranged_weapon", type_="motivation")
                
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
                initial_memory_type="episodic",
                function_reference=None,
                implementation_path=None,
                associated_function=None
            )
            npc.mind.memory.add_episodic(memory_entry)
            #anchors are important, promte to semantic here
            #Later logic could be time passed, number of times reinforced, used successfully in decision-making
        # Set attention focus
        npc.mind.attention_focus = max(thoughts, key=lambda t: t.urgency)
        #set npc.default_focus here as well
        self.npc.mind.remove_thought_by_content("No focus")

        if self.npc.is_test_npc:
            print(f"[FOCUS] From promote_thoughts {self.npc.name}'s attention focused on: {self.npc.mind.attention_focus}")

    def examine_episodic_memory(self, episodic_memories):
        event_counts = defaultdict(int)
        for m in episodic_memories:
            key = (m.subject, m.object_, m.verb, m.type)
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

    
    def recall_location_with_tags(npc, required_tags: list, min_salience=0.5):
        memories = npc.mind.memory.query_memory_by_tags(required_tags)
        scored = []
        anchor = npc.mind.attention_focus or npc.default_focus

        for memory in memories:
            location = memory.source
            if location:
                sal = compute_salience(location, npc, anchor)
                scored.append((location, sal))

        if scored:
            scored.sort(key=lambda x: x[1], reverse=True)
            top_location, score = scored[0]
            if score >= min_salience:
                return top_location
        return None
    #usage
    """ loc = recall_location_with_tags(npc, ["weapon", "shop"])
        if loc:
            return {"name": "visit_location", "params": {"location": loc}} """

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
                        tags=percept.get("tags", []),
                    ))
                    self.npc.mind.add_thought(thought)
                    #added
                    thoughts = self.npc.mind.get_all()
                    self.deduplicate_thoughts_by_type(thoughts)
                    self.npc.mind.remove_thought_by_content("No focus")
        
        self.promote_thoughts()       
        self.generate_thoughts_from_percepts()#can we then just add the salient percepts to the parameters here?
        self.promote_thoughts()
        #flow needs to pass to score_action, then choose_action then execute_action

        print(f"[DEBUG] From UtilityAI, def think()")
        print(f"[DEBUG] {self.npc.name} in {self.npc.location.name}")
        print(f"[DEBUG] Percepts: {[p['data'].get('description') for p in percepts]}")
        print(f"[DEBUG] Thoughts: {[str(t) for t in self.npc.mind.thoughts]}")

    def resolve_percept_target_for_anchor(self, anchor, required_tags=None):
        """
        Utility function to return the best percept matching an anchor.
        """
        percepts = self.npc.get_percepts()
        scored = []

        for p in percepts:
            data = p["data"]
            origin = p["origin"]
            if not anchor.is_percept_useful(data):
                continue
            if required_tags and not all(tag in data.get("tags", []) for tag in required_tags):
                continue
            score = anchor.compute_salience_for(data, self.npc)
            scored.append((origin, score))

        if scored:
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[0][0]  # return best match origin
        return None

    def evaluate_turf_war_status(self, region_knowledge):
        # Basic version — maybe no-op or minimal response
        return None
    
    def find_known_locations_by_tags(self, required_tags: list[str], region_name: str = None) -> list:
        npc = self.npc
        region_name = region_name or npc.region.name
        matches = []
        region_knowledge = get_region_knowledge(npc.mind.memory.semantic, region_name)

        if not region_knowledge:
            print(f"[UtilityAI] No region knowledge for {region_name}")
            return []

        for loc_name in region_knowledge.locations:
            location = npc.region.get_location_by_name(loc_name)
            print(f"[DEBUG] from find_known_locations_by_tags Couldn't find location: {loc_name}")
            if not location:
                continue

            if hasattr(location, "get_percept_data"):
                percept_data = location.get_percept_data(observer=npc)
                tags = percept_data.get("tags", [])
                if all(tag in tags for tag in required_tags):
                    matches.append(location)

        return matches

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

                self.npc.mind.remove_thought_by_content("No focus")

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
                self.npc.motivation_manager.increase("rob", amount=thought.weight)
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

def generate_location_visit_thought(npc, location, enabling_motivation=None):
        """
        Creates a thought suggesting visiting a specific location to satisfy a motivation.
        """
        print(f"[THOUGHT GEN] Generating thought to visit {location.name}")
        tags = []
        reason = []

        if hasattr(location, "tags"):
            tags.extend(location.tags)
        if getattr(location, "is_robbable", False):
            tags.append("robbable")
            reason.append("it's robbable")
        if getattr(location, "contains_weapons", False):
            tags.append("weapon")
            reason.append("it has weapons")
        if "shop" in location.name.lower():
            tags.append("shop")
            reason.append("it's a shop")

        thought = Thought(
            subject="visit_location",
            content=f"Maybe I should go to {location.name} because {' and '.join(reason)}.",
            origin="generate_location_visit_thought",
            urgency=6,
            tags=tags + ["location", "move", "travel"],
            source=enabling_motivation,
            weight=6
        )

        npc.mind.add_thought(thought)
        npc.mind.remove_thought_by_content("No focus")

        # Optional: Remove “No focus” placeholder
        npc.mind.remove_thought_by_content("No focus")

        return thought