#ai_gang.py
import time
from ai_utility import UtilityAI
from worldQueries import get_viable_robbery_targets
from npc_actions import steal_auto, rob_auto, idle_auto, visit_location_auto
from character_thought import Thought
from worldQueries import get_viable_robbery_targets
from motivation import Motivation
from summary_utils import summarize_motivations_and_percepts
import random
from city_vars import GameState
from create_game_state import get_game_state

class BossAI(UtilityAI):
    def think(self, region):
        evaluate_turf_war_status(self, self.memory.semantic)
        self.promote_thoughts()

class GangCaptainAI(UtilityAI):
    def think(self, region):
        evaluate_turf_war_status(self.npc, self.memory.semantic)
        self.promote_thoughts()

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
    def __init__(self, npc):
        super().__init__(npc)  # calls UtilityAI.__init__, which sets self.npc = npc
        
        
        """Custom salience tuning, override functions in UtilityAI
        Let UtilityAI produce options, and GangMemberAI choose from them based on gang-specific rules"""

    def choose_action(self, region):
        self.think(region)

        top_motivation = self.npc.motivation_manager.get_highest_priority_motivation()
        if top_motivation == "rob":
            return self.resolve_robbery_action(region)

        if top_motivation == "steal":
            return self.resolve_steal_action(region)

        if top_motivation == "placeholder":
            return self.resolve_explore_action(region) #hmmm, decision to visit_location doesnt come directly from a motivation
            #Starting confition of most urgent motivation is rob=8

        return {"name": "Idle"}

    def compute_salience(self, obj):
        from location import Shop, CorporateStore
        base = super().compute_salience(obj)

        if isinstance(obj, (Shop, CorporateStore)) and has_tag(obj, "weapon"):
            base += 5

        return base

    

    def execute_action(self, action, region):
        npc = self.npc #should this just be npc = self  ?

        if not isinstance(action, dict):
            print(f"[ERROR] Action must be a dict, got: {action}")
            return
                
        name = action.get("name")
        params = action.get("params", {})

        action_map = {
            "Rob": rob_auto,
            "Steal": steal_auto,
            "Visit": visit_location_auto,
            "Idle": idle_auto,
        }

        action_func = action_map.get(name)
        if action_func:
            action_func(npc, region, **params)
        else:
            print(f"[GangMemberAI] Unknown action name: {name}")

        if npc.is_test_npc:
            print(f"[MIND DUMP] from GangMemberAI execute_action {npc.name} current thoughts: {[str(t) for t in npc.mind]}")

    def think(self, region):
        self.npc.observe(region=region, location=self.npc.location)

        if self.npc.isTestNPC:
            print(f"\n--- from GangMemberAI, {self.npc.name} is about to think ---")
            #print("\n" * 1)     
            print(f"[Percepts Before Thinking] {self.npc.name}:\n{summarize_motivations_and_percepts(self.npc)}")
            print("\n" * 1)


        if self.npc.faction.is_street_gang == True:
            evaluate_turf_war_status(self.npc, self.npc.memory.semantic)

        for memory in self.npc.mind.semantic:
            if "weapon" in memory.tags or "weapons" in memory.description.lower():
                #this needs to detect or increase the salience of shops for robbery

                #this needs to detect the semantic memory 
                #<MemoryEntry: event_type='observation', target='None', description='Shops usually have weapons', tags=['weapon', 'shop'

                thought = f"I could rob a shop because: {memory.description}" #and because of the salience of shop for robbery, and them having weapons available
                self.npc.mind.thoughts.append(thought)
                #add salience robbing shops for weapons here

        if not self.npc.mind.thoughts:

            idk_thought = Thought(
                subject="confusion",
                content="I don't know what to do.",
                origin="GangMemberAI.think",
                urgency=1,
                tags=["confusion"]
            )

            self.npc.mind.add_thought(idk_thought)

        for memory in self.npc.mind.semantic:
            if "weapon" in memory.tags:
                self.npc.mind.add(
                    Thought(
                        content=f"Scored memory: {memory.description}",
                        origin="semantic_memory",
                        urgency=8,
                        tags=memory.tags,
                        source=memory
                    )
                )

        motivations = self.npc.motivation_manager.get_motivations()
        motivation_types = {m.type for m in motivations}

        relevant_thoughts = [
        t for t in self.npc.mind.thoughts if any(tag in motivation_types for tag in t.tags)
        ]


        salient_thoughts = sorted(relevant_thoughts, key=lambda t: t.compute_salience(self), reverse=True)
        #Would I then pass salient_thoughts into compute_salience from here, salient_thoughts is greyed out here, not accesed

        if self.npc.is_test_npc:
            print(f"[MIND DUMP] {self.npc.name} current thoughts: {[str(t) for t in self.npc.mind]}")
        print(f"[DEBUG] from def think in GangMemberAI {self.npc.name} thinking with {len(self.npc.memory.episodic)} episodic memories")
        print(f"From GangMember Attention focus: {self.npc.attention_focus}")

        # Use the shared logic
        self.promote_thoughts()
        #print(f"[DEBUG] From GangMemberAI def think {npc.name} current thoughts:")
        #npc not defined here, so commentedd out for now
        """ for thought in npc.mind:
            print(f" - {thought}") """

        """ print(f"{self.npc.name}'s thoughts after thinking:")
        for t in self.npc.mind:
            print(f" - {t}") """
        

    """ def custom_action_logic(self, region):
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

        return "Idle" """

    def promote_thoughts(self):
        super().promote_thoughts()

        npc = self.npc
        thoughts = npc.mind.thoughts
        promoted = set()

        tag_to_motivation = {
            "rob": "rob",
            "steal": "steal",
            "weapon": "obtain_ranged_weapon",
            # Add more mappings as needed
        }

        for thought in list(thoughts):
            if not isinstance(thought, Thought):
                continue

            for tag in thought.tags:
                if tag in tag_to_motivation:
                    motivation_type = tag_to_motivation[tag]
                    if thought.urgency >= 4:
                        motivation = Motivation(
                            motivation_type,
                            urgency=thought.urgency,
                            target=thought.source,
                            source=thought
                        )
                        npc.motivation_manager.update_motivations(
                            motivation_type,
                            motivation.urgency,
                            target=motivation.target,
                            source=thought
                        )
                        print(f"[GANG] {npc.name} promotes {motivation_type}: {motivation}")
                        promoted.add(motivation_type)

        if not promoted:
            print(f"[GANG] {npc.name} did not promote any thoughts this cycle.")


    def resolve_robbery_action(self, region):
        target = self.utility_ai.resolve_obtain_weapon_target(region)
        if target:
            return target  # May be 'steal' or 'visit_location'
        else:
            print("Idling from resolve_robbery_action: target not found")
            return {"name": "Idle"}
    
    def resolve_steal_action(self, region):
            target = self.utility_ai.resolve_obtain_weapon_target(region)
            if target:

                return {
                    "name": "Steal",
                    "target": target
                }
            return {"name": "Idle"}
        
    def resolve_explore_action(self, region): #decide to visit shop to rob, in current use
        # case, but also, decide to visit_location in general
            from location import Shop
            target = self.utility_ai.resolve_robbery_target(region)
            if target:
                self.npc.attention_focus = target
                self.npc.mind.add(Thought(
            content=f"Target spotted for robbery: {target.name}",
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
                    content=f"Perhaps I should check out {target.name}.",
                    origin="Memory",
                    tags=["explore", "shop"],
                    urgency=2,
                    timestamp=time.time()
                )
                self.npc.mind.add(thought)


#maybe explore a random location..emergent exploration:

                locations = [loc for loc in region.locations if isinstance(loc, Shop)]
                if locations:
                    loc = random.choice(region.locations)
                    self.npc.attention_focus = loc
                    return {
                        "name": "Visit",
                        "params": {"location": loc.name}
                    }

            return {"name": "Idle"}

game_state = get_game_state()

#utilty functions, called from within gang character classes
def evaluate_turf_war_status(npc, region_knowledge):
    
    my_faction = npc.faction

    if not my_faction.is_street_gang:
        if hasattr(region_knowledge, "region_gangs"):
            thought = Thought(
                content=f"Turf war active in region: {region_knowledge.name}. The homeless street gangs are desperate.",
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


def gang_observation_logic(npc, region): #A general function to handle gang characers observation of other gangs
#called from handle_observation(self, region), so put a gang twist on observations


    #for gang in game_state.gangs and npc.faction.name not :

        appraise_rival = Thought(
            content="So, they are xyz",
            origin=region.name,
            urgency=8,
            tags=["compete", "danger", "gang"],
            source="Observation",
            timestamp=time.time()
        )
        npc.mind.add(appraise_rival)
        if hasattr(npc, 'utility_ai'):
            npc.utility_ai.evaluate_thought_for_threats(appraise_rival)

def has_tag(obj, tag):
        return hasattr(obj, "inventory") and hasattr(obj.inventory, "tags") and tag in obj.inventory.tags