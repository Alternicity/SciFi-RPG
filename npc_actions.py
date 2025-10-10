# npc_actions.py
from memory_entry import MemoryEntry
import copy
from motivation import MotivationManager

def visit_location_auto(character, region, location):
    if location is None:
        return False
    print(f"[AUTO VISIT] {character.name} is going to {location.name}")
    
     # Update character’s state
    character.location = location
    character.just_arrived = True

    # --- stamp tick/day context ---
    # uses character’s stored time attributes if available
    tick = getattr(character, "current_tick", None)
    day = getattr(character, "current_day", None)
    timestamp = f"Day {day} Tick {tick}" if tick is not None else None

    # Track arrivals at the location
    if hasattr(location, "recent_arrivals"):
        location.recent_arrivals.append(character)

    # Ensure location tracks who’s currently there
    if hasattr(location, "characters_there") and character not in location.characters_there:
        location.characters_there.append(character)

    # Trigger perception of surroundings immediately
    character.perceive_current_location()

    # Optional: stamp tick/day for debugging or analytics
    """ if hasattr(character, "current_tick"):
        character.last_visit_tick = character.current_tick
        character.last_visit_day = getattr(character, "current_day", None) """

    # --- remember last visit ---
    character.last_visit_tick = tick
    character.last_visit_day = day
    character.last_visit_timestamp = timestamp
    
    return True

def rob_auto(npc, region=None, location=None, target_item=None, **kwargs):
    from events import Robbery
    from InWorldObjects import CashWad

    if not location:
        location = npc.location

    print(f"[NPC ACTION] {npc.name} attempts to rob {location.name}")
    npc.motivation_manager.resolve_motivation("obtain_ranged_weapon")
    has_weapon = hasattr(npc, "primary_weapon") and npc.primary_weapon is not None

    robbery_event = Robbery(
        instigator=npc,
        location=location,
        weapon_used=has_weapon
    )

    robbery_event.target_item = target_item  # Optional, like a high-value item from percepts

    # Let the existing system handle everything
    result = robbery_event.resolve(simulate=False, verbose=npc.is_test_npc)

    # Motivation resolution — assuming rob target was cash or similar
    if hasattr(npc, "motivation_manager"):
        npc.motivation_manager.resolve_motivation("rob")

    return result
    """I can later enhance this to let the NPC:
Choose a target item with logic like “most valuable percepted object in location”
Decide whether to rob based on mood, threat level, weapon presence, etc. """

def steal_auto(npc, region, item=None):
    print(f"[STEAL] {npc.name} tries to steal {item.name if item else 'something'} at {npc.location.name}")

    if not item:
        print("[STEAL] No item specified.")
        return

    location = npc.location

    # Check if the location has the item in its inventory
    if not hasattr(location, "inventory") or item.name not in location.inventory.items:
        print(f"[STEAL FAIL] {item.name} not found in {location.name}'s inventory.")
        return

    # Skill-based theft logic
    employees = getattr(location, 'employees_there', [])
    observation = max([e.skills.get("observation", 0) for e in employees]) if employees else 0
    stealth = npc.skills.get("stealth", 0)

    resistance_mod = getattr(location, "security_level", 0)
    attempt_mod = getattr(npc, "criminal_modifier", 0)

    from attribute_tests import adversarial_attribute_test
    success = adversarial_attribute_test(
        attempt_value=stealth,
        resistance_value=observation,
        attempt_mod=attempt_mod,
        resistance_mod=resistance_mod,
        simulate=False,
        verbose=npc.is_test_npc
    )
    from weapons import Weapon
    if success:
        stolen_item = copy.deepcopy(item)
        location.inventory.remove_item(item.name)
        npc.inventory.add_item(stolen_item)
        npc.inventory.recently_acquired.append(stolen_item)
        npc.inventory.update_weapon_flags()
        npc.inventory.update_primary_weapon()
        print(f"[STEAL SUCCESS] {npc.name} stole {stolen_item.name}!")
        print(f"[DEBUG] Primary weapon equipped: {npc.inventory.primary_weapon}")
        
        if isinstance(stolen_item, Weapon):
            npc.inventory.update_primary_weapon()
            npc.motivation_manager.resolve_motivation("obtain_ranged_weapon")
            cleared = npc.motivation_manager.clear_highest_priority_motivation()
            if cleared:
                print(f"[MOTIVATION] Cleared highest-priority motivation: {cleared.type}")
            npc.mind.attention_focus = None
        if npc.is_test_npc:
            print(f"[DEBUG] Primary weapon equipped: {getattr(npc.inventory.primary_weapon, 'name', None)}")

        # Optional memory entry
        memory_entry = MemoryEntry(
            subject=npc.name,
            object_=stolen_item.name,
            verb="stole",
            details=f"Stole {stolen_item.name} from {location.name}",
            importance=7,
            type="theft",
            tags=["theft", "weapon", "crime"],
            initial_memory_type="episodic",
            function_reference=None,
            implementation_path=None,
            associated_function=None
        )
        npc.mind.memory.add_episodic(memory_entry)

        print(f"[STEAL] {npc.name} successfully stole {stolen_item.name} from {location.name}")

        # Reduce related motivation
        npc.motivation_manager.resolve_motivation("obtain_ranged_weapon")

        # Update intimidation stat if relevant
        if hasattr(stolen_item, "intimidate"):
            npc.skills["intimidation"] = npc.skills.get("intimidation", 0) + stolen_item.intimidate
            print(f"[STEAL] {npc.name}'s intimidation increased due to {stolen_item.name}.")

    else:
        print(f"[STEAL FAIL] {npc.name} failed to steal {item.name} from {location.name}.")

        #You could generalize this further later by checking containers within containers, 
        #or using location.get_all_items() if you add that kind of method

def exit_location_auto():
    print (f"npc exit location called")

def eat_auto():
    pass
    print (f"npc eat called")

def idle_auto(npc, region=None, **kwargs):
    pass
    #print (f"npc idle called")

#explore
    """ if not percepts and not promoted_actions:
            unexplored = [l for l in region.locations if l.name != self.npc.location.name]
            if unexplored:
                next_loc = random.choice(unexplored)
                print(f"[EXPLORE] {self.npc.name} wandering to {next_loc.name}")
                return {
                    "name": "visit_location",
                    "params": {"location": next_loc}
                } """
    

