# simulate_day.py
import random
from location import Shop
from create_game_state import get_game_state
from ai_utility import UtilityAI #not currently accessed
from events import Robbery
from characterActions import execute_action #not currently accessed


def simulate_days(all_characters, num_days=1, debug_character=None):
    game_state = get_game_state()
    all_regions = game_state.all_regions

    for _ in range(num_days):
        # STEP 1: Perceive and Think
        for region in all_regions:
            for npc in region.characters_there:
                if npc.is_player:
                    continue

                # OBSERVE
                print(f"In simulate_days, {npc.name} attempting to observe.")
                npc.observe(region=region, location=npc.location)


                if debug_character and npc.name == debug_character.name:
                    print(f"[DEBUG] {npc.name} percepts after observe:")
                    for k, v in npc._percepts.items():
                        print(f"  - {k}: {v.get('description', v['type'])}")                    
                    
                    print(f"[DEBUG] {npc.name} location: {npc.location}")
                    print(f"[DEBUG] {npc.name} region characters: {[c.name for c in region.characters_there]}")
                    print(f"[DEBUG] {npc.name} region objects: {[o.name if hasattr(o, 'name') else str(o) for o in getattr(region, 'objects_there', [])]}")


                if npc.is_test_npc:
                    print(f"[DEBUG] {npc.name} percepts after observe: {[v.get('description', v['type']) for v in npc._percepts.values()]}")

                #THINK
                if hasattr(npc, 'ai') and npc.ai:
                    npc.ai.think(npc.location.region)
                    npc.ai.promote_thoughts()

                # DEBUG: Thought Check
                if debug_character and npc.name == debug_character.name:
                    print(f"\n[DEBUG] {npc.name} Thoughts:")
                    for t in npc.mind:
                        print(f" - {t}")
                    print(f"[DEBUG] Attention focus: {npc.attention_focus}")
                    #print(f"[DEBUG] Motivations: {npc.motivation_manager.get_motivations()}")

        # STEP 2: Choose and Execute Action
        for npc in all_characters:
            if hasattr(npc, 'ai') and npc.ai:

                # NEW: Let AI process thoughts
                npc.ai.evaluate_thoughts()  # << Thought-based motivation tuning
                if npc.location and npc.location.region:
                    npc.ai.think(npc.location.region)
                else:
                    print(f"[Warning] {npc.name} has no location or region.")
                npc.ai.promote_thoughts()     # << Optional: Push important thoughts into action-focus

                # DEBUG: Thought Check
                if debug_character and npc.name == debug_character.name:
                    print(f"\n[DEBUG] {npc.name} Thoughts:")
                    for t in npc.mind.thoughts:
                        print(f" - {t}")
                    print(f"[DEBUG] Attention focus: {npc.attention_focus}")
                    #print(f"[DEBUG] Motivations: {npc.motivation_manager.get_motivations()}")

                region = npc.location.region if hasattr(npc.location, 'region') else None
                action = npc.ai.choose_action(npc.location)
                if action:
                    npc.ai.execute_action(action, region)

        # STEP 3: Post-Day DEBUG (single character)
        for npc in all_characters:
            if npc is not debug_character:
                continue
            print(f"=== DEBUG: {npc.name} ===")
            #print(f"MIND: {[str(thought) for thought in npc.mind]}")

            """ print("MOTIVATIONS:")
            for m in npc.motivation_manager.get_motivations():
                print(f" - {m}") """
            
            #print("MEMORY (Episodic):")

            for mem in npc.memory.episodic:
                print(f" - {mem}")
            print("MEMORY (Semantic):")
            for mem in npc.memory.semantic:
                print(f" - {mem}")
            #print("THOUGHTS:")
            for thought in npc.mind:
                pass
                """ print(f" - {thought}")
            print(f"ATTENTION: {npc.attention_focus}") """

    # STEP 4: Sanity Check on Character List
    for c in all_characters:
        if not hasattr(c, "motivation_manager"):
            print(f"[ERROR] Non-character in all_characters: {type(c)} -> {c}")

    # STEP 5: Optional Motivation Debugging
    for character in all_characters:
        motivations = character.motivation_manager.get_motivations()
        criminal_motivated = any(
            m.type in {"rob", "steal", "obtain_ranged_weapon"} for m in motivations
        )
        # Debug print here if desired


    #tmp
    for c in all_characters:
            if not hasattr(c, "motivation_manager"):
                print(f"[ERROR] Non-character in all_characters: {type(c)} -> {c}")
    #deprecated?
    for character in all_characters:
        motivations = character.motivation_manager.get_motivations()
        criminal_motivated = any(m.type in {"rob", "steal", "obtain_ranged_weapon"} for m in motivations)

        """if criminal_motivated:
            print(f"[Action] {character.name} is criminally motivated:")
             for m in motivations:
                if m.type in {"rob", "steal", "obtain_ranged_weapon"}:
                    print(f" - {m.type} (urgency: {m.urgency})") """

        # 🔄 OPTIONAL: Add future game state updates here
        # update_world_state(game_state)
        # handle_daily_events(game_state)
            # Add more actions like "Buy", "Recruit", "Report", etc.


