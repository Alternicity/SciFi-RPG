#ai_gang.py
import time
from ai_utility import UtilityAI
from worldQueries import get_viable_robbery_targets
from npc_actions import steal_auto, rob_auto, idle_auto, visit_location_auto
from character_thought import Thought
from worldQueries import get_viable_robbery_targets, get_region_knowledge
from motivation import Motivation
from summary_utils import summarize_motivations_and_percepts
import random
from city_vars import GameState
from create_game_state import get_game_state
from memory_entry import RegionKnowledge
from character_think_utils import promote_relevant_thoughts, should_promote_thought
#from character_memory import Memory
from salience import compute_salience
from anchor_utils import Anchor, create_anchor_from_motivation

class BossAI(UtilityAI):
    def think(self, region):
        rk = get_region_knowledge(self.mind.memory.semantic, region.name)
        if rk:
            evaluate_turf_war_status(self.npc, observed_region=rk)
        self.promote_thoughts()

class GangCaptainAI(UtilityAI):
    def think(self, region):
        rk = get_region_knowledge(self.mind.memory.semantic, region.name)
        if rk:
            evaluate_turf_war_status(self.npc, observed_region=rk)

        self.promote_thoughts()

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

        if npc.isTestNPC and not npc.attention_focus:
            print(f"[GANG] {npc.name} did not promote any thoughts this cycle.")

    #For AI Subclasses that need special behavior, override this method only
    def compute_salience_for_motivation(self, percept, motivation):
        return compute_salience(percept, self.npc, create_anchor_from_motivation(motivation))

    def choose_action(self, region):
        top_motivation = self.npc.motivation_manager.get_highest_priority_motivation()
        if top_motivation and top_motivation.type == "rob":
            return self.resolve_robbery_action(region)
        if top_motivation == "steal":
            #if top_motivation and top_motivation.type == "steal":  ?
            return self.resolve_steal_action(region)

        percepts = self.npc.get_percepts()

        # Compute contextual salience
        anchor = create_anchor_from_motivation(top_motivation)

        if percepts:
            print(f"[DEBUG] Percepts: {percepts}")
            print(f"[DEBUG] First percept: {percepts[0]} (type: {type(percepts[0])})")
        else:
            print("[DEBUG] Noo percepts found.")

        scored = [(p, compute_salience(p["data"], self.npc, anchor)) for p in percepts]


        if scored:
            top_percept, score = scored[0]
            print(f"[SALIENT] Most salient percept for anchor '{anchor.name}' is: {top_percept['data'].get('name')} (score: {score:.2f})")
           
            if "weapon" in top_percept["data"].get("tags", []):
                weapon = top_percept["origin"]
                return {"name": "steal", "params": {"item": weapon.name}}
        else:
            print(f"[AI] {self.npc.name} found no percepts worth acting on.")

        # Step 2: Memory fallback
        known_weapon_locations = self.npc.mind.memory.query_memory_by_tags(["weapon", "shop"])
        print(f"[DEBUG] Known weapon locations: {known_weapon_locations}")

        if known_weapon_locations:
            memory = known_weapon_locations[0]
            location = memory.source
            if location:
                print(f"[AI] {self.npc.name} remembers a shop with weapons: {location}")
                return {"name": "visit_location", "params": {"location": location}}

        # Step 3: Spawn a thought and wait
        motivation = self.npc.motivation_manager.get_highest_priority_motivation()
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
        self.npc.mind.add_thought(new_thought)
        print(f"[THOUGHT] {self.npc.name} had a new thought: {new_thought.content}")

        self.npc.attention_focus = new_thought
        self.npc.motivation_manager.update_motivations("rob", urgency=1.1, source=new_thought)
        print(f"[AI] {self.npc.name} choosing action. Primary motivation: {top_motivation}")
        self.npc.ai.promote_thoughts()
        print(f"[POST-THOUGHT] Thoughts: {[t.summary() for t in self.npc.mind.thoughts]}")
        return {"name": "Idle"}

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

        action_func = action_map.get(name)
        if action_func:
            action_func(npc, region, **params)
        else:
            print(f"[GangMemberAI] Unknown action name: {name}")

        if npc.is_test_npc:
            print(f"[MIND DUMP] from GangMemberAI execute_action {npc.name} current thoughts: {[str(t) for t in npc.mind]}")

    def resolve_weapon_target_from_percepts(self):
        percepts = self.npc.get_percepts()
        anchor = Anchor(name="obtain_ranged_weapon", type="motivation", weight=1.5)
        scored = [(p, compute_salience(p["data"], anchor, observer=self.npc)) for p in percepts]
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
                #You don’t need to return an action here — just populate memory/thoughts. 
                # The action will be chosen later from context.
        #get percepts. Can the npc perceive a target location with a targetteable weapons?

    def resolve_weapon_target_from_memory(self):
        npc = self.npc
        memories = npc.mind.memory.semantic.get("region_knowledge", [])

        for memory in memories:
            if not isinstance(memory, RegionKnowledge):
                continue
            if memory.region_name != npc.region.name:
                continue

            for loc_name in memory.locations or []:
                loc = npc.region.get_location_by_name(loc_name)
                if not loc or not getattr(loc, "contains_weapons", False):
                    continue

                thought = Thought(
                    content=f"I remember {loc.name} has weapons. I could go there.",
                    subject=loc.name,
                    origin="resolve_weapon_target_from_memory",
                    urgency=6,
                    tags=["weapon", "shop", "memory", "visit"],
                    timestamp=time.time(),
                    source=memory,
                )
                # Future: Consider setting attention_focus = Anchor(...) or Location itself
                npc.mind.add_thought(thought)
                npc.attention_focus = thought
                print(f"[MEMORY] {npc.name} thought of visiting {loc.name} for weapons.")
                return  # Exit after the first valid location

        # If nothing found, optionally fallback to a lower-level motivation
        print(f"[MEMORY] {npc.name} found no weapon-related locations in memory.")

            #spawn a thought that spawns a semanitc memory search for target locations with weapons

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

        if self.npc.isTestNPC:
            print(f"\n--- from GangMemberAI, {self.npc.name} is about to think ---")
            #print("\n" * 1)     
            print(f"{self.npc.name}:\n{summarize_motivations_and_percepts(self.npc)}")
            print("\n" * 1)

            region_knowledge = get_region_knowledge(self.npc.mind.memory.semantic, region.name)

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

        if not self.npc.mind.thoughts:

            idk_thought = Thought(
                subject="confusion",
                content="No focus",
                origin="GangMemberAI.think",
                urgency=0,
                tags=["confusion"]
            )

            self.npc.mind.add_thought(idk_thought)

        """ for memories in self.npc.mind.memory.semantic.values():
            for memory in memories:
                if "weapon" in memory.tags:
                    self.npc.mind.add(
                        Thought(
                            content=f"Scored memory: {memory.description}",
                            origin="semantic_memory",
                            urgency=8,
                            tags=memory.tags,
                            source=memory
                        )
                    ) """

        motivations = self.npc.motivation_manager.get_motivations()
        motivation_types = {m.type for m in motivations}

        # After gathering motivation
        motivation = self.npc.motivation_manager.get_highest_priority_motivation()

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

                    thought = Thought(
                        content=f"Maybe I should rob {loc_obj.name}.",
                        subject=loc_obj.name,
                        origin="RegionKnowledge",
                        urgency=7,
                        tags=["rob", "shop"],
                        timestamp=time.time()
                    )
                    self.npc.mind.add_thought(thought)

        anchor = create_anchor_from_motivation(motivation)

        relevant_thoughts = [
            t for t in self.npc.mind.thoughts
            if isinstance(t, Thought) and t.salience_for(self.npc, anchor=anchor) > 0
        ]
        salient_thoughts = sorted(relevant_thoughts, key=lambda t: t.salience_for(self.npc, anchor=anchor), reverse=True)
        #all salience is computed relative to an anchor
        high_salient = [t for t in salient_thoughts if t.salience_for(self.npc) >= 6]
        if salient_thoughts:
            top = salient_thoughts[0]
            print(f"[THINK] {self.npc.name} Top salient thought: '{top.content}' (score: {top.salience_for(self.npc):.2f})")


        for t in high_salient:
            score = t.salience_for(self.npc, anchor=anchor)
            print(f"[THINK] {self.npc.name} Salient thought: '{t.content}' (score: {score:.2f})")
            


        self.npc.attention_focus = salient_thoughts[0] if salient_thoughts else None

        if self.npc.is_test_npc:
            print(f"[MIND DUMP] {self.npc.name} current thoughts: {[str(t) for t in self.npc.mind]}")

        episodic_memories = self.npc.mind.get_episodic()
        self.examine_episodic_memory(episodic_memories)
        self.generate_thoughts_from_percepts()
        self.promote_thoughts()#deprecated? below we have promote_relevant_thoughts

        npc = self.npc
        thoughts = npc.mind.thoughts #thoughts currently not accessed
        promoted = set()# promoted currently not accessed

        promote_relevant_thoughts(npc, self.npc.mind.thoughts)


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