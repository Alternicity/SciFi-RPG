#ai_gang.py
import time
from ai_utility import UtilityAI, generate_location_visit_thought
from worldQueries import get_viable_robbery_targets
from npc_actions import steal_auto, rob_auto, idle_auto, visit_location_auto
from character_thought import Thought
from worldQueries import get_viable_robbery_targets, get_region_knowledge
from motivation import Motivation
from summary_utils import summarize_motivations_and_percepts
import random
from city_vars import GameState
from create_game_state import get_game_state
from memory_entry import RegionKnowledge, ShopsSellRangedWeapons
from character_think_utils import promote_relevant_thoughts, should_promote_thought
#from character_memory import Memory
from salience import compute_salience
from anchor_utils import Anchor, create_anchor_from_motivation, ObtainWeaponAnchor
from perceptibility import PerceptibleMixin


class BossAI(UtilityAI):
    def think(self, region):
        rk = get_region_knowledge(self.mind.memory.semantic, region.name)
        if rk:
            evaluate_turf_war_status(self.npc, observed_region=rk)
        self.promote_thoughts()
        self.npc.mind.remove_thought_by_content("No focus")

class GangCaptainAI(UtilityAI):
    def think(self, region):
        rk = get_region_knowledge(self.mind.memory.semantic, region.name)
        if rk:
            evaluate_turf_war_status(self.npc, observed_region=rk)

        self.promote_thoughts()
        self.npc.mind.remove_thought_by_content("No focus")

    def choose_action(self, region):

        if self.npc.is_test_npc:
            top_motivation = self.npc.motivation_manager.get_highest_priority_motivation()
            print(f"[CHOOSE_ACTION] {self.npc.name} motivation: {top_motivation.type} (urgency: {top_motivation.urgency})")

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
    def __init__(self, npc):
        super().__init__(npc)  # calls UtilityAI.__init__, which sets self.npc = npc
        #It calls super().promote_thoughts(), so it runs the base ai_utility.py version first.
        
        """Custom salience tuning, override functions in UtilityAI
        Let UtilityAI produce options, and GangMemberAI choose from them based on gang-specific rules"""

    def promote_thoughts(self):
        super().promote_thoughts()
        npc = self.npc

        for thought in npc.mind.thoughts:
            if "intention" in thought.tags and "weapon" in thought.content:
                anchor = Anchor(
                    name="obtain_ranged_weapon",
                    type="motivation",
                    weight=thought.urgency,
                    source=thought,
                    tags=thought.tags
                    )

                npc.motivation_manager.update_motivations(anchor.name, urgency=thought.urgency, source=thought)
                print(f"[GANG] {npc.name} reinforced motivation to obtain weapon from thought: {thought.content}")
                self.npc.mind.remove_thought_by_content("No focus")

        if npc.isTestNPC and not npc.attention_focus:
            print(f"[GandgMemberAI] {npc.name} did not promote any thoughts this cycle.")

    #For AI Subclasses that need special behavior, override this method only
    def compute_salience_for_motivation(self, percept, motivation):
        return compute_salience(percept, self.npc, create_anchor_from_motivation(motivation))

    def choose_action(self, region):
        print(f"[CHECK] choose_action called")
        known_weapon_locations = []
        npc = self.npc
        top_motivation = npc.motivation_manager.get_highest_priority_motivation()
        anchor = create_anchor_from_motivation(top_motivation)
        npc.current_anchor = anchor
        
        
        if self.npc.is_test_npc:
            print(f"[ANCHOR DEBUG] Active anchor: {npc.current_anchor.name}, tags: {npc.current_anchor.tags}")

        # Handle explicit motivations
        if top_motivation:
            if top_motivation.type == "rob":
                return self.resolve_robbery_action(region)
            elif top_motivation.type == "steal":
                return self.resolve_steal_action(region)

        percepts = npc.get_percepts()

        scored = [(p, anchor.compute_salience_for(p["data"], npc)) for p in percepts]
        scored.sort(key=lambda x: x[1], reverse=True)

        weapon = None  # <-- declared early for final fallback

        if npc.is_test_npc:
            for p, score in scored:
                data = p["data"]
                origin = p["origin"]

                if not anchor.is_percept_useful(data):
                    continue
                if npc.inventory.has_item(origin):
                    continue

                print(f"[AI DECISION] {npc.name} sees {origin.name} (score {score:.2f}) as useful.")

                # Optional salience threshold
                if "weapon" in data.get("tags", []) and score >= 0.8:
                    print(f"[SALIENCE DEBUG] {npc.name} sees {data.get('name')} with score {score:.2f}")
                    print(f"[AI DECISION] {npc.name} sees {origin.name} as highly salient. Attempting to steal.")

                for debug_p, debug_score in scored:
                    print(f"[DEBUG] Percept: {debug_p['data'].get('name', debug_p['data'].get('type'))}, Salience: {debug_score:.2f}")

                weapon = origin  # set weapon for fallback trace/logs
                return {"name": "Steal", "params": {"item": origin}}

            # Try to find a useful percept to act on
            for p, score in scored:
                data = p["data"]
                origin = p["origin"]

                if not anchor.is_percept_useful(data):
                    continue
                if npc.inventory.has_item(origin):
                    continue

                # Optional salience threshold
                if score < 0.8:
                    print(f"[SKIP] {npc.name} sees {origin.name} but score {score:.2f} is too low")
                    continue

                print(f"[AI DECISION] {npc.name} sees {origin.name} (score {score:.2f}) as useful.")
                return {"name": "Steal", "params": {"item": origin}}

            # No suitable percept was found
            if scored:
                top_percept, top_score = scored[0]
                print(f"[SKIP] {npc.name} saw top percept '{top_percept['data'].get('name')}' (score {top_score:.2f}), but it was not useful or already owned.")
            else:
                print(f"[AI] {npc.name} found no percepts worth acting on.")

                return {"name": "Steal", "params": {"item": origin}}

            # Optional fallback: try to recall weapon locations from memory
            if anchor.name == "obtain_ranged_weapon":
                if npc.location and any(loc.target == npc.location for loc in npc.mind.memory.query_memory_by_tags(["weapons", "shop"])):
                    print(f"[MEMORY FALLBACK] {npc.name} is already at a known weapon shop: {npc.location.name}")
                else:
                    print(f"[MEMORY FALLBACK] {npc.name} is searching memory for weapon locations...")
                    known_weapon_locations = npc.mind.memory.query_memory_by_tags(["weapons", "shop"])
                    if known_weapon_locations:
                        location = known_weapon_locations[0].target
                        if location:
                            print(f"[MEMORY DECISION] {npc.name} decides to visit {location.name} from memory.")
                            return {"name": "visit_location", "params": {"location": location}}

            # Create a guiding thought
            motivation = top_motivation
            new_thought = Thought(
                subject="ranged_weapon",
                content="Maybe I should get a weapon before robbing.",
                origin="resolve_robbery_action",
                urgency=7,
                tags=["rob", "shop", "weapon", "enable", "crime"],
                timestamp=time.time(),
                source=motivation,
                weight=7
            )
            npc.mind.add_thought(new_thought)
            npc.mind.remove_thought_by_content("No focus")
            npc.attention_focus = new_thought

            if npc.inventory.has_ranged_weapon():
                npc.mind.remove_thought_by_content("Maybe I should get a weapon before robbing.")
                npc.motivation_manager.resolve_motivation("obtain_ranged_weapon")

            npc.motivation_manager.update_motivations("rob", urgency=new_thought.weight)
            npc.default_focus = anchor
            npc.ai.promote_thoughts()

            # Try visiting best location via memory
            known_locations = npc.mind.memory.query_memory_by_tags(["location"])
            location_scores = []

            for memory in known_locations:
                location = memory.source
                if not location:
                    continue

                salience = compute_salience(location, npc, anchor)
                location_scores.append((location, salience))

            if location_scores:
                location_scores.sort(key=lambda x: x[1], reverse=True)
                best_location, score = location_scores[0]
                print(f"[SALIENT] Best known location for anchor '{anchor.name}' is {best_location.name} (score: {score:.2f})")

                if score > 0.5:
                    thought = generate_location_visit_thought(npc, best_location, enabling_motivation=anchor)
                    npc.attention_focus = thought
                    npc.default_focus = anchor
                    return {"name": "visit_location", "params": {"location": best_location}}
                

            print(f"[POST-THOUGHT] Thoughts: {[t.summary() for t in npc.mind.thoughts]}")
            for m in npc.mind.memory.semantic.get("shop_knowledge", []):
                print(f"[DEBUG] Semantic memory: {m.description} tags: {m.tags} source: {getattr(m, 'source', None)}")
            
            if weapon:
                print(f"[CHOOSE ACTION] {npc.name} returns Steal with item: {weapon.name}")
                return {"name": "Steal", "params": {"item": weapon}}
                    
        # Fall back: seed test case with rob if no motivation exists
            if not npc.motivation_manager.get_motivations():
                npc.motivation_manager.update_motivations("rob", urgency=5)
            #this block is temporary as it is specific to test case 1. What if the npc will not rob after stealing?

        #restore a previous default_focus if attention_focus is lost here

        from display import display_percepts_table
        display_percepts_table(npc)

    def execute_action(self, action, region):
        npc = self.npc 

        if not isinstance(action, dict):
            print(f"[ERROR] Action must be a dict, got: {action}")
            return
                
        name = action.get("name")
        params = action.get("params", {})

        action_map = {
            "Rob": rob_auto,
            "Steal": steal_auto,
            "visit_location": visit_location_auto,
            "Idle": idle_auto,
        }

        action_func = action_map.get(name) #just retrieves the function object.
        if action_func:
            print(f"[DEBUG] {npc.name} will execute: {name} with params: {params}")
            action_func(npc, region, **params)
            print(f"[POST-ACTION] {npc.name} is now at {npc.location.name}")
            # After visiting a location, observe surroundings
            if name == "visit_location":
                npc.observe(location=npc.location, region=region)
                from display import (
                    show_shop_inventory,
                    display_employees,
                    display_npc_mind,
                )
                from location import Shop

                # Only do this for test NPCs and if new location is a shop
                if npc.is_test_npc and isinstance(npc.location, Shop):
                    show_shop_inventory(npc, npc.location)
                    display_employees(npc.location)
                    display_npc_mind(npc)

            action_func(npc, region, **params) #the actual function call
        else:
            print(f"[GangMemberAI] Unknown action name: {name}")
            
        if npc.is_test_npc:
            #print(f"[MIND DUMP] from GangMemberAI execute_action {npc.name} current thoughts: {[str(t) for t in npc.mind]}")
            for t in npc.mind:
                        print(f"[MIND DUMP] from GangMemberAI execute_action {npc.name} current thoughts: ")
                        print(f" - {t}")
        if npc.is_test_npc:
            print(f"[POST-ACTION DEBUG] {npc.name} is now at {npc.location.name}")
            print(f"[POST-ACTION] Current attention: {npc.attention_focus}")
            print(f"[POST-ACTION] Current motivation: {npc.motivation_manager.get_urgent_motivations()}")
            print(f"[DEBUG] {npc.name}'s inventory: {[item.name for item in npc.inventory]}")
                                                                                  

    def resolve_weapon_target_from_percepts(self):
        percepts = self.npc.get_percepts()
        anchor = Anchor(name="obtain_ranged_weapon", type="motivation", weight=1.5)
        scored = [(p, anchor.compute_salience_for(p["data"], self.npc)) for p in percepts]
        scored.sort(key=lambda x: x[1], reverse=True)
        if scored:
            top_percept, score = scored[0]
            origin = top_percept["origin"]
            if hasattr(origin, "location"):
                print(f"[TARGET] Weapon seen at: {origin.location.name}")
                self.npc.mind.add_thought(
                    Thought(
                        content=f"I saw a weapon at {origin.location.name}",
                        subject=origin.location.name,
                        origin="percept",
                        urgency=anchor.weight,
                        tags=["weapon", "shop", "target"],
                        source=origin
                    )
                )
                self.npc.mind.remove_thought_by_content("No focus")

                if "weapon" in top_percept["data"].get("tags", []):
                    weapon = top_percept["origin"]
                    loc = getattr(weapon, "location", None)
                    if loc:
                        memory = ShopsSellRangedWeapons(location_name=loc.name)
                        memory.source = loc
                        self.npc.mind.memory.add_to_semantic("shop_knowledge", memory)
                #You don’t need to return an action here — just populate memory/thoughts. 
                # The action will be chosen later from context.
        #get percepts. Can the npc perceive a target location with a targetteable weapons?

    def resolve_weapon_target_from_memory(self):
        npc = self.npc
        found_any = False  # Track if we acted

        region_knowledge = [
            m for m in npc.mind.memory.semantic.get("region_knowledge", [])
            if isinstance(m, RegionKnowledge) and m.region_name == npc.region.name
        ]
        print(f"[DEBUG] RegionKnowledge entries: {[rk.locations for rk in region_knowledge]}")

        for knowledge in region_knowledge:
            for loc_name in knowledge.locations:
                location = npc.region.get_location_by_name(loc_name)
                if not location:
                    continue

                # Confirm it's a shop that sells ranged weapons
                from location import Shop
                if not isinstance(location, Shop):
                    if npc.is_test_npc:
                        print(f"[DEBUG] {location.name} is not a Shop instance.")
                    continue
                if not location.inventory.has_ranged_weapon():
                    print(f"[DEBUG] {location.name} does not sell ranged weapons.")
                    print(f"[DEBUG] Shop inventory: {[item.name for item in location.inventory.items.values()]}")

                    continue
                
                print(f"[MEMORY CHECK] Considering shop: {location.name}")
                print(f"[MEMORY CHECK] Inventory items: {[item.name for item in location.inventory.items.values()]}")
                print(f"[MEMORY CHECK] Has ranged weapon: {location.inventory.has_ranged_weapon()}")


                existing = npc.mind.memory.query_memory_by_tags(["weapons", "shop"])
                print(f"[DEBUG] Existing shop memories: {[mem.source.name if mem.source else 'None' for mem in existing]}")
                print(f"[DEBUG] Existing shop memories: {[mem.source.name for mem in existing if mem.source]}")
                
                if any(mem.has_tags(["weapon", "shop"]) and mem.source == location for mem in existing):
                    #exising is not defined here

                    # Add semantic memory about this shop
                    memory = ShopsSellRangedWeapons(location_name=location.name)
                    memory.source = location
                    npc.mind.memory.add_to_semantic("shop_knowledge", memory)
                    print(f"[MEMORY ADD] Added shop weapon memory: {memory.description} tags: {memory.tags}")
                    print(f"[MEMORY] {npc.name} added memory of {location.name} selling weapons.")
                    print(f"[MEMORY ADD] {npc.name} adds memory of shop: {location.name} with tags: {memory.tags}")


                    # Add enabling thought
                    thought = Thought(
                        content=f"I remember {location.name} sells weapons.",
                        subject=location.name,
                        origin="resolve_weapon_target_from_memory",
                        urgency=6,
                        tags=["weapon", "shop", "memory", "visit"],
                        timestamp=time.time(),
                        source=memory,
                    )
                    npc.mind.add_thought(thought)
                    npc.attention_focus = thought
                    npc.mind.remove_thought_by_content("No focus")
                    print(f"[MEMORY] {npc.name} thought of visiting {location.name} for weapons.")

                    found_any = True
                    break  # Comment this `break` if you want to process *all* valid locations

            if not found_any:
                print(f"[MEMORY] {npc.name} found no weapon-selling shops in memory.")


    def resolve_obtain_weapon_target(self, region):#region is not accessed
        self.resolve_weapon_target_from_percepts()
        self.resolve_weapon_target_from_memory()
        return {"name": "idle", "params": {}}

    def debug_percepts(npc, context=""):
        print(f"\n--- [PERCEPT DEBUG] {npc.name} ({context}) ---")
        for p in npc.get_percepts():
            d = p.get("data", {})
            print(f"→ {d.get('type')} | {d.get('name')} | tags: {d.get('tags')} | salience: {p.get('salience')}")

    def is_viable_robbery_target(location):
        return getattr(location, "robbable", False) and not getattr(location, "heavily_guarded", False)


    def resolve_robbery_action(self, region):
        npc = self.npc

        # Do we have a ranged weapon?
        if not npc.inventory.has_ranged_weapon():
            anchor = Anchor(name="obtain_ranged_weapon", type="motivation", weight=5)
            self.npc.motivation_manager.update_motivations(anchor.name, urgency=anchor.weight)

            if not npc.inventory.has_ranged_weapon():
                return self.resolve_obtain_weapon_target(region)
            
            print(f"[CHAIN] Enabling motivation '{anchor.name}' activated.")

            #enable_motive marked as not defined
            return self.resolve_obtain_weapon_target(region)

        # Are we in a robbable location?
        if npc.location and getattr(npc.location, "robbable", False):
            return {"name": "Rob", "params": {"location": npc.location}}

        # Else: No robbable location or still lacking weapon
        return {"name": "Idle", "params": {}}

    def think(self, region):
        rk = None  # Always define upfront to avoid UnboundLocalError
        region_knowledge = get_region_knowledge(self.npc.mind.memory.semantic, region.name)
        if self.npc.isTestNPC:
            print(f"\n--- from GangMemberAI, {self.npc.name} () ---")
            #print("\n" * 1)     
            print(f"{self.npc.name}:\n{summarize_motivations_and_percepts(self.npc)}")
            print("\n" * 1)

            if rk:
                evaluate_turf_war_status(self.npc, observed_region=rk) #only if is street gang memeber?

        for memories in self.npc.mind.memory.semantic.values():
            for memory in memories:
                if not hasattr(memory, 'tags'):
                    print(f"[ERROR] Invalid memory object: {memory} (type: {type(memory)})")
                    continue
                if "weapon" in memory.tags:
                    thought = Thought(
                    content=f"Target spotted for robbery",
                    subject=None,
                    origin="ai_gang.robbery_decision",
                    tags=["robbery", "shop", "weapon"],
                    urgency=3,
                    timestamp=time.time()
                )
                    self.npc.mind.add_thought(thought)
                    self.npc.mind.remove_thought_by_content("No focus")
        if not self.npc.mind.thoughts:

            idk_thought = Thought(
                subject="confusion",
                content="No focus",
                origin="GangMemberAI.think",
                urgency=0,
                tags=["confusion"]
            )

            self.npc.mind.add_thought(idk_thought)

        motivations = self.npc.motivation_manager.get_motivations()#motivations not actually accessed
        # After gathering motivation
        motivation = self.npc.motivation_manager.get_highest_priority_motivation()
        if not motivation:
            print(f"[THINK] No motivation found for {self.npc.name}")
            return
        
        anchor = create_anchor_from_motivation(motivation)
        # If the anchor has no tags, patch them from defaults
        if not anchor.tags:
            anchor.tags = motivation.tags

        self.npc.current_anchor = anchor
        self.npc.attention_focus = anchor # OR: a related Thought, if one exists. Yes but it is defined below here
        #If you're transitioning from rob → obtain_weapon, the obtain_weapon anchor becomes the new center of attention.
        if self.npc.is_test_npc:
            (f"[ANCHOR DEBUG] Thinking about: {anchor.name} (tags: {anchor.tags})")

        #This lets Anchors "focus" the NPC’s mind, spotlighting thoughts that help them act.
        for thought in self.npc.mind.thoughts:
            if set(thought.tags) & set(anchor.tags):
                thought.urgency += 1
            else:
                thought.urgency *= 0.9  # decay unrelated thoughts

        recalled = self.npc.mind.memory.query_memory_by_tags(anchor.tags)
        for m in recalled:
            if isinstance(m, RegionKnowledge):
                print(f"[RECALL] Anchor {anchor.name} brought up memory: I know {m.region_name} pretty well.")
            else:
                print(f"[RECALL] Anchor {anchor.name} brought up memory: {getattr(m, 'description', 'Unknown memory')}")

        self.promote_thoughts()

        if motivation.type == "rob":
            if not self.npc.inventory.find_item("ranged_weapon"):
                enable_motive = "obtain_ranged_weapon"
                self.npc.motivation_manager.update_motivations(motivation_type=enable_motive, urgency=5)
                print(f"[CHAIN] Promoting enabling motivation: {enable_motive}")

            if region_knowledge:
                for loc_name in region_knowledge.locations or set():
                    loc_obj = self.npc.region.get_location_by_name(loc_name)
                    if not loc_obj or not getattr(loc_obj, "robbable", False):#see def is_viable_robbery_target
                        continue  # Skip non-robbable locations

                    thought = Thought( #This thought might be needed above
                        content=f"Maybe I should rob {loc_obj.name}.",
                        subject=loc_obj.name,
                        origin="RegionKnowledge",
                        urgency=7,
                        tags=["rob", "shop"],
                        timestamp=time.time()
                    )
                    self.npc.mind.add_thought(thought)
                    self.npc.mind.remove_thought_by_content("No focus")

            if self.npc.has_recently_acquired("ranged_weapon") and self.npc.motivation_manager.has("rob"):
                thought = Thought(
                    subject="robbery",
                    content="Now that I'm armed, I could rob this shop.",
                    origin="post_theft",
                    urgency=8,
                    tags=["rob", "crime", "weapon", "opportunity"],
                    timestamp=time.time()
                )
                self.npc.mind.add_thought(thought)
                self.npc.attention_focus = thought

        relevant_thoughts = [
            t for t in self.npc.mind.thoughts
            if isinstance(t, Thought) and t.salience_for(self.npc, anchor=anchor) > 0
        ]
        salient_thoughts = sorted(relevant_thoughts, key=lambda t: t.salience_for(self.npc, anchor=anchor), reverse=True)
        #all salience is computed relative to an anchor
        high_salient = [t for t in salient_thoughts if t.salience_for(self.npc, anchor) >= 6]#if change search high_salient and edit
        if salient_thoughts:
            top = salient_thoughts[0]
            if self.npc.is_test_npc:
                print(f"[THINK] {self.npc.name} Top salient thought: '{top.content}' (score: {top.salience_for(self.npc):.2f})")

        for t in high_salient: #currently >= 6
            score = t.salience_for(self.npc, anchor=anchor)
            print(f"[THINK] {self.npc.name} Salient thought: '{t.content}' (score: {score:.2f})")
            
                # Finalize attention
        self.npc.attention_focus = salient_thoughts[0] if salient_thoughts else anchor

        if self.npc.is_test_npc:
            print(f"[GangMemberAI think()] {self.npc.name} current thoughts: {[str(t) for t in self.npc.mind.thoughts]}")

        # Memory review & supporting thought generation
        episodic_memories = self.npc.mind.get_episodic()
        self.examine_episodic_memory(episodic_memories)

        # Only generate perceptual thoughts if attention isn't already focused
        if not high_salient:
            self.generate_thoughts_from_percepts()

        # Promote any new insights based on current mental context
        self.promote_thoughts()

        # Refine & structure relevant thoughts
        promote_relevant_thoughts(self.npc, self.npc.mind.thoughts)

    def resolve_steal_action(self, region):
            target = target = self.resolve_obtain_weapon_target(region)

            if target:

                return {
                    "name": "Steal",
                    "params": target.get("params", {}) #Or standardize format to return target  # if target is already in the correct {"name": ..., "params": ...} format
                }
            return {"name": "Idle"}
        
    def resolve_explore_action(self, region): 
            from location import Shop
            target = self.resolve_obtain_weapon_target(region) #no longer in utility_ai
            if target:
                self.npc.attention_focus = target
                self.npc.mind.add(Thought(
            content=f"Target spotted for robbery",
            subject=target,
            origin="resolve_explore_action",
            urgency=5,
            tags=["robbery", "target"],
            timestamp=time.time()
        ))
                return {
                    "name": "Rob",
                    "target": target
                }
            
            if target == Shop:
                thought = Thought(
                    content=f"Target spotted for robbery",
                    subject=target,
                    origin="Memory",
                    tags=["explore", "shop"],
                    urgency=2,
                    timestamp=time.time()
                )
                self.npc.mind.add_thought(thought)
                self.npc.mind.remove_thought_by_content("No focus")

game_state = get_game_state() #why is this here?

#utilty functions, called from within gang character classes

""" Refactor evaluate_turf_war_status and similar character AI methods to rely
only on the agents perceived knowledge (via RegionKnowledge object), not global truths from Region """

def evaluate_turf_war_status(npc, observed_region):
    #needs to call TurfWar event object 

    my_faction = npc.faction

    if not my_faction.is_street_gang:
        if hasattr(region_knowledge, "region_gangs"):
            thought = Thought(
                content=f"Turf war active in region: {observed_region.region_name}. The homeless street gangs are desperate.",
                origin="Faction Intel",
                urgency=5,
                tags=["turf_war", "gang_conflict", "intel"],
                source="SemanticMemory",
                timestamp=time.time(),
                corollary=["monitor_streetgang_migration"]
            )
            npc.mind.add_thought(thought)
            npc.mind.remove_thought_by_content("No focus")
        return

    # Handle street gang logic
    if npc.region.turf_war_triggered:
        #both memoey and RegionKnowledge marked as not defined here now. What is memory here?
        #maybe this new block is more hassle than it is worth?

        memory = npc.mind.memory.semantic
        for region_knowledge in memory.get("region_knowledge", []):
            
            if not isinstance(region_knowledge, RegionKnowledge):
                print(f"[BUG] Non-RegionKnowledge in memory: {region_knowledge}")
                continue

            for gang in region_knowledge.region_gangs:
                if gang in my_faction.enemies:
                    npc.faction.increase_violence(1)  # Optional: have cooldown or limit per cycle

                    thought = Thought(
                        content=f"Turf war active in {region_knowledge.name}. Our enemies ({gang.name}) are involved.",
                        origin=gang.name,
                        urgency=7,
                        tags=["turf_war", "gang_conflict", "enemies"],
                        source="SemanticMemory",
                        timestamp=time.time(),
                        corollary=["monitor_streetgang_migration"]
                    )
                    npc.mind.add_thought(thought)
                    npc.mind.remove_thought_by_content("No focus")
                    npc.is_alert = True

                    # ShareKnowledge up chain
                    if npc.role == "GangMember":
                        npc.share_knowledge_with_faction_rank("Captain", tags=["turf_war"])
                    elif npc.role == "Captain":
                        npc.share_knowledge_with_faction_rank("Boss", tags=["turf_war"])

#possibly rename to override UtilitAI function
def gang_observation_logic(
    npc,
    region,
    content=None,
    subject=None,
    origin=None,
    urgency=1,
    source=None,
    weight=1.0,
    timestamp=None,
    resolved=False,
    corollary=None
):#called from handle_observation(self, region), so put a gang twist on observations
#not sure if this func will be called automatically to appraise rival factions, or on a triggered in code when a rival 
# faction does something. Maybe both? Thought can be update or have corollories?
    #for gang in game_state.gangs and npc.faction.name not :

        appraise_rival = Thought(
            content="So, they are xyz",
            subject=subject,
            origin=region.name,
            urgency=urgency or 10,
            tags=["compete", "danger", "gang"],
            source="Observation",
            weight = weight or 10, # How impactful (can be salience or derived)
            timestamp=time.time(),
            resolved = resolved,
            corollary = corollary or []
        )
        #npc.mind.memory.semantic.setdefault("enemies", []).append(appraise_rival)
        #old call
        npc.mind.add_thought_to_enemies(appraise_rival) #new call
        
        if hasattr(npc, 'utility_ai'):
            npc.utility_ai.evaluate_thought_for_threats(appraise_rival)

def has_tag(obj, tag):
        return hasattr(obj, "inventory") and hasattr(obj.inventory, "tags") and tag in obj.inventory.tags