#ai_gang.py
import time
from ai.ai_utility import UtilityAI
from actions.npc_actions import steal_auto, rob_auto
from character_thought import Thought
from worldQueries import get_region_knowledge
from create.create_game_state import get_game_state
from character_thought import Thought
from memory.memory_entry import RegionKnowledge
from focus_utils import set_attention_focus, clear_attention_focus
from character_think_utils import promote_relevant_thoughts, should_promote_thought, debug_recent_thoughts

from anchors.anchor_utils import Anchor, create_anchor_from_motivation, ObtainWeaponAnchor, create_robbery_anchor, create_anchor_from_thought
from ai.ai_utils import encode_weapon_shop_memory
from debug_utils import debug_print
from weapons import Weapon
from ai.behaviour_roles import role, ROLE_PERMISSIONS
class BossAI(UtilityAI):
    def think(self, region):
        rk = get_region_knowledge(self.mind.memory.semantic, region.name)
        if rk:
            evaluate_turf_war_status(self.npc, observed_region=rk)
        #self.promote_thoughts()# Delete in favour of calling from simulate_hours() 
        self.npc.mind.remove_thought_by_content("No focus")

class GangCaptainAI(UtilityAI):
    def think(self, region):
        rk = get_region_knowledge(self.mind.memory.semantic, region.name)
        if rk:
            evaluate_turf_war_status(self.npc, observed_region=rk)

        #self.promote_thoughts()# Delete in favour of calling from simulate_hours()
        self.npc.mind.remove_thought_by_content("No focus")

    def choose_action(self, region):
        return

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

    def promote_thoughts(self): #promote thought to anchor
        
        super().promote_thoughts()#UtilityAI version called
        # now gang-specific logic if required (but keep guard!)...


        """ A ThoughtPromotionMixin is a nice pattern for later; it’s not urgent for Test Case 1.
        Keep polymorphic promote_thoughts() definitions (UtilityAI default + Gang override) but ensure central invocation.
        That gives both specialization and a single per-tick execution guarantee.
        """

        npc = self.npc
        to_remove = []

        if not ROLE_PERMISSIONS[role(npc)]["anchor_creation"]:
            return

        for thought in npc.mind.thoughts:
            if "intention" in thought.tags and "weapon" in thought.content.lower():
                anchor = Anchor(
                    name="obtain_ranged_weapon",
                    type="motivation",
                    weight=thought.urgency,
                    source=thought,
                    tags=thought.tags,
                    desired_tags = ["ranged_weapon"],
                    disfavored_tags = ["security"],
                    owner=npc
                    )#This will currently create this anchor for any thought with those tags. Ok for now I think
                debug_print(npc, f"[ANCHOR] Created anchor {anchor.name} target={getattr(anchor,'target',None)} source={type(getattr(anchor,'source',None)).__name__}", category="anchor")

                npc.motivation_manager.update_motivations(
                    anchor.name,
                    urgency=thought.urgency,
                    source=thought)
                debug_print(npc, f"[PROMOTE] {npc.name} reinforced '{anchor.name} via thought: '{thought.content}'", "MOTIVE")
                
                to_remove.append("No focus")
        for r in to_remove:
            npc.mind.remove_thought_by_content(r)

        if not npc.mind.attention_focus:
            urgent_thoughts = npc.mind.urgent(min_urgency=0.5)
            if urgent_thoughts:
                
                set_attention_focus(npc, thought=urgent_thoughts[0])
                debug_print(npc, f"[FOCUS] Attention set to most urgent thought: '{urgent_thoughts[0].content}'", "FOCUS")
            elif npc.current_anchor:
                
                set_attention_focus(npc, thought=npc.current_anchor.source)
                debug_print(npc, f"[FOCUS] Defaulting focus to anchor source: '{npc.current_anchor.name}'", "FOCUS")
                
                source_obj = npc.current_anchor.source
                label = getattr(source_obj, "content", getattr(source_obj, "name", str(source_obj)))
                debug_print(npc, f"[FOCUS] Attention set to: '{label}'", "FOCUS")

        debug_print(
            npc,
            f"[THOUGHTSS] {[t.content for t in npc.mind.thoughts]}",
            category="thought"
        )
    

    def iter_candidate_locations(self, region):
        """Return all candidate locations from memory or region knowledge."""
        npc = self.npc
        region_knowledge = npc.mind.memory.find_region_knowledge(region.name)
        semantic = npc.mind.memory.semantic

        candidates = set()

        if region_knowledge:
            candidates.update(region_knowledge.shops)
            candidates.update(region_knowledge.locations)

        for mem in semantic.get("shop_knowledge", []):
            if getattr(mem, "source", None):
                candidates.add(mem.source)

        # fallback: region.get_viable_robbery_targets()
        if hasattr(region, "get_viable_robbery_targets"):
            for loc in region.get_viable_robbery_targets():
                candidates.add(loc)

        return [loc for loc in region.locations if hasattr(loc, "tags")]

    def choose_action(self, region):
        npc = self.npc

        debug_print(npc, f"[CHECK] choose_action called for {npc.name}", category="decision")

        # Update percepts before scoring
        npc.perceive_current_location()

        # ✅ 1 — STEAL OVERRIDE CHECK (anchor-aware)
        debug_print(npc, "[TRACE] Entering STEAL OVERRIDE CHECK", "choice")

        # Highest motivation
        motivation = npc.motivation_manager.get_highest_priority_motivation()
        debug_print(npc, f"[TRACE] Highest motivation = {motivation}", "motive")

        # List weapon percepts
        for p in npc.percepts.values():
            tags = p["data"].get("tags", [])
            if "ranged_weapon" in tags:
                debug_print(npc,
                    f"[TRACE] Weapon percept detected: {p['data'].get('name')} tags={tags}",
                    "steal"
                )

        # Test weapon target resolver
        target = self.resolve_weapon_target_from_percepts()#line 196
        debug_print(npc, f"[TRACE] resolve_weapon_target_from_percepts() -> {target}", "steal")

        # Decision
        if motivation and motivation.type == "obtain_ranged_weapon":
            if isinstance(target, Weapon):
                debug_print(npc, f"[TRACE] STEAL OVERRIDE TRIGGERED: stealing {target.name}", "steal")
                return {"name": "steal", "params": {"item": target}}

        debug_print(npc, "[TRACE] Skipping steal override — NO target OR wrong top motivation", "steal")

        # ✅ ROB OVERRIDE CHECK (NPC)
        debug_print(npc, "[TRACE] Entering ROB OVERRIDE CHECK", "rob")

        has_gun = npc.inventory.has_ranged_weapon()

        # Conditions:
        #  1. Top motivation must be "rob"
        #  2. NPC must have a ranged weapon
        #  3. Current location must be robbable
        if motivation and motivation.type == "rob" and has_gun:
            if getattr(npc.location, "robbable", False):
                debug_print(
                    npc,
                    f"[TRACE] ROB OVERRIDE TRIGGERED: robbing {npc.location.name}",
                    "rob"
                )
                return {
                    "name": "rob",
                    "params": {"location": npc.location}
                }

        debug_print(npc, "[TRACE] Skipping rob override — conditions not met", "rob")

        # Ensure current anchor
        anchor = getattr(npc, "current_anchor", None)
        if not anchor and npc.mind.attention_focus:
            anchor = create_anchor_from_thought(npc, npc.mind.attention_focus)

            #deprecated in UtilityAI
            #debug_print(npc, f"[ANCHOR] Created from attention focus: {anchor.name}", category="anchor")
        elif not anchor:
            motive = npc.motivation_manager.get_highest_priority_motivation()
            if motive:
                anchor = create_anchor_from_motivation(npc, motive)
                
                #deprecated in UtilityAI
                #debug_print(npc, f"[ANCHOR] Created from motivation: {anchor.name}", category="anchor")

        npc.current_anchor = anchor
        
        # Gather candidate locations
        candidates = self.iter_candidate_locations(region)
        if not candidates:
            debug_print(npc, "[CANDIDATES] No candidate locations found! Idling.", category="decision")
            return {"name": "idle", "params": {}}

        # Score each candidate
        scored = []
        for loc in candidates:
            if hasattr(loc, "get_percept_data"):
                data = loc.get_percept_data(observer=npc)
            else:
                data = {"tags": getattr(loc, "tags", []), "object": loc, "name": getattr(loc, "name", str(loc))}

            sal = 0.0
            if anchor and hasattr(anchor, "compute_salience_for"):
                sal = anchor.compute_salience_for(data, npc)

            scored.append((loc, sal))


        if not scored:
            debug_print(npc,
        "[DECISION] No scored candidates found in choose_action(); defaulting to idle.",
        category="decision"
    )
            return {"name": "idle", "params": {}}

        # Select best candidate
        best_loc, best_score = max(scored, key=lambda x: x[1])
        debug_print(npc, f"[DECISION] Best target: {best_loc.name} ({best_score})", category="decision")#line 256

        # Spawn thought and decide to act
        motivation = npc.motivation_manager.get_highest_priority_motivation()
        if motivation and motivation.type not in ("visit", "obtain_ranged_weapon"):
            suppress_visit_or_rob = True
        else:
            suppress_visit_or_rob = False

        allowed_to_visit = ROLE_PERMISSIONS[role(npc)].get("visit", False)

        if (#secondary GangMembers must be re allowed to visit
            allowed_to_visit
            and not suppress_visit_or_rob
            and npc.location != best_loc
        ):
            # spawn the thought
            # --- Prevent useless "visit/rob" thoughts after obtaining weapon or if already at target ---
            if npc.inventory.has_ranged_weapon() or npc.location == best_loc:
                pass  # Skip spawning thought
            else:
                new_thought = Thought(
                    subject=npc.name,
                    content=f"Should visit or rob {best_loc.name}",
                    origin="salience_evaluation",
                    urgency=3,
                    tags=["visit", "robbery_target"],
                    source=best_loc,
                    weight=best_score
                )
                npc.mind.add_thought(new_thought)
                #Later, once Test Case 1 is complete, I can refactor “thought spawning” into a unified helper.

        # Decide on action
        debug_print(
            npc,
            f"[DECISION TRACE] Choosing to visit {best_loc.name} (score={best_score:.2f}) "
            f"due to motivation '{motivation}'",
            category="decision"
        )

        #Stop re-visiting the same location
        if npc.location == best_loc:
            debug_print(npc, f"[DECISION] Stop re-visiting the same location block triggered ({best_loc})", category="decision")
            return {"name": "idle", "params": {}}

        if best_score > 0.3:
            return {"name": "visit_location", "params": {"destination": best_loc}}
        else:
            debug_print(
                npc,
                f"[DECISION] Idling because best_score={best_score:.2f} (target={best_loc.name}) "
                f"below threshold (0.5).",
                category="decision"
            )
            return {"name": "idle", "params": {}}

    def execute_action(self, action, region):
        npc = self.npc 

        if not isinstance(action, dict):
            print(f"[ERROR] From GangmemberAI Action must be a dict, got: {action}")
            return
                
        name = action.get("name", "").lower()

        debug_print(
            npc,
            f"[EXECUTE TRACE] Executing action='{name}' with params={action.get('params')}",
            category="action"
        )

        if name in ["rob", "steal"]:
            # Keep domain-specific behavior local
            action_map = {"rob": rob_auto, "steal": steal_auto}
            func = action_map.get(name)
            if func:
                return func(npc, region, **action.get("params", {}))
        else:
            # Delegate all generic actions
            #debug_print(npc, f"[ACTION] {npc.name} execute_action {params}", category="action")
            return super().execute_action(action, region)

            

    def generate_location_visit_thought(npc, location, enabling_motivation=None):
        """
        Creates a thought suggesting visiting a specific location to satisfy a motivation, GangMember edition
        """
        debug_print(npc, f"[THINK] Generating thought to visit {location.name} GangMember version", category="think")
        #this print does not show up in current output
        tags = []
        reason = []

        if hasattr(location, "tags"):
            tags.extend(location.tags)
        if getattr(location, "robbable", False):
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
            tags=tags + ["location", "move", "travel", "intention"],
            source=enabling_motivation,
            weight=6
        )

        npc.mind.add_thought(thought)

        # Optional: Remove “No focus” placeholder
        npc.mind.remove_thought_by_content("No focus")

        return thought
    
    def resolve_visit_action(self, region):
        npc = self.npc
        # Try to use a remembered location with "weapon" or "shop" tags

        #GATE
        if not ROLE_PERMISSIONS[role(npc)].get("visit", False):
            return None

        for thought in npc.mind.thoughts:
            if "visit" in thought.tags and ("weapon" in thought.tags or "shop" in thought.tags):
                location_name = thought.subject if isinstance(thought.subject, str) else None
                location = region.get_location_by_name(location_name)#here
                if location:
                    debug_print(npc, f"[VISIT RESOLVE] Decided to visit {location.name} from thought {thought.content}", category="decision")
                    npc.current_destination = location
                    return {"name": "visit_location", "params": {"destination": location}}

        debug_print(npc, f"[VISIT RESOLVE] No valid visit target found, defaulting to idle", category="decision")
        return {"name": "idle", "params": {}}

    def resolve_weapon_target_from_percepts(self):

        npc=self.npc
        # 🚫 ROLE GATE: background / non-criminal NPCs do not reason about weapons
        if not ROLE_PERMISSIONS[role(npc)]["weapon_reasoning"]:
            return None

        percepts = self.npc.get_percepts()
        location =self.npc.location
        #get a weapon target from weapon objects at npcs current location
        #this function should also contain stub code pertaining to multiple weapon choices, ie if a future npc
        #is in an armoury with several perceivable weapon types, or a shop with several.

        scored = []
        for p in percepts:
            data = p.get("data", {})
            tags = data.get("tags", [])

            # ✅ Only accept ranged weapons
            if "ranged_weapon" not in tags:
                continue
            if "location" in tags:
                continue
            origin = data.get("object") or p.get("origin")
            if not origin:
                continue


            if self.npc.inventory.has_item(getattr(origin, "name", "")):
                continue  # skip duplicates

            scored.append((p, 1.0))  # simple relevance; salience via anchors later

        if not scored:
            return

        top_percept, _ = scored[0]

        data = top_percept.get("data", {})
        origin = data.get("object") or top_percept.get("origin")

        if not isinstance(origin, Weapon):
            debug_print(
                self.npc,
                f"[TRACE] Rejected steal target — origin not Weapon: {type(origin).__name__}",
                "action"
            )
            return None

        content = f"I saw a weapon at {location.name}"#this and below code should stay
        
        if not self.npc.mind.has_thought_content(content):
            
            new_thought = Thought(
                content=content,
                subject=location.name,
                origin="percept",
                urgency=4,
                tags=["ranged_weapon", "shop", "target", "criminal", "test_case_1"],
                source=origin,
            )
            self.npc.mind.add_thought(new_thought)
            #Will this just create a thought object called new_thought? If so should we use a more decriptive name?
            #or is this just a local variable?
            self.npc.mind.remove_thought_by_content("No focus")

        from ai.ai_utils import encode_weapon_shop_memory
        memory_entry = encode_weapon_shop_memory(self.npc, location)


        if npc.debug_role == "primary":
            debug_print(
                npc,
                f"Added memory: {location.name} sells weapons",
                category="memory"
            ) 
            self.npc.mind.memory.add_semantic_unique(
            "shop_knowledge", memory_entry, dedupe_key="details"
        )
        return origin
            

    @staticmethod
    def has_shop_weapon_memory(npc, location) -> bool:
        """
        Check if NPC remembers this location as selling ranged weapons.
        Works with both legacy and generic semantic memory entries.
        """
        if not hasattr(npc, "mind") or not hasattr(npc.mind, "memory"):
            raise TypeError(f"Expected NPC with mind, got {type(npc).__name__}: {npc}")

        for mem in npc.mind.memory.semantic.get("shop_knowledge", []):
            # Generic check using tags + location name
            if (
                getattr(mem, "object_", None) == location.name
                and any(tag in mem.tags for tag in ["weapon", "ranged_weapon", "shop"])
            ):
                from debug_utils import debug_print
                debug_print(npc, f"Recalled weapon shop: {location.name}", category="memory")
                return True

        return False
    #Eventually this could merge KnownWeaponLocationMemory entries too, ie is shop, and police known weapon locations
    #memory entries exist, replace them with a KnownWeaponLocations one.
    
    #A parallel system for thought objects could take mutliple specific thoughts, and replace them with a general one

    def resolve_weapon_target_from_memory(self):
        npc = self.npc
        found_any = False 

        # Iterate over remembered regions
        for knowledge in npc.mind.memory.semantic.get("region_knowledge", []):
            if not isinstance(knowledge, RegionKnowledge):
                continue
            if knowledge.region_name != npc.region.name:
                continue

            # Loop through known locations in this region
            for loc_name in knowledge.locations:
                location = npc.region.get_location_by_name(loc_name)
                if not location:
                    continue

                # Skip if already armed
                if npc.inventory.has_ranged_weapon():
                    
                    debug_print(npc, f"{npc.name} already has a ranged weapon. Skipping search.", "DEBUG")
                    return  

                # Skip if location doesn’t sell weapons
                if not any(obj.has_tag("ranged_weapon") for obj in location.inventory.items.values()):
                    continue

                # Skip if already remembered this shop
                if GangMemberAI.has_shop_weapon_memory(npc, location):
                    found_any = True
                    continue

                # Encode a new semantic memory of this shop
                memory_entry = encode_weapon_shop_memory(npc, location)
                npc.mind.memory.add_semantic_unique("shop_knowledge", memory_entry, dedupe_key="details")

                #do we need to define location here first?
                if not npc.mind.has_thought_content(f"I remember {location.name} sells weapons."):

                    # Form a thought about recalling it
                    thought = Thought(
                        content=f"I remember {location.name} sells weapons.",
                        subject=location.name,
                        origin="memory",
                        urgency=6,
                        tags=["weapon", "shop", "memory", "visit", "ranged_weapon"],
                        source=location,
                    )
                    npc.mind.add_thought(thought)

                # Update motivations via manager
                npc.motivation_manager.update_motivations(
                    "visit",
                    urgency=12,
                    source="obtain_ranged_weapon",
                )

                # Focus NPC’s attention on this recalled location
                #npc.mind.attention_focus = set_attention_focus(npc, thought)
                set_attention_focus(npc, anchor=None, thought=thought, character=None)

                npc.mind.remove_thought_by_content("No focus")

                debug_print(
                    npc,
                    f"[MEMORY→MOTIVATION] {npc.name} recalled {location.name} sells weapons and formed a 'visit' motivation (urgency 12).",
                    "DEBUG",
                )

                found_any = True
                break  # Stop after first valid shop

        if not found_any:
            debug_print(npc, f"[MEMORY] {npc.name} found no weapon-selling shops in memory. Setting exploration motive.", "MEMORY")
            npc.motivation_manager.update_motivations("explore", urgency=4, source="memory_scan")
    
    def resolve_obtain_weapon_target(self, region):#line 578
        action = self.resolve_weapon_target_from_percepts()
        if action: 
            return action
        action = self.resolve_weapon_target_from_memory()
        if action:
            return action
            if not action:
                debug_print(npc,
                    "[RESOLVE] resolve_obtain_weapon_target(): No weapon target from percepts or memory; idling.",
                    category="resolve"
                )
        return {"name": "idle", "params": {}}#returns an action

    def debug_percepts(npc, context=""):
        print(f"\n--- [PERCEPT DEBUG] {npc.name} ({context}) ---")
        for p in npc.get_percepts():
            d = p.get("data", {})
            print(f"→ {d.get('type')} | {d.get('name')} | tags: {d.get('tags')} | salience: {p.get('salience')}")

    def resolve_robbery_action(self, region):
        npc = self.npc

        if not npc.inventory.has_ranged_weapon():

            if not npc.mind.has_thought_content("Maybe I should get a weapon before robbing."):
                
                new_thought = Thought(
                    subject="ranged_weapon",
                    content="Maybe I should get a weapon before robbing.",
                    origin="resolve_robbery_action",
                    urgency=7,
                    tags=["rob", "shop", "weapon", "enable", "crime", "ranged_weapon", "pistol", "intention"],
                    timestamp=time.time(),
                    source=None,
                    weight=7
                )
                npc.mind.add_thought(new_thought)
                set_attention_focus(npc, anchor=None, thought=new_thought, character=None)
                npc.mind.remove_thought_by_content("No focus")

                self.promote_thoughts()# Delete in favour of calling from simulate_hours()

                return self.resolve_obtain_weapon_target(region)#what!?

        # Are we in a robbable location?
        if npc.location and getattr(npc.location, "robbable", False):
            return {"name": "Rob", "params": {"location": npc.location}}

        # Else: No robbable location or still lacking weapon
        return {"name": "idle", "params": {}}

    def think(self, region):
        npc = self.npc
        mind = npc.mind
        motives = npc.motivation_manager

        if getattr(npc, "debug_role", None) != "primary":
            return

        game_state = get_game_state()
        
        current_tick = getattr(game_state, "tick", None)
        current_day = getattr(game_state, "day", None)
        #we must access game_state via its getter, so are these getattr() calls correct?

        debug_print(npc, f"[PRE-THINK] ====== DAY {current_day}, TICK {current_tick} — THINK CYCLE START for {npc.name} ======", category ="think")
        debug_print(npc, f"[STATE] Location: {npc.location.name if npc.location else 'Unknown'} | Region: {region.name}", "state")
        debug_print(
                npc,
                f"[MOTIVE] Current motivations: {npc.motivation_manager.get_motivations_display()}",
                "motive"
            )
        debug_print(npc, f"[FOCUS] Current focus: {getattr(mind.attention_focus, 'content', None)}", "focus")#what good does this do here?

        try:
            ranged_weapons = [
                p["origin"] for p in npc.percepts.values()
                if "ranged_weapon" in p.get("data", {}).get("tags", [])
            ]
        except Exception as e:
            ranged_weapons = []
            debug_print(npc, f"[ERROR] reading npc.percepts for ranged_weapons: {e}", category="ERROR")

        

        if ranged_weapons:
            #deprecated
            
            if not ROLE_PERMISSIONS[role(npc)]["anchor_creation"]:
                return

            #Later improvement: replace return with pass or continue once you split think() into sub-phases

            pistol = ranged_weapons[0]

            npc.motivation_manager.consider_adding_motivation(
                "obtain_ranged_weapon",
                urgency=25,
                target=pistol,
                source="percept"
            )

            # Deboost rivals so this becomes clearly dominant
            npc.motivation_manager.deboost_others("obtain_ranged_weapon", amount=5)


        if npc.just_arrived:
            npc.observe(location=npc.location, region=npc.region)#does this need to be here?
        #neither of these prints are in the current output
            try:
                self.generate_thoughts_from_percepts()#Is this actually working well?
                debug_print(
                    npc,
                    f"[ARRIVAL] After thought-gen: {[t.content for t in npc.mind.thoughts][-5:]}",
                    category="think"
                )
            except Exception as e:
                debug_print(
                    npc,
                    f"[ERROR] generate_thoughts_from_percepts() failed on arrival: {e}",
                    category="error"
                )

            #refresh salience for the current anchor (if any)
            from anchors.anchor_utils import refresh_salience_for_anchor
            try:
                refresh_salience_for_anchor(npc)
            except Exception as e:
                debug_print(
                    npc,
                    f"[ERROR] refresh_salience_for_anchor() failed on arrival: {e}",
                    category="ERROR"
                )

                # Deboost rivals
                npc.motivation_manager.deboost_others("obtain_ranged_weapon", amount=5)

                debug_print(npc, f"[STEAL] Weapon seen — obtain_ranged_weapon set to 25, target={pistol.name}", "steal")

                if not npc.mind.has_thought_content("Now that I'm armed, I could rob"):
                    npc.mind.add_thought(Thought(
                        subject="robbery",
                        content="Now that I'm armed, I could rob this shop.",
                        origin="episodic_enable",
                        urgency=9,
                        tags=["rob", "crime", "weapon", "intention"]
                    ))
                    #npc.mind.attention_focus = set_attention_focus(npc, npc.mind.thoughts[-1])
                    if npc.mind.thoughts:
                        set_attention_focus(npc, anchor=None, thought=npc.mind.thoughts[-1], character=None)
                #break
                #this break doesnt fit right any more at any indentation so I commented it

            npc.just_arrived = False

            # Episodic enablement: check if the NPC recently stole a ranged weapon
            episodics = npc.mind.get_episodic()
            for mem in episodics:
                if "theft" in getattr(mem, "tags", []) and "ranged_weapon" in getattr(mem, "tags", []):
                    # Post-theft flow: clean up obsolete motives & create post-theft robbery thought
                    npc.motivation_manager.remove_motivation("obtain_ranged_weapon")
                    npc.motivation_manager.remove_motivation("visit")
                    npc.mind.remove_thoughts_with_tag("visit")
                    npc.mind.remove_thoughts_with_tag("obtain_ranged_weapon")
                    npc.mind.remove_thoughts_with_tag("robbery_prereq")

            # If a ranged weapon is present in inventory, remove only visit-related motivations/thoughts.
            if npc.inventory.has_ranged_weapon():
                npc.motivation_manager.remove_motivation("visit")
                # remove any stale visit/obtain_ranged_weapon thoughts but DO NOT remove 'steal' or existing theft memories.
                npc.mind.remove_thoughts_with_tag("visit")#duplicate command
                npc.mind.remove_thoughts_with_tag("obtain_ranged_weapon")#duplicate command
                npc.motivation_manager.remove_motivation("obtain_ranged_weapon")
                npc.motivation_manager.update_motivations("rob", urgency=20)
                npc.motivation_manager.deboost_others("rob", amount=7)

                # ensure a robbery motive exists and is prominent
                if npc.motivation_manager.has_motivation("rob"):#we know this exists
                    npc.motivation_manager.boost("rob", amount=10)#We just called update_motivations a few lines above

                # Also remove pre-theft "Should visit or rob XYZ"
                npc.mind.remove_thought_by_predicate(
                    lambda t: "visit" in t.tags or "steal" in t.tags
                )

                # Add new post-theft robbery thought (if not present)
                if not npc.mind.has_thought_content("Now that I'm armed"):
                    rob_thought = Thought(
                        subject="robbery",
                        content="Now that I'm armed, I can rob this shop.",
                        origin="post_theft",
                        urgency=8,
                        tags=["rob", "crime", "weapon", "opportunity"],
                        timestamp=time.time()
                    )
                    npc.mind.add_thought(rob_thought)
                    
                    set_attention_focus(npc, anchor=None, thought=rob_thought, character=None)
                #. Ensure robbery motivation is active
                npc.motivation_manager.boost("rob", amount=5)

                #. Ensure rob becomes top anchor pathway
                npc.current_anchor = create_robbery_anchor(npc)


                npc.motivation_manager.remove_motivation("visit")
                npc.mind.remove_thoughts_with_tag("visit")

        # INITIAL DEBUG / CONTEXT DUMP

        region_knowledge = get_region_knowledge(npc.mind.memory.semantic, region.name)
        if npc.debug_role == "primary":
            if region_knowledge:
                shops = ", ".join(region_knowledge.shops) or "No shops listed"
                debug_print(npc, f"[RK] Shops in {region.name}: {shops}", category="rkprint")
            else:
                debug_print(npc, f"[RK] No region knowledge for {region.name}", category="rkprint")

        if region_knowledge and getattr(npc, "is_gang_member", True):
            evaluate_turf_war_status(npc, observed_region=region_knowledge)


        # CREATE ROBBERY-RELATED THOUGHTS FROM MEMORY

        for category, memories in npc.mind.memory.semantic.items():
            if not isinstance(memories, list):
                continue

            for memory in memories:
                if not hasattr(memory, 'tags'):
                    print(f"[ERROR] Invalid memory object: {memory} (type: {type(memory)})")
                    continue
                if "weapon" in memory.tags:
                    thought = Thought(
                        content="Target spotted for robbery",
                        subject=None,
                        origin="ai_gang.robbery_decision",
                        tags=["robbery", "shop", "weapon", "intention"],
                        urgency=3,
                        timestamp=time.time()
                    )
                    npc.mind.add_thought(thought)

        if not npc.mind.thoughts:#is this worth keeping? Wouldnt a confusion print be more useful?
            npc.mind.add_thought(Thought(
                subject="confusion",
                content="No focus",
                origin="GangMemberAI.think",
                urgency=0,
                tags=["confusion"]
            ))

        # DETERMINE HIGHEST PRIORITY MOTIVATION

        motivation = motives.get_highest_priority_motivation()
        if not motivation:
            debug_print(npc, f"[THINK] No motivation found for {npc.name}", category="motive")
            return

        
        debug_print(npc, f"[MOTIVES] Active motivation: {motivation.type} (urgency={motivation.urgency})", category="motive")

        # CREATE ANCHOR FROM MOTIVATION

        anchor = create_anchor_from_motivation(npc, motivation)
        if anchor is None:
            debug_print(npc, f"[ANCHOR] No anchor could be created from {motivation}", "ERROR")
            return

        if not getattr(anchor, "tags", None):
            anchor.tags = getattr(motivation, "tags", [])
        npc.current_anchor = anchor
        
        set_attention_focus(npc, anchor=anchor, thought=None, character=None)
        debug_print(
            npc,
            f"Thinking about anchor: {anchor.name} (tags={anchor.tags})",
            category="anchor"
        )

        # THOUGHT URGENCY ADJUSTMENTS

        for thought in npc.mind.thoughts:
            if set(thought.tags) & set(anchor.tags):
                thought.urgency += 1
            else:
                thought.urgency = max(thought.urgency * 0.9, 0.5)

        # THOUGHT DRIVES MOTIVATION

        self.evaluate_thoughts()

        # MEMORY RECALL BASED ON ANCHOR TAGS
        if not anchor.tags:
            debug_print(npc, f"[MEMORY DEBUG] WARNING: anchor '{anchor.name}' has no tags — skipping query.", "memory")
        else:
            recalled_by_tags = npc.mind.memory.query_memory_by_tags(anchor.tags)
            if not recalled_by_tags:
                debug_print(npc, f"[RECALL] Anchor '{anchor.name}' found no tag-matching memories.", "memory")
            else:
                for m in recalled_by_tags:
                    desc = getattr(m, 'description', None) or getattr(m, 'details', 'Unknown memory')
                    debug_print(npc, f"[RECALL] Anchor '{anchor.name}' recalled: {desc}", "memory")

        # Also show which anchor the NPC is currently thinking through
        debug_print(npc, f"[ANCHOR DEBUG] Thinking about anchor: {anchor.name} (tags={anchor.tags})", "anchor")
        
        #SHAKEDOWN CHAIN
        if motivation.type == "shakedown":
            allow_visit = True

        # ROB CHAIN (only activates when rob is top motive) - does it?
        if motivation.type == "rob" and not npc.inventory.has_ranged_weapon():
            motives.consider_adding_motivation(
                "obtain_ranged_weapon",
                urgency=15,
                source="rob_chain",
            )
            

            if region_knowledge:
                for loc_name in region_knowledge.locations or set():
                    loc_obj = npc.region.get_location_by_name(loc_name)
                    if not loc_obj or not getattr(loc_obj, "robbable", False):
                        continue
                    if not mind.has_thought_content(f"Maybe I should rob {loc_obj.name}."):
                        thought = Thought(
                            content=f"Maybe I should rob {loc_obj.name}.",
                            subject=loc_obj.name,
                            origin="RegionKnowledge",
                            urgency=7,
                            tags=["rob", "shop", "intention"],
                            timestamp=time.time()
                        )
                        mind.add_thought(thought)

            existing_targets = [t for t in mind.thoughts if "rob" in t.tags and "store" in t.content.lower()]
            if len(existing_targets) > 1:
                debug_print(npc, f"[THINK] Multiple robbery target thoughts: {[t.content for t in existing_targets]}", category="think")
                """ a non-destructive diagnostic first step.
                Later, we could promote the second most salient one as a secondary anchor once the AI can plan ahead across ticks
                """

            if (npc.inventory_component.has_recently_acquired("ranged_weapon") 
                and npc.motivation_manager.has_motivation("rob")
                and not mind.has_thought_content("Now that I'm armed, I could rob this shop.")):
                thought = Thought(
                    subject="robbery",
                    content="Now that I'm armed, I could rob this shop.",
                    origin="post_theft",
                    urgency=8,
                    tags=["rob", "crime", "weapon", "opportunity", "intention"],
                    timestamp=time.time()
                )
                mind.add_thought(thought)
                set_attention_focus(npc, anchor=None, thought=thought, character=None)
        # PERTINENCE EVALUATION
        relevant_thoughts = [t for t in mind.thoughts if isinstance(t, Thought)]
        for t in relevant_thoughts:

            raw = t.salience_for(npc, anchor)
            # Ensure cache is ALWAYS numeric
            t._salience_cache = raw if isinstance(raw, (int, float)) else 0.0
            #This prevents None values from ever entering the sorter.

        pertinent_thoughts = sorted(relevant_thoughts, key=lambda t: getattr(t, "_salience_cache", 0), reverse=True)

        if pertinent_thoughts:#the word pertinent used here, to avoid confusion with object salience, in anchors.
            top = pertinent_thoughts[0]
            debug_print(
                npc,
                f"[THINK] Top pertinent thought: '{top.content}' (pertinence={top._salience_cache:.2f})",
                category="think"
            )
            
            set_attention_focus(npc, anchor=None, thought=top, character=None)
            new_anchor = create_anchor_from_thought(npc, top)

            if new_anchor:
                npc.current_anchor = new_anchor
                debug_print(npc, f"[ANCHOR SET] Current anchor is now {type(new_anchor).__name__}: '{new_anchor.name}'", category="anchor")

        # MEMORY REVIEW & PERCEPT THOUGHTS

        episodic_memories = mind.get_episodic()
        self.examine_episodic_memory(episodic_memories)
        high_pertinent = [t for t in pertinent_thoughts if t._salience_cache >= 6]
        if not high_pertinent:
            self.generate_thoughts_from_percepts()

        # FINAL PROMOTION AND STRUCTURING

        #self.promote_thoughts()# Delete in favour of calling from simulate_hours()
        promote_relevant_thoughts(npc, mind.thoughts)#omg what is this?


        # END OF THINK CYCLE LOGGING

        debug_print(
            npc,
            "====== THINK CYCLE END ======",
            category="think"
        )
        debug_print(
            npc,
            f"Focus: {getattr(mind.attention_focus, 'content', None)}",
            category="think"
        )

        debug_recent_thoughts(npc, mind)
        npc.mind.deduplicate_thoughts(npc)
        debug_print(
            npc,
            f"Inventory: {npc.inventory.get_inventory_summary()}",
            category="inventory"
        )

    def evaluate_thoughts(self):
        """Gang-specific thought evaluation: promotes robbery-related thoughts to motivations.
        iF YOU ADD LOGIC HERE UPDATE THE iNSTRUMENTATION HEADER IN THINK()"""

        """ Evaluating/promoting thoughts is a sub-step of cognition — conceptually part of thinking,
        but distinct enough to warrant its own function for clarity and testability. """
        #Eventually this should evolve into a utility-based appraisal. I think

        npc = self.npc
        
        if not ROLE_PERMISSIONS[role(npc)]["thought_to_motivation"]:
            return
        #with this secondaryGangMembers can think but not escalate that to new motivations


        for thought in list(npc.mind.thoughts):
            if getattr(thought, "resolved", False):
                continue
            if "rob" in thought.tags and "weapon" in thought.tags:#uses weapon, is that optimal? we have npc booleans we can look up
                debug_print(npc, f"[THOUGHT EVAL] {npc.name} is influenced by thought: {thought.content}", "think")
                npc.motivation_manager.increase("rob", amount=getattr(thought, "weight", 1))
                thought.resolved = True

    def resolve_steal_action(self, region):
            target = target = self.resolve_obtain_weapon_target(region)#no. work from percepts

            if target:

                return {
                    "name": "Steal",
                    "params": target.get("params", {}) #Or standardize format to return target  # if target is already in the correct {"name": ..., "params": ...} format
                }
            return {"name": "idle"}
    #put a debug_print here saying where this idle action came from
        
    def resolve_explore_action(self, region): 
            from location.locations import Shop
            target = self.resolve_obtain_weapon_target(region) #no longer in utility_ai
            if target:
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
            
            if not self.npc.mind.has_thought_content("Target spotted for robbery."):
                if target == Shop:
                    thought = Thought(
                        content=f"Target spotted for robbery",
                        subject=target,
                        origin="Memory",
                        tags=["explore", "shop", "intention"],
                        urgency=2,
                        timestamp=time.time()
                    )
                    self.npc.mind.add_thought(thought)
                    self.npc.mind.remove_thought_by_content("No focus")



#utilty functions, called from within gang character classes

""" Refactor evaluate_turf_war_status and similar character AI methods to rely
only on the agents perceived knowledge (via RegionKnowledge object), not global truths from Region """

#utility function
def evaluate_turf_war_status(npc, observed_region):
    """
    Turf war is flavour only right now. This creates ONE ambient intel thought,
    only when the region is in turf_war_triggered=True state.
    """

    # Only do anything if the region is actually in a turf war
    if not getattr(observed_region, "turf_war_triggered", False):
        return

    # Avoid duplicates
    if npc.mind.has_thought_content(f"Turf war active in region: {observed_region.name}."):
        return

    thought = Thought(
        subject="Turf war",
        content=f"Turf war active in region: {observed_region.name}. The homeless street gangs are desperate.",
        origin="Faction Intel",
        urgency=3,
        tags=["turf_war", "gang_conflict", "intel"],
        source="SemanticMemory",
        timestamp=time.time(),
    )

    npc.mind.add_thought(thought)

    # ShareKnowledge up chain
    if npc.role == "GangMember":
        npc.share_knowledge_with_faction_rank("Captain", tags=["turf_war"])
    elif npc.role == "Captain":
        npc.share_knowledge_with_faction_rank("Boss", tags=["turf_war"])

#possibly rename to override UtilityAI function
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