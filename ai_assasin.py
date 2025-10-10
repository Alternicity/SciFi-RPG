#ai_assasin.py
from time import time

from ai_utility import UtilityAI
from worldQueries import get_region_knowledge
from character_thought import Thought
from npc_actions import visit_location_auto
from character_thought import Thought
from anchor_utils import Anchor

class AssassinAI(UtilityAI):
    def __init__(self, npc):
        super().__init__(npc)
        self.visited_locations = set()
        self.current_region_index = 0
        self.search_complete = False

    def resolve_find_target(self, target_name="Karen"):
        npc = self.npc
        current_region = npc.region
        rk = get_region_knowledge(npc.mind.memory.semantic, current_region.name)

        if not rk:
            print(f"[AssassinAI] No region knowledge for {current_region.name}")
            return {"name": "idle", "params": {}}

        # Step 1: Check current location for target
        for char in npc.location.characters_there:
            if char.name == target_name:
                npc.mind.attention_focus = char
                print(f"[AssassinAI] Target {char.name} found at {npc.location.name}")
                return {"name": "target_acquired", "params": {"target": char}}

        # Step 2: Move through known locations in the region
        for loc in rk.locations:
            if loc.name not in self.visited_locations:
                self.visited_locations.add(loc.name)
                print(f"[AssassinAI] Visiting {loc.name} to search for {target_name}")
                return {"name": "visit_location", "params": {"location": loc}}

        # Step 3: Exhausted region locations, explore next region
        all_known_regions = list({mem.region_name for mems in npc.mind.memory.semantic.values() for mem in mems if hasattr(mem, "region_name")})

        if self.current_region_index < len(all_known_regions) - 1:
            self.current_region_index += 1
            next_region_name = all_known_regions[self.current_region_index]
            print(f"[AssassinAI] Switching to new region: {next_region_name}")
            return {"name": "travel_to_region", "params": {"region": next_region_name}}

        # Step 4: Entire map exhausted
        if not self.search_complete:
            thought = Thought(
                content=f"Could not find {target_name} anywhere...",
                origin="AssassinAI.resolve_find_target",
                urgency=5,
                tags=["search_failed"],
                timestamp=time.time()
            )
            npc.mind.add(thought)
            npc.motivation_manager.increase("search", -2)
            self.search_complete = True

        return {"name": "idle", "params": {}}
    
    #For AI Subclasses that need special behavior, override this method only
    def compute_salience_for_motivation(self, percept, motivation):
        # Create an anchor specific to the motivation or context
        anchor = Anchor(name="assassin_target", type="motivation", weight=motivation.urgency, tags=["assassin", "target_search"])
        #Do we need to ensure this anchor is stored in assassins current_anchor, not globally?
        return anchor.compute_salience_for(percept, self.npc)
        """ Notice how create_anchor_from_motivation(top_motivation) is used to define the anchor, and anchor drives
        subsequent behavior.
        So for all relevant actions, anchor.compute_salience_for() is how you'll calculate salience. """


        # Tweak or add special Assasin-specific logic
        """ if motivation.type == "rob":
            if percept.get("tags") and "gang_territory" in percept["tags"]:
                score += 0.3 """
        #MODEL LOGIC

    def think(self, region):
        npc = self.npc

        self.generate_thoughts_from_percepts()  # New: gain general awareness

        if not npc.mind.attention_focus:
            action = self.resolve_find_target("Karen")
            self.execute_action(action, region)

        
        self.promote_thoughts()  # Consider what's most urgent or interesting
        self.npc.mind.remove_thought_by_content("No focus")
        
    def execute_action(self, action, region):
        npc = self.npc
        name = action.get("name")
        params = action.get("params", {})

        if name == "visit_location":
            visit_location_auto(npc, params.get("location"))

        elif name == "target_acquired":
            print(f"[ACTION] {npc.name} has acquired target {params['target'].name}")
            # Placeholder for next step (attack, follow, etc.)

        elif name == "travel_to_region":
            # Placeholder for region transition logic
            print(f"[ACTION] {npc.name} would travel to region {params['region']}")

        else:
            print(f"[AssassinAI] No actionable behavior for {name}, idling...")

