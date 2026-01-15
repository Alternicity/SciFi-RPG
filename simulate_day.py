# simulate_day.py
import random
from location.locations import Shop
from create.create_game_state import get_game_state
from ai.ai_utility import UtilityAI #not currently accessed
from ai.behaviour_roles import role
from events import Robbery
from characterActions import execute_action #not currently accessed
from summary_utils import format_location
from display import display_region_knowledge_summary, display_percepts_table, summarize_npc_turns, display_civ_worker, display_civ_waitress, display_civ_liberty, display_npc_vitals, summarize_action
from memory.memory_entry import RegionKnowledge
from memory.ambience_utils import update_ambient_scene_memory
from character_thought import Thought
from ambience.ambience_and_psy_utils import compute_location_ambience
from debug_utils import debug_print
from base.character import Character
from employment.employment import update_employee_presence

def simulate_hours(all_characters, num_days=1, debug_character=None):
    game_state = get_game_state()
    all_regions = game_state.all_regions
    all_locations = game_state.all_locations
    day = game_state.day

    for _ in range(num_days):
        game_state.advance_hour()
        debug_print(None, f"[TIME] Hour {game_state.hour}, Day {game_state.day}", category="tick")
        debug_print(None, summarize_npc_turns(all_characters), category="tick")
        for location in all_locations:
                    location.recent_arrivals.clear()

        # Each hour:
        for region in all_regions:
            for npc in region.characters_there:
                #npc._observed_this_tick = False
                begin_npc_turn(npc)
                update_employee_presence(npc, game_state.hour)
                if npc.is_player:
                    continue
                
                # OBSERVE
                npc.observe(region=region, location=npc.location)

                gs = get_game_state()
                
                if gs.day == 1 and gs.hour == 1:
                    if npc in gs.debug_npcs.values():
                        display_npc_vitals(npc)

                for effect in npc.effects[:]:
                    effect.on_tick(npc)
                    effect.remaining -= 1
                    if effect.remaining <= 0:
                        effect.on_end(npc)
                        npc.effects.remove(effect)

                if npc in gs.debug_npcs.values():
                    display_percepts_table(npc)#I wonder if effects will show up here via self percept

                # --- Ambience Influence + Social Vibe Logging ---
                #This framework sets the stage for scene-level emergent stories, largely un developed
                for loc in game_state.all_locations:
                    for char in getattr(loc, "characters_there", []):
                        if not hasattr(char, "mind") or not hasattr(char, "psy"):
                            continue

                        perceived = compute_location_ambience(loc, observer=char)
                        if not perceived:
                            continue

                        # 1. Add ambient thoughts
                        for tag, power in perceived.items():
                            if power > 0.1:
                                char.mind.add_thought(Thought(
                                    subject="Ambience",
                                    content=f"This place feels {tag}",
                                    urgency=round(power * 10),
                                    tags=["ambience", tag]
                                ))
                                npc.mind.remove_thought_by_content("No focus")

                        # 2. Log peak vibe
                        peak_tag, peak_power = max(perceived.items(), key=lambda x: x[1], default=("none", 0))

                        # 3. Capture social snapshot
                        #This logic also encapsulated as a func in social_utils
                        social = char.mind.memory.semantic.get("social")
                        if not social:
                            continue

                        friends_present = []
                        enemies_present = []
                        allies_present = []

                        for other in loc.characters_there:
                            if other is char:
                                continue

                            rel = social.get_relation(other)

                            if rel.current_type == "friend":
                                friends_present.append(other.name)
                            elif rel.current_type == "enemy":
                                enemies_present.append(other.name)
                            elif rel.current_type == "ally":
                                allies_present.append(other.name)

                        social_data = {
                            "friends_present": friends_present,
                            "enemies_present": enemies_present,
                            "allies_present": allies_present,
                        }


                        # 4. Save semantic ambient snapshot
                        if char.should_log_ambient_scene(loc, peak_tag, peak_power):
                            if char.should_log_ambient_scene(loc, peak_tag, peak_power):
                                update_ambient_scene_memory(
                                    char=char,
                                    loc=loc,
                                    perceived_ambience=perceived,
                                    peak_tag=peak_tag,
                                    peak_power=peak_power,
                                    social_data=social_data,
                                    current_day=game_state.day,
                                    current_hour=game_state.hour,
                                )
                


                # THINK CYCLE
                if hasattr(npc, 'ai') and npc.ai:
                    if role(npc) != "background":#GATE
                        think_loops = getattr(npc, "max_thinks_per_tick", 1)
                        for _ in range(think_loops):
                            npc.ai.think(npc.location.region)
                        npc.ai.promote_thoughts()

        # ✅ NEW: TC2 snapshot displays
        DISPLAY_BY_DEBUG_ROLE = {
            "civilian_worker": display_civ_worker,
            "civilian_liberty": display_civ_liberty,
            "civilian_waitress": display_civ_waitress,
        }

        for dbg_npc in gs.debug_npcs.values():
            if not dbg_npc:
                continue

            fn = DISPLAY_BY_DEBUG_ROLE.get(dbg_npc.debug_role)
            if fn:
                fn(dbg_npc)

                #At some point, ensure you're calling npc.inventory.clear_recently_acquired() somewhere in the tick loop
                    
        # STEP 2: Choose and Execute Action
        for npc in all_characters:
            if hasattr(npc, 'ai') and npc.ai:
                if role(npc) != "background":
                    npc.ai.evaluate_thoughts()
                    region = npc.location.region if hasattr(npc.location, 'region') else None
                    action = npc.ai.choose_action(region)
                    if action:
                        npc.ai.execute_action(action, region)

                    debug_print(
                        npc,
                        f"[ACTIONx] {npc.name} finished {summarize_action(action)}, "
                        f"current_location={npc.location.name}",
                        category="action"
                    )



        # STEP 3: Post-Day DEBUG (single character)
        for npc in all_characters:#ATTN
            end_npc_turn(npc)

            if npc is not debug_character:
                continue
            for mem in npc.mind.memory.episodic:
                pass

        debug_print(npc, f"[DEBUG] debug_character is: {debug_character.name} (id={id(debug_character)})", category="think")#ATTN :are there more than one?
        

        if npc is debug_character:#is debug_character even set? Should we instead use an npc attribute lookup?
            region_knowledges = [
                mem for mem in npc.mind.memory.semantic.get("region_knowledge", [])
                if isinstance(mem, RegionKnowledge) and mem.region_name == npc.region.name
            ]
            print(f"=== REGION KNOWLEDGE: {npc.region.name}, {npc.name} ===")
            if day == 1:
                for i, rk in enumerate(region_knowledges):

                    print(display_region_knowledge_summary(region_knowledges, npc=npc))

        debug_print(npc, "[THOUGHTS — filtered]", "think")
        for thought in npc.mind.thoughts:
            if thought.urgency > 1:
                debug_print(npc, f" - {thought.content} (urgency {thought.urgency})", "think")

    # STEP 4: Sanity Check on Character List
    for c in all_characters:
        if not hasattr(c, "motivation_manager"):
            print(f"[ERROR] Non-character in all_characters: {type(c)} -> {c}")

def begin_npc_turn(npc):
    npc.just_arrived = False
    #npc.turn_start_tick = get_game_state().tick
    npc.mind.remove_thought_by_content("No focus")

    # ✅ passive physiological drift
    npc.hunger = min(npc.hunger + 0.2, 20)
    #hunger = 20 → starving
    npc.effort = max(npc.effort - 0.1, 1)
    #effort = 1 → exhausted

    #npc.motivation_manager.sync_physiological_motivations()
    tick = get_game_state().tick
    npc.motivation_manager.sync_motivations(tick)

def end_npc_turn(npc):
    npc.mind.clear_stale_percepts()
    npc.inventory.clear_recently_acquired()
    #npc.last_action_tick = get_game_state().tick

    # reset observation flag so next tick will allow a fresh observation
    """ if hasattr(npc, "_observed_this_tick"):
        npc._observed_this_tick = False """

    game_state = get_game_state()#Needed for the lines below
    debug_print(f"[TURN] Hour {game_state.hour}, Day {game_state.day}", category="tick")


    
    

