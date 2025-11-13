# npc_actions.py
from memory_entry import MemoryEntry
from debug_utils import debug_print
import copy
from character_thought import Thought
from create_game_state import get_game_state


def visit_location_auto(character, region=None, destination=None, destination_name=None, **kwargs):
    npc = character

    import inspect
    caller = inspect.stack()[1]
    caller_info = f"{caller.function} @ {caller.filename}:{caller.lineno}"

    # inside visit_auto() or the movement routine where you actually change civ.location
    debug_print(npc, f"[MOVE] {npc.name} -> {getattr(destination,'name',destination)} triggered_by={caller_info}", category="movement")


    debug_print(
        npc,
        f"[VISIT TRACE] visit_location_auto invoked by {caller_info}",
        category="visit"
    )#is this print superfluous now?


    search_region = region or npc.region #search_region is not accessed
    debug_print(npc, f"[VISIT] Arrived at {destination.name}", "visit")

    # Resolve destination by name if needed
    if destination is None and destination_name:
        destination = search_region.get_location_by_name(destination_name)
        debug_print(npc, f"[VISIT] Resolved destination_name='{destination_name}' to {destination}", category="visit")
    elif destination is None and "destination_name" in kwargs:
        destination = search_region.get_location_by_name(kwargs["destination_name"])
        debug_print(npc, f"[VISIT] Resolved from kwargs destination_name='{kwargs['destination_name']}' to {destination}", category="visit")

    if destination is None:
        debug_print(npc, f"[VISIT] {npc.name} has no valid destination to visit (lookup failed).", category="visit")
        return False
    
    if npc.just_arrived:#line 39
        return True   # Already here, don't re-visit

    # --- Core movement ---
    old_location = npc.location
    # Remove NPC from old location
    if old_location and hasattr(old_location, "characters_there"):
        if npc in old_location.characters_there:
            old_location.characters_there.remove(npc)

    npc.location = destination
    npc.just_arrived = True
    #this is the only place in the code base where  npc.just_arrived is set to true
    # --- Clear visit-related thoughts ---
    npc.mind.remove_thoughts_with_tag("visit")
    # Clear visit motivation if it was active
    npc.motivation_manager.remove_motivation("visit")

    debug_print(npc, f"[VISIT] {npc.name} arrived at {npc.location.name}", category="visit")

    # --- Track presence ---
    if hasattr(destination, "characters_there") and npc not in destination.characters_there:
        destination.characters_there.append(npc)
    if hasattr(destination, "recent_arrivals"):
        destination.recent_arrivals.append(npc)

    # --- Optional tick/day stamp ---
    tick = getattr(character, "current_tick", None)
    day = getattr(character, "current_day", None)
    timestamp = f"Day {day} Tick {tick}" if (day is not None and tick is not None) else None
    character.last_visit_timestamp = timestamp

    # --- Observation ---
    if hasattr(character, "perceive_current_location"):
        character.perceive_current_location()#line 48

    # --- Episodic memory ---
    if hasattr(character, "mind") and hasattr(character.mind, "memory"):
        memory_entry = MemoryEntry(
            subject=character.name,
            verb="arrived_at",
            object_=destination.name,
            details=f"{character.name} arrived at {destination.name}.",
            tags=["arrival", "travel", "location_entry"],
            type="event",
            initial_memory_type="episodic",
            timestamp=timestamp or "Unknown time"
        )
        character.mind.memory.episodic.append(memory_entry)

        # Clear thoughts related to this destination
        if hasattr(character, "mind"):
            to_remove = []
            for t in list(character.mind.thoughts):
                # if thought source is the location or content references the location name, remove/resolve it
                if getattr(t, "source", None) is destination or str(destination.name) in str(getattr(t, "content", "")):
                    t.resolved = True
                    to_remove.append(t)
            for t in to_remove:
                try:
                    character.mind.thoughts.remove(t)
                    #perhaps add it to memory.forgotten
                except ValueError:
                    pass
            # Clear attention focus if it pointed at that thought
            af = getattr(character.mind, "attention_focus", None)
            if af and (getattr(af, "source", None) is destination or getattr(af, "content", "") and destination.name in getattr(af, "content", "")):
                character.mind.attention_focus = None

    return True


def rob_auto(npc, region=None, location=None, target_item=None, **kwargs):
    from events import Robbery
    from InWorldObjects import CashWad

    if not location:
        location = npc.location

    #debug_print(npc, f"[DEBUG] from rob_auto, robbable={getattr(npc.location, 'robbable', None)}", "rob")

    debug_print(npc, f"[NPC ACTION] {npc.name} attempts to rob {location.name}", category = "action")
    npc.motivation_manager.resolve_motivation("obtain_ranged_weapon")
    has_weapon = hasattr(npc, "primary_weapon") and npc.primary_weapon is not None

    robbery_event = Robbery(
        instigator=npc,
        location=location,
        weapon_used=has_weapon,
        mode="npc"
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
        return False

    location = npc.location

    # Ensure location has inventory and that item exists
    if not hasattr(location, "inventory") or item.name not in location.inventory.items:
        print(f"[STEAL FAIL] {item.name} not found in {location.name}'s inventory.")
        return False

    # Theft difficulty setup
    employees = getattr(location, 'employees_there', [])
    observation = max((e.skills.get("observation", 0) for e in employees), default=0)
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

    if not success:
        print(f"[STEAL FAIL] {npc.name} failed to steal {item.name} from {location.name}.")
        return False

    # ============================
    # ✅ SUCCESSFUL STEAL BEGINS
    # ============================

    # Remove real item and give NPC a copy
    stolen_item = item.clone()
    location.inventory.remove_item(item.name)
    npc.inventory.add_item(stolen_item)
    npc.inventory.recently_acquired.append(stolen_item)

    # Update weapon state
    npc.inventory.update_weapon_flags()
    npc.inventory.update_primary_weapon()

    # ✅ Remove weapon-fetching motives
    npc.motivation_manager.remove_motivation("obtain_ranged_weapon")
    npc.mind.remove_thoughts_with_tag("obtain_ranged_weapon")

    # ✅ Raise robbery motive cleanly (exactly once)
    npc.motivation_manager.update_motivations("rob", urgency=20)
    npc.motivation_manager.deboost_others("rob", amount=7)

    # ✅ (Optional) Set a robbery thought
    if npc.is_test_npc:
        npc.mind.add_thought(Thought(
            subject="robbery",
            content=f"Now that I'm armed, I could rob {location.name}.",
            origin="steal_auto_post",
            urgency=9,
            tags=["rob"]
        ))

    # ✅ DO NOT wipe attention_focus here
    # npc.mind.attention_focus must be set by the salience system afterwards

    # -----------------------------------------------
    # ✅ EPISODIC MEMORY ENTRY
    # -----------------------------------------------
    from memory_entry import MemoryEntry
    state = get_game_state()

    memory = MemoryEntry(
        subject=npc.name,
        object_=stolen_item.name,
        verb="stole",
        details=f"I stole a {stolen_item.name} from {location.name}.",
        type="theft",
        initial_memory_type="episodic",
        description="Theft of a ranged weapon enabling robbery.",
        tags=["theft", "weapon", "ranged_weapon", "enabling"],
        target=location.name,
        payload={"item": stolen_item, "location": location},
        source="steal_auto",
        created_day=state.day,
        last_updated_day=state.day,
    )

    npc.mind.memory.add_episodic(memory, current_day=state.day)

    # -----------------------------------------------
    # ✅ THOUGHT FROM MEMORY
    # -----------------------------------------------
    npc.mind.add_thought(
        Thought(
            subject=npc.name,
            content=f"I stole a {stolen_item.name}.",
            origin="episodic_memory",
            urgency=7,
            tags=["theft", "self", "weapon", "ranged_weapon", "enabling"],
            source=memory,
            weight=3.0
        )
    )

    # -----------------------------------------------
    # ✅ SKILL INCREASE (optional but realistic)
    # -----------------------------------------------
    if hasattr(stolen_item, "intimidate"):
        npc.skills["intimidation"] = npc.skills.get("intimidation", 0) + stolen_item.intimidate
        print(f"[STEAL] {npc.name}'s intimidation increased due to {stolen_item.name}.")

    print(f"[STEAL] {npc.name} successfully stole {stolen_item.name} from {location.name}")
    return True

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
    

