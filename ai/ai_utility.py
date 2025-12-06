#ai_utility.py

from ai.ai_base import BaseAI
from character_thought import Thought
from character_think_utils import social_thoughts
from actions.npc_actions import visit_location_auto, idle_auto
from character_memory import Memory
from time import time

from anchors.anchor_utils import Anchor, create_anchor_from_motivation, create_anchor_from_thought, create_anchor_from_motivation
from collections import defaultdict
from worldQueries import get_region_knowledge
from memory.memory_entry import MemoryEntry
from debug_utils import debug_print
from create.create_game_state import get_game_state


class UtilityAI(BaseAI):
    def __init__(self, npc):
    #Core cognitive pipeline.
        self.npc = npc
        
    """ Filtering episodic memories and tagging/promoting important ones into thoughts.
        Generating motivations from urgent thoughts.
        Managing the “thinking” lifecycle. """
    
    #self._region_cache = getattr(npc, "region", None)#why does this exist?
    """ @property
    def region(self):
        if self._region_cache is None:
            self._region_cache = getattr(self.npc, "region", None)
        return self._region_cache """

    def choose_action(self, region):
        npc = self.npc
    
        motivations = npc.motivation_manager.get_motivations()
        if not motivations:
            return {"name": "idle"}

        top = npc.motivation_manager.get_highest_priority_motivation()
        mtype = top.type

        # === 2. Basic Need: Procure Food ===
        if mtype == "procure_food" or mtype == "eat":
            return self._choose_procure_food(npc)

        # === 3. Basic Need: Earn Money ===
        if mtype == "earn_money":
            return self._choose_earn_money(npc)

        # === 4. Fun / Social / Recreation ===
        if mtype == "have_fun":
            return self._choose_have_fun(npc)

        # === 5. Unknown → idle fallback ===
        return {"name": "idle"}
    
        debug_print(
            npc,
            f"[CHOOSE] {npc.name} motivation={top.type} → chose {action['name']}",
            category="choose"
        )


    def _choose_procure_food(self, npc):

        # 1. Eat snack if available
        snack = npc.inventory.get_item_with_tag("snack")
        if snack:
            return {"name": "eat_auto", "params": {"item": snack}}

        # 2. Use semantic knowledge
        food_sources = npc.mind.memory.food_sources
        if food_sources:
            best = food_sources.best_source()
            if best and best.location_ref:
                return {
                    "name": "visit_location_auto",
                    "params": {"destination": best.location_ref}
                }

        # 3. No food source → fallback
        return {"name": "idle"}

    def _choose_earn_money(self, npc):
        wp = npc.employment.workplace
        if wp and npc.employment.on_duty(npc.world.tick):
            return {
                "name": "visit_location_auto",
                "params": {"destination": wp}
            }

        # fallback — no workplace assigned
        return {"name": "idle"}
    
    def _choose_have_fun(self, npc):
        prefs = npc.fun_prefs or {}

        # 1. Social fun: meet a friend
        if prefs.get("social", 0) > 5:
            friend = npc.get_close_friend()
            if friend:
                return {
                    "name": "visit_location_auto",
                    "params": {"destination": friend.location}
                }

        # 2. Location-based fun
        fav_loc = npc.world.find_location_matching_fun_prefs(prefs)
        if fav_loc:
            return {
                "name": "visit_location_auto",
                "params": {"destination": fav_loc}
            }

        # 3. Object-based fun (retail therapy)
        if prefs.get("shopping", 0) > 5:
            shop = npc.world.find_nearest_location_with_tag(npc.location, "shop")
            if shop:
                return {
                    "name": "visit_location_auto",
                    "params": {"destination": shop}
                }

        return {"name": "idle"}

    def execute_action(self, action, region):
        """
        Dispatch NPC actions to npc_actions.py functions.
        """
        npc = self.npc
        # Ensure action is a dict
        if not isinstance(action, dict):
            print(f"[ERROR] From UtilityAI Action must be a dict, got: {action}")
            return

        action_name = action.get("name", "")
        params = action.get("params", {})

        # Import action implementations once, before use (prevents UnboundLocalError)
        from actions.npc_actions import (
            visit_location_auto,
            exit_location_auto,
            eat_auto,
            idle_auto
        )

        # Special-case visit_location so it runs exactly once here
        if action_name.lower() == "visit_location":
            # Call visit auto directly
            try:
                result = visit_location_auto(npc, region, **params)
            except Exception as e:
                print(f"[ERROR] visit_location_auto failed: {e}")
                result = None

            # After visiting, remove the visit motivation and stale visit thoughts
            npc.motivation_manager.remove_motivation("visit")
            npc.mind.remove_thoughts_with_tag("visit")
            debug_print(npc, f"[VISIT] execute_action returned {result} — location now {npc.location}", category="visit")
            return result
        


        # --- fallback routing for other actions ---
        action_map = {
            "exit_location": exit_location_auto,
            "eat": eat_auto,
            "idle": idle_auto
        }

        action_func = action_map.get(action_name.lower())
        if not action_func:
            debug_print(npc, f"[EXECUTE] Unknown action '{action_name}' — cannot dispatch; skipping.", category="action")
            return

        debug_print(npc, f"[EXECUTE UTILITYAI] Dispatching {action_name} with params={params}", category="action")
        try:
            return action_func(npc, region, **params)
        except Exception as e:
            print(f"[ERROR] Executing action {action_name}: {e}")


    def score_action(self, action: dict, context: dict = None) -> float:
        """
        Score an action based on motivational anchor + updated salience system.
        This is now intentionally simple.
        """
        npc = self.npc
        context = context or {}

        #Anchors participate only in the scoring phase
        # ----------------------------------------
        # 1. Anchor selection (cleaned up)
        # ----------------------------------------
        from ai_utility_thought_tools import extract_anchor_from_action
        anchor = (
            extract_anchor_from_action(action)

            or npc.mind.attention_focus#What are these lines actualy doing?
            or npc.default_focus
        )

        if anchor is None:
            debug_print(
                npc,
                f"[ANCHOR] No anchor found for scoring '{action.get('name')}'. Returning 0.",
                category="ANCHOR"
            )
            return 0.0

        action_name = action.get("name", "")
        score = 0.0

        # ----------------------------------------
        # 2. Handle core actions
        # ----------------------------------------

        # === Movement (visit_location_auto) ===
        if action_name == "visit_location_auto":
            destination = (
                action.get("params", {}).get("destination")
                or action.get("params", {}).get("location")
            )

            if destination:
                salience = anchor.compute_salience_for(destination, npc, anchor)#we must check the paramters in the anchor
                score += salience

                debug_print(
                    npc,
                    f"[SCORE] Movement → {npc.name} → {destination.name}: salience={salience:.2f}",
                    category="action"
                )
                
        # === Eating ===
        elif action_name == "eat_auto":
            item = action.get("params", {}).get("item")
            if item:
                salience = anchor.compute_salience_for(item, npc)
                score += salience

                debug_print(
                    npc,
                    f"[SCORE] Eat → {npc.name} eats {item.name}: salience={salience:.2f}",
                    category="action"
                )


        # === Idle ===
        elif action_name == "idle":
            score = 0.1  # Always valid but low
            debug_print(
                npc,
                f"[SCORE] Idle assigned fallback score={score:.2f}",
                category="action"
            )

        # === Unknown ===
        else:
            debug_print(
                npc,
                f"[SCORE] Unknown action '{action_name}' — assigning soft fallback.",
                category="action"
            )
            score = 0.1

        # ----------------------------------------
        # 3. Motivation urgency weighting
        # ----------------------------------------

        score *= anchor.weight

        debug_print(
            npc,
            f"[SCORE] from UtilityAI.score_action {npc.name} '{action_name}': {score:.2f} anchor={anchor.name}, anchor weight={anchor.weight} score={score}",
            category="action"
        )

        return score


    def promote_thoughts(self):
        npc = self.npc
        mind = npc.mind
        game_state = get_game_state()

        # Guard: only promote once per tick
        if getattr(npc, "_last_promote_tick", -1) == game_state.tick:
            return

        # mark we've run this tick
        npc._last_promote_tick = game_state.tick

        if not mind.thoughts:
            return

        # Pick the most urgent thought
        strongest = max(mind.thoughts, key=lambda t: (t.urgency, getattr(t, "timestamp", 0)))
        
        # Create or update an anchor from that thought
        anchor = create_anchor_from_thought(npc, strongest, name=strongest.primary_tag() or "general")
        #and here

        if not anchor:
            # Could happen if thought already anchored or duplicate detected
            return

        # --- Check enabler relationships for debug awareness ---
        #tells me if, say, a rob anchor is being promoted before obtain_ranged_weapon exists - or vice versa
        has_enabler = False
        for a in getattr(npc, "anchors", []):
            if getattr(a, "enables", None) and anchor.name in a.enables:
                has_enabler = True
                break

        if not has_enabler:
            debug_print(
                npc,
                f"[ANCHOR-PROMOTE] '{anchor.name}' promoted without enabler relationship. "
                f"Existing anchors: {[a.name for a in npc.anchors]}",
                category="anchor"
            )
        else:
            debug_print(
                npc,
                f"[ANCHOR-PROMOTE] '{anchor.name}' promoted WITH enabler(s).",
                category="anchor"
            )

        # Boost motivation
        anchor_weight = getattr(anchor, "weight", 1.0)
        top_motive = getattr(self.npc.motivation_manager, "top_motivation", None)
        top_urgency = getattr(top_motive, "urgency", 1) if top_motive else 1
        strongest_urgency = getattr(strongest, "urgency", 1)

        urgency_base = max(top_urgency, strongest_urgency)
        #Take whichever is greater
        """ top_urgency comes from the motivation manager, e.g., how strongly the NPC already feels about "rob" or "obtain_ranged_weapon".
        strongest_urgency comes from the new thought being promoted """

        urgency_delta = min(int(anchor_weight * urgency_base), 3)
        #Scale urgency by the anchor’s weight, but clamp it to a maximum of 3
        #int() → converts it to an integer.

        npc.motivation_manager.update_motivations(motivation_type=anchor.name, urgency=urgency_delta)
        
        # Set attention focus
        npc.mind.attention_focus = strongest
        npc.default_focus = anchor
        
        if npc.is_test_npc:
            debug_print(
                f"[FOCUS] {npc.name} promoted thought '{strongest.content}' "
                f"→ anchor '{anchor.name}' (urgency +{urgency_delta})",
                category="think"
            )
            print(f"[FOCUS] From promote_thoughts {self.npc.name}'s attention focused on: {self.npc.mind.attention_focus}")

    def examine_episodic_memory(self, episodic_memories):
        event_counts = defaultdict(int)
        npc = self.npc
        for m in episodic_memories:
            key = (m.subject, m.object_, m.verb, m.type)
            event_counts[key] += 1

            if event_counts[key] >= 3:
                debug_print(npc, f"[INSIGHT] {m.subject} has done {m.verb} {event_counts[key]} times.", category = "insight")
            
            if m.verb == "finished_shift":
                npc.add_anchor("just_got_off_shift")#there is currently no add_anchor()
                #anchor_utils.py is the obvious place to put one, but so far we have been adding anchors without a function
                #So should this be npc.current_anchor = 
                #perhaps the function makes the most sense, and it could push any per-existing anchor into npc.anchors
                #(which is a list of anchors)
                debug_print(npc, "[SHIFT] {self.npc.name} Shift ended → activating just_got_off_shift anchor", category="employment")
                

            #call trigger just_got_off_shift=True
            

    def deduplicate_thoughts_by_type(thoughts):
        #call it: After thoughts are generated from percepts, before promotions happen
        #do we want all thoghts of the same type to get de duped?
        #Should the npc notice that some thoughts are recurrent?
        seen = {}
        for t in thoughts:
            if t.type not in seen or t.urgency > seen[t.type].urgency:
                seen[t.type] = t
        return list(seen.values())

    def evaluate_candidates_with_anchor(npc, region):
        candidates = npc.mind.memory.get_candidate_locations(region)
        for loc in candidates:
            #score = visit_to_xyz_anchor.compute_salience_for(loc, npc)
            pass 
            #to get region to be defined here.
            #I added npc and region to the parameters.
            #visit_to_rob_anchor remains marked an not defined.
            #If I import that here is there a risk of circular import problems?
            #can we get it via npc.current_anchor.visit_to_rob_anchor ?




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
        from region.region import Region
        #tmp if/print block for debug
        if not isinstance(region, Region):
            print(f"[DEBUG] {self.npc.name} UtilityAI def think calling observe with region={region}, location={self.npc.location}")
            print(f"[UtilityAI] Bad region: {region} ({type(region).__name__}) for {self.npc.name}")

        #observe calls have moved to the game loop tick  
        #self.npc.observe(region=region, location=self.npc.location)

        region_knowledge = get_region_knowledge(self.npc.mind.memory.semantic, region.name)
        if region_knowledge:
            turf_status = self.evaluate_turf_war_status(self.npc, region_knowledge)  # Base awareness
        #self.promote_thoughts()# Delete in favour of calling from simulate_days()

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

        candidate_thoughts = [] #candidate_thoughts not accesssed
        for motivation in motivations:
            anchor = create_anchor_from_motivation(self.npc, motivation)
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
        
        #self.promote_thoughts()# Delete in favour of calling from simulate_days()
        self.generate_thoughts_from_percepts()#can we then just add the salient percepts to the parameters here?

        #Add a function for this:
        social_thoughts(self)
        

        print(f"[DEBUG] From UtilityAI, def think()")
        print(f"[DEBUG] {self.npc.name} in {self.npc.location.name}")
        print(f"[DEBUG] Percepts: {[p['data'].get('description') for p in percepts]}")
        print(f"[DEBUG] Thoughts: {[str(t) for t in self.npc.mind.thoughts]}")

    def resolve_percept_target_for_anchor(self, anchor, required_tags=None):
        """
        Attempts to resolve a concrete target object for this anchor.
        Preference order:
        1. anchor.target_object or anchor.target
        2. anchor.source (if perceptible)
        3. highest-salience percept matching tags
        """
        if not anchor:
            return None

        # 1️⃣ Directly linked targets
        if getattr(anchor, "target_object", None):
            return anchor.target_object
        if getattr(anchor, "target", None):
            return anchor.target
        if getattr(anchor, "source", None):
            return anchor.source

        # 2️⃣ Fallback: scan percepts
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
            return scored[0][0]  # best origin
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
        percepts = list(npc.observation_component._percepts.values())

        motivations = npc.motivation_manager.get_urgent_motivations()
        if not motivations:
            return

        for motivation in motivations:
            anchor = create_anchor_from_motivation(self.npc, motivation)

            for percept in percepts:
                
                origin_obj = percept.get("origin")
                if origin_obj is None:
                    continue
                from events import Event
                if isinstance(origin_obj, Event):
                    continue

                try:
                    from anchors.anchor_utils import _normalize_percept
                    normalized = _normalize_percept(percept.get("data", percept), npc)

                    # compute_salience may return None or a number — normalize and guarantee numeric
                    raw_sal = compute_salience(normalized, npc, anchor)#now in ai_utility.py
                    salience = normalize_salience(raw_sal)
                    if not isinstance(salience, (int, float)):
                        # Fallback to zero salience to prevent TypeErrors downstream
                        salience = 0.0

                except Exception as e:
                    # surface the error but keep the loop running — treat as zero salience
                    debug_print(npc, f"[THINK ERROR] {npc.name} failed to normalize/compute salience for {origin_obj}: {e}", category="think")
                    salience = 0.0  # fallback to non-crash behavior

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
                    tags=tags,#check!
                    source=anchor  # useful for later motivation tracking
                )

                if not npc.mind.has_similar_thought(thought):
                    npc.mind.add_thought(thought)
                    debug_print(npc, f"[THINK] {npc.name} -> thought: {thought.content} (tags={thought.tags}, urgency={thought.urgency})", category="think")

                    if percept.object is npc:
                        return 0.0  # skip self
                    debug_print(npc, f"[THINK] {npc.name} thought about {description} (salience={salience}, anchor={anchor.name})", category="think")
                    

                self.npc.mind.remove_thought_by_content("No focus")

    def evaluate_thoughts(self): #remove or override in subclasses
        """Loop through unresolved thoughts and increase motivations accordingly."""
        #Eventually this should evolve into a utility-based appraisal. I think
        npc = self.npc
        if not getattr(npc, "is_test_npc", False):
            return  # suppress for non-test NPCs

        for thought in npc.mind.thoughts:
            if thought.resolved:
                continue #possibly write or create corollories and failed thoughts
                return


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
    Designed for general-purpose NPCs (non-criminal).
    """
    debug_print(npc, f"[THINK] Generating thought to visit {location.name}", category="think")
    
    tags = []
    reasons = []

    # Collect location tags if available
    if hasattr(location, "tags"):
        tags.extend(location.tags)

    # General contextual logic (non-criminal)
    # Expand this as your world adds more location attributes.
    if getattr(location, "serves_food", False):
        tags.append("food")
        reasons.append("they serve food")
    if getattr(location, "provides_rest", False):
        tags.append("rest")
        reasons.append("it’s a place to rest")
    if getattr(location, "is_social_spot", False):
        tags.append("social")
        reasons.append("people gather there")
    if getattr(location, "sells_items", False):
        tags.append("shop")
        reasons.append("it’s a shop")
    if getattr(location, "offers_work", False):
        tags.append("work")
        reasons.append("there might be work opportunities")
    if getattr(location, "teaches_skills", False):
        tags.append("learning")
        reasons.append("I could learn something there")
    if getattr(location, "provides_entertainment", False):
        tags.append("fun")
        reasons.append("it sounds enjoyable")
    if getattr(location, "is_safe_spot", False):
        tags.append("safe")
        reasons.append("it feels safe there")

    # Default reason if none found
    if not reasons:
        reasons.append("it seems interesting")

    thought = Thought(
        subject="visit_location",
        content=f"Maybe I should go to {location.name} because {' and '.join(reasons)}.",
        origin="generate_location_visit_thought",
        urgency=6,
        tags=tags + ["location", "move", "travel", "intention"],
        source=enabling_motivation,
        weight=6,
    )

    npc.mind.add_thought(thought)

    # Remove placeholder “No focus” thoughts if present
    npc.mind.remove_thought_by_content("No focus")

    return thought

def normalize_salience(value):
    return value if isinstance(value, (int, float)) else 0.0

def compute_salience(obj, observer, anchor=None):
    if anchor:
        return anchor.compute_salience_for(obj, observer)
    return getattr(obj, "salience", 0.5)