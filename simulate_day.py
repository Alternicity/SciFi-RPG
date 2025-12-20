# simulate_day.py
import random
from location.locations import Shop
from create.create_game_state import get_game_state
from ai.ai_utility import UtilityAI #not currently accessed
from events import Robbery
from characterActions import execute_action #not currently accessed
from summary_utils import format_location
from display import display_region_knowledge_summary, display_percepts_table
from memory.memory_entry import RegionKnowledge
from character_thought import Thought
from ambience.ambience_and_psy_utils import compute_location_ambience
from debug_utils import debug_print

def simulate_hours(all_characters, num_days=1, debug_character=None):
    game_state = get_game_state()
    all_regions = game_state.all_regions
    all_locations = game_state.all_locations
    day = game_state.day

    for _ in range(num_days):
        game_state.advance_hour()
        debug_print(None, f"[TIME] Hour {game_state.hour}, Day {game_state.day}", category="tick")

        for location in all_locations:
                    location.recent_arrivals.clear()

        # STEP 1: Perceive and Think
        for region in all_regions:
            for npc in region.characters_there:
                #npc._observed_this_tick = False
                begin_npc_turn(npc)
                if npc.is_player:
                    continue
                
                # OBSERVE
                npc.observe(region=region, location=npc.location)

                if npc is debug_character:
                    debug_print(npc, "This is a test NPC log.", category="think")
                    #or here?

                    

                if npc.is_test_npc or npc is debug_character:
                    display_percepts_table(npc)

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
                        social_data = {
                            "friends_present": [c.name for c in loc.characters_there if c.name in char.social_connections["friends"]],
                            "enemies_present": [c.name for c in loc.characters_there if c.name in char.social_connections["enemies"]],
                            "allies_present": [c.name for c in loc.characters_there if c.name in char.social_connections["allies"]],
                        }

                        # 4. Save semantic ambient snapshot
                        char.mind.memory.semantic.setdefault("ambient_vibes", []).append({
                            "location": loc.name,
                            "top_vibe": peak_tag,
                            "power": peak_power,
                            "others_present": [c.name for c in loc.characters_there if c.name != char.name],
                            **social_data
                        })


                # THINK CYCLE
                if hasattr(npc, 'ai') and npc.ai:
                    think_loops = getattr(npc, "max_thinks_per_tick", 1)#max_thinks_per_tick is just a placeholder, for uber npcs, not widely implemented
                    for _ in range(think_loops):
                        npc.ai.think(npc.location.region)
                    npc.ai.promote_thoughts()

                    #At some point, ensure you're calling npc.inventory.clear_recently_acquired() somewhere in the tick loop
                    
        # STEP 2: Choose and Execute Action
        for npc in all_characters:
            if hasattr(npc, 'ai') and npc.ai:

                #Let AI process thoughts
                npc.ai.evaluate_thoughts()  # << Thought-based motivation tuning
                
                region = npc.location.region if hasattr(npc.location, 'region') else None
                action = npc.ai.choose_action(npc.location.region)
                if action:
                    npc.ai.execute_action(action, region)

                    debug_print(npc, f"[ACTION] {npc.name} finished {action}, current location: {npc.location}", category="action")

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
    debug_print(f"[TURN] Begin NPC turn: {npc.name}", category="tick")

def end_npc_turn(npc):
    npc.mind.clear_stale_percepts()
    npc.inventory.clear_recently_acquired()
    #npc.last_action_tick = get_game_state().tick

    # reset observation flag so next tick will allow a fresh observation
    """ if hasattr(npc, "_observed_this_tick"):
        npc._observed_this_tick = False """

    game_state = get_game_state()#Needed for the lines below
    debug_print(f"[TURN] Hour {game_state.hour}, Day {game_state.day}", category="tick")


    
    

