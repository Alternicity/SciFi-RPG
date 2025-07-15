# simulate_day.py
import random
from location import Shop
from create_game_state import get_game_state
from ai_utility import UtilityAI #not currently accessed
from events import Robbery
from characterActions import execute_action #not currently accessed
from summary_utils import format_location
from display import display_region_knowledge_summary, display_percepts_table
from memory_entry import RegionKnowledge
from character_thought import Thought
from ambience_and_psy_utils import compute_location_ambience

def simulate_days(all_characters, num_days=1, debug_character=None):
    game_state = get_game_state()
    all_regions = game_state.all_regions
    all_locations = game_state.all_locations
    
    for _ in range(num_days):
        # STEP 1: Perceive and Think
        for region in all_regions:
            for npc in region.characters_there:
                if npc.is_player:
                    continue

                for npc in npc.location.characters_there:
                    npc.just_arrived = False

                for location in all_locations:
                    location.recent_arrivals.clear()
                # OBSERVE
                
                if npc is debug_character:
                    #print(f"[DEBUG] {npc.name} attempting to observe.")

                    npc.observe(region=region, location=npc.location)
                    #observe call moved here from npc AI think functions

                    #print(f"[DEBUG] {npc.name} location: {format_location(npc.location)}")
                    #replace with call to summary_utils.py def format_location(loc):

                #print(f"[DEBUG] {npc.name} region characters: {[c.name for c in region.characters_there]}")
                #verbose

                if npc.is_test_npc or npc is debug_character:
                    display_percepts_table(npc)

                # --- Ambience Influence + Social Vibe Logging ---
                #This framework sets the stage for scene-level emergent stories
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
                    think_loops = getattr(npc, "max_thinks_per_tick", 1)
                    for _ in range(think_loops):
                        npc.ai.think(npc.location.region)
                    npc.ai.promote_thoughts()

                # DEBUG: Thought Check 1

                """ if debug_character and npc.name == debug_character.name:
                    print(f"\n[DEBUG] From simulate_days Thought Check 1 {npc.name} Thoughts:")
                    for t in npc.mind:
                        print(f" - {t}")
                    print(f"[DEBUG] simulate_days Thought Check 1, debug_character attention focus is {npc.attention_focus}") """
                
                    #print(f"[DEBUG] Motivations: {npc.motivation_manager.get_motivations()}")
                    #At some point, ensure you're calling npc.inventory.clear_recently_acquired() somewhere in the tick loop
                    
        # STEP 2: Choose and Execute Action
        for npc in all_characters:
            if hasattr(npc, 'ai') and npc.ai:

                # NEW: Let AI process thoughts
                npc.ai.evaluate_thoughts()  # << Thought-based motivation tuning
                
                npc.ai.promote_thoughts()     # line 71

                # DEBUG: Thought Check 2

                """ if debug_character and npc.name == debug_character.name:
                    print(f"\n[DEBUG] from simulate_days Thought Check 2 {npc.name} Thoughts:")
                    for t in npc.mind.thoughts:
                        print(f" - {t}")
                    print(f"[DEBUG] Attention focus: {npc.attention_focus}") """

                    #print(f"[DEBUG] Motivations: {npc.motivation_manager.get_motivations()}")

                region = npc.location.region if hasattr(npc.location, 'region') else None
                action = npc.ai.choose_action(npc.location)
                if action:
                    npc.ai.execute_action(action, region)
                    print(f"[FLOW DEBUG] {npc.name} finished action, current location: {npc.location}")


        # STEP 3: Post-Day DEBUG (single character)
        for npc in all_characters:
            if npc is not debug_character:
                continue
            #print(f"MIND: {[str(thought) for thought in npc.mind]}")

            """ print("MOTIVATIONS:")
            for m in npc.motivation_manager.get_motivations():
                print(f" - {m}") """
            
            #print("MEMORY (Episodic):")

            for mem in npc.mind.memory.episodic:
                print(f" - {mem}")

        print(f"[DEBUG] debug_character is: {debug_character.name} (id={id(debug_character)})")

        if npc is debug_character:
            region_knowledges = [
                mem for mem in npc.mind.memory.semantic.get("region_knowledge", [])
                if isinstance(mem, RegionKnowledge) and mem.region_name == npc.region.name
            ]
            print(f"=== REGION KNOWLEDGE: {npc.region.name}, {npc.name} ===")
            for i, rk in enumerate(region_knowledges):

                print(display_region_knowledge_summary(region_knowledges, npc=npc))

                print("THOUGHTS:")
                for thought in npc.mind:
                    print(f" - {thought}")  # Optional again

                print(f"ATTENTION: {npc.attention_focus}")


    # STEP 4: Sanity Check on Character List
    for c in all_characters:
        if not hasattr(c, "motivation_manager"):
            print(f"[ERROR] Non-character in all_characters: {type(c)} -> {c}")

    # STEP 5: Optional Motivation Debugging CURRENTLY DOESNT DO ANYTHING
    if debug_character:
        for character in all_characters:
            motivations = character.motivation_manager.get_motivations()
            criminal_motivated = any(
                m.type in {"rob", "steal", "obtain_ranged_weapon"} for m in motivations
            )



