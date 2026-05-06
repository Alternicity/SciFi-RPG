# actions.npc_actions.py
from memory.memory_entry import MemoryEntry

from debug_utils import debug_print, can_narrate, print_region_fun
#can_narrate greyed out not accessed

import copy
from character_thought import Thought
from create.create_game_state import get_game_state
from focus_utils import clear_attention_focus
import random
from employment.employment import update_employee_presence
from character_components.npc_effects import RecentMealEffect
from employment.workplace_mixin import WorkplaceMixin
from create.create_game_state import get_game_state
game_state = get_game_state()

def have_fun_auto(npc, region=None):
    loc = npc.location
    cls = loc.__class__.__name__

    if cls == "Library":
        from world.books import Book
        books_here = [
            o for o in loc.items.objects_present
            if isinstance(o, Book)
        ]
        if books_here:
            book = random.choice(books_here)
            return read_auto(npc, region, item=book)

    if cls == "Park" or "nature" in getattr(loc, "tags", []):
        return stroll_auto(npc, region)

    if cls == "SportsCentre" or "sport" in getattr(loc, "tags", []):
        return exercise_auto(npc, region)

    # Generic fallback for SportsCentre, Cafe, etc.
    debug_print(npc, f"[FUN] {npc.name} enjoys being at {loc.name}", category="fun")

    entry = MemoryEntry(
        subject=npc.name,
        verb="enjoyed",
        object_=loc.name,
        details=f"Spent leisure time at {loc.name}.",
        importance=1,
        tags=["fun", "leisure"],
        type="experience",
    )
    npc.mind.memory.add_episodic(entry)
    return True


# actions/npc_actions.py

def exercise_auto(npc, region=None):
    """NPC uses sports equipment at a SportsCentre."""
    from objects.sports_objects import PoolTable, BowlingLane
    import random

    loc = npc.location

    # Find free equipment, prefer pool table then bowling
    pool_tables = [
        o for o in loc.items.objects_present
        if isinstance(o, PoolTable) and o.is_free()
    ]
    lanes = [
        o for o in loc.items.objects_present
        if isinstance(o, BowlingLane) and o.is_free()
    ]

    if pool_tables:
        table = random.choice(pool_tables)
        table.occupy(npc)
        npc.current_sports_equipment = table  # track for vacating later

        debug_print(
            npc,
            f"[EXERCISE] {npc.name} plays pool at {table.name}",
            category="fun"
        )
        verb = "played_pool"
        detail = f"Played pool at {table.name} in {loc.name}."

    elif lanes:
        lane = random.choice(lanes)
        lane.occupy(npc)
        npc.current_sports_equipment = lane

        pins = lane.roll()
        debug_print(
            npc,
            f"[EXERCISE] {npc.name} bowls at {lane.name} — {pins} pins",
            category="fun"
        )
        verb = "went_bowling"
        detail = f"Bowled at {lane.name}, knocked down {pins} pins."

    else:
        # All equipment occupied — generic activity
        npc.current_sports_equipment = None
        debug_print(npc, f"[EXERCISE] {npc.name} works out at {loc.name}", category="fun")
        verb = "exercised"
        detail = f"Worked out at {loc.name}."

    entry = MemoryEntry(
        subject=npc.name,
        verb=verb,
        object_=loc.name,
        details=detail,
        importance=1,
        tags=["fun", "sport", "leisure"],
        type="experience",
    )
    npc.mind.memory.add_episodic(entry)
    return True

def stroll_auto(npc, region=None):
    """NPC wanders and enjoys the park environment."""
    loc = npc.location

    # Absorb ambience from trees and plants
    from objects.trees_and_plants import Tree, Plant
    nature_objects = [
        o for o in loc.items.objects_present
        if isinstance(o, (Tree, Plant))
    ]

    resonance = sum(getattr(o, "resonance_factor", 1.0) for o in nature_objects)
    psy_gain = sum(getattr(o, "golden_ratio_influence", 0.0) for o in nature_objects)

    # Boost psy for sensitive NPCs
    if psy_gain > 0 and getattr(npc, "psy", 0) > 5:
        npc.psy = min(20, npc.psy + psy_gain * 0.1)
        debug_print(npc, f"[STROLL] Psy resonance +{psy_gain:.1f}", category="fun")

    debug_print(
        npc,
        f"[STROLL] {npc.name} strolls through {loc.name} "
        f"(resonance={resonance:.1f}, {len(nature_objects)} nature objects)",
        category="fun"
    )

    entry = MemoryEntry(
        subject=npc.name,
        verb="strolled",
        object_=loc.name,
        details=f"Wandered through {loc.name}, felt the resonance of nature.",
        importance=1,
        tags=["fun", "nature", "leisure"],
        type="experience",
    )
    npc.mind.memory.add_episodic(entry)
    return True

def read_auto(npc, region=None, *, item):
    """NPC reads a book."""

    if item is None:
        debug_print(npc, "[READ] No book provided", category="fun")
        return False
    
    if not hasattr(item, "get_knowledge_payload"):
        return False

    payload = item.get_knowledge_payload()

    # Reduce have_fun urgency slightly (they're enjoying themselves)
    npc.motivation_manager.set_urgency(
        "have_fun",
        max(1, npc.motivation_manager.get_motivation("have_fun").urgency - 1)
    )

    # Boost fun stat
    npc.fun = min(10, npc.fun + 2)

    # Psy effect on sensitive NPCs
    psy_res = payload.get("psy_resonance", 0)
    if psy_res > 0 and getattr(npc, "psy", 0) > 5:
        npc.psy = min(20, npc.psy + psy_res)
        debug_print(npc, f"[PSY] {npc.name} resonates with '{item.title}' +{psy_res}", category="psy")

    # Create a memory of reading this
    entry = MemoryEntry(
        subject=npc.name,
        verb="read",
        object_=item.title,
        details=f"Read '{item.title}' at {npc.location.name}",
        tags=["reading", "knowledge"] + payload.get("subject_tags", []),
        importance=2 + int(psy_res),
        type="knowledge_acquisition",
        payload=payload,
    )
    npc.mind.memory.add_episodic(entry)

    # Redacted books create a specific thought
    if item.is_redacted and not npc.mind.has_thought_with_tag("redacted_content"):
        npc.mind.add_thought(Thought(
            subject="knowledge",
            content=f"Pages are missing from '{item.title}'. Why?",
            urgency=3,
            tags=["redacted_content", "curiosity", "mystery"]
        ))

    debug_print(npc, f"[READ] {npc.name} read '{item.title}' fun={npc.fun}", category="fun")
    return True


def visit_location_auto(character, region=None, destination=None, destination_name=None, **kwargs):
    npc = character
    gs = get_game_state()

    debug_print(
            npc,
            f"[VISIT] {npc.name} role={npc.debug_role} "
            f"from={npc.location} to={destination.name}",
            category="visit"
        )

    import inspect
    caller = inspect.stack()[1]
    caller_info = f"{caller.function} @ {caller.filename}:{caller.lineno}"

    search_region = region or npc.region
    #debug_print(npc, f"[VISIT] Arrived at {destination.name}", "visit")

    # Resolve destination by name if needed
    #This code seems odd. If this function is called there should a priori be a destination location
    if destination is None and destination_name:
        destination = search_region.get_location_by_name(destination_name)
        #debug_print(npc, f"[VISIT] Resolved destination_name='{destination_name}' to {destination}", category="visit")
    elif destination is None and "destination_name" in kwargs:
        destination = search_region.get_location_by_name(kwargs["destination_name"])
        debug_print(npc, f"[VISIT] Resolved from kwargs destination_name='{kwargs['destination_name']}' to {destination}", category="visit")
        #so this block marked for possible deprecation

    if destination is None:
        debug_print(npc, f"[VISIT] {npc.name} has no valid destination to visit (lookup failed).", category="visit")
        return False

    #vacate an pool table etc
    equipment = getattr(npc, "current_sports_equipment", None)
    if equipment and hasattr(equipment, "vacate"):
        equipment.vacate(npc)
        npc.current_sports_equipment = None

    # --- Core movement ---
    
    # Remove NPC from old location
    old_location = npc.location
    old_region = npc.region

    # Remove from current location
    if old_location and hasattr(old_location, "characters_there"):
        if npc in old_location.characters_there:
            old_location.characters_there.remove(npc)

    npc.previous_location = old_location
    npc.location = destination
    npc.region = destination.region

    #tmp print until visit_region_auto() exists
    if old_region and old_region is not npc.region:
        debug_print(
            npc,
            f"[REGION DRIFT] {old_region.name} → {npc.region.name}",
            category=["placement", "warning"]
        )
        

    npc.just_arrived = True
    npc.time_in_location = 0
    npc.recently_visited.append((npc.location, gs.hour))
    npc.recently_visited = npc.recently_visited[-3:]  # keep last 3


    # derive purpose from current top motivation
    top = npc.motivation_manager.get_highest_priority_motivation()
    new_purpose = str(top.type) if top else None

    # Only reset fulfilled if purpose changes
    if new_purpose != npc.location_purpose:
        npc.location_purpose = new_purpose
        npc.location_purpose_fulfilled = False
    # If same purpose, preserve fulfilled state

        print(f"[VISIT RESET] {npc.name} purpose_fulfilled reset at {destination}")

    npc.mind.remove_thoughts_with_tag("leave_location")#likly source
    
    #the following track presence block move up to here
    # --- Track presence ---
    if hasattr(destination, "characters_there") and npc not in destination.characters_there:
        destination.characters_there.append(npc)
    if hasattr(destination, "recent_arrivals"):
        destination.recent_arrivals.append(npc)
        """ debug_print(
            npc,
            f"[ARRIVAL] Added to recent_arrivals at {destination.name}",
            category="visit"
        ) """

    # Entering or leaving workplace
    update_employee_presence(npc, game_state.hour)

    if npc.current_anchor and npc.current_anchor.type == "work":
        debug_print(npc, "[ANCHOR] Work anchor satisfied — clearing", category="anchor")
        npc.current_anchor.active = False
        npc.current_anchor = None

    #this is the only place in the code base where  npc.just_arrived is set to true
    # --- Clear visit-related thoughts ---
    npc.mind.remove_thoughts_with_tag("visit")
    # Clear visit motivation if it was active
    npc.motivation_manager.remove_motivation("visit")

    debug_print(npc, f"[VISIT] {npc.name} arrived at {npc.location.name}", category="visit")

    debug_print(
        npc,
        f"[MOVE] {npc.name} {npc.previous_location} -> {destination} | "
        f"old_chars={len(getattr(old_location,'characters_there',[])) if old_location else None} "
        f"new_chars={len(destination.characters_there)}",
        category="visit"
    )

    #the assert block stays down here
    assert npc in destination.characters_there, (f"{npc.name} not in {destination}.characters_there")

    assert npc.location in npc.region.locations, (
        f"{npc.name} is in {npc.location} which is not in region {npc.region.name}"
    )

    #tmp
    from location.locations import Cafe
    if isinstance(destination, Cafe):
        pass
        """ print(
            f"[VISIT CHECK] npc={npc.name} "
            f"dest_id={id(destination)} "
            f"chars={[ (c.name, id(c)) for c in destination.characters_there ]}"
        ) """


    # --- Optional hour/day stamp ---
    hour = getattr(character, "current_hour", None)
    day = getattr(character, "current_day", None)
    timestamp = f"Day {day} Hour {hour}" if (day is not None and hour is not None) else None
    character.last_visit_timestamp = timestamp

    # --- Observation ---
    """ if hasattr(character, "perceive_current_location"):
        character.perceive_current_location() """

    # --- Episodic memory ---
    if hasattr(character, "mind") and hasattr(character.mind, "memory"):
        prev_loc_name = getattr(character.previous_location, "name", None)
        dest_name = destination.name

        movement_memory = MemoryEntry(
            subject=character.name,
            verb="arrived_at",
            left=prev_loc_name,
            arrived_at=dest_name,
            object_=dest_name,
            details=f"{character.name} moved from {prev_loc_name} to {dest_name}.",
            tags=["movement", "travel", "arrival", "location_entry"],
            type="movement",
            initial_memory_type="episodic",
            timestamp=timestamp or "Unknown time",
            description=f"Movement event: {character.name} → {dest_name}",
            target=destination,
            payload={
                "previous_location": prev_loc_name,
                "destination": dest_name,
                "day": day,
                "hour": hour
            },
            associated_function="visit_location_auto",
            implementation_path="npc_actions.visit_location_auto"
        )

        character.mind.memory.episodic.append(movement_memory)


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
                clear_attention_focus(character)
                #replaced:
                #character.mind.attention_focus = None
                
    return True


def rob_auto(npc, region=None, location=None, target_item=None, **kwargs):
    from events import Robbery
    from objects.InWorldObjects import CashWad

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
    debug_print(
            npc,
            f"Tries to steal {item.name if item else 'something'} at {npc.location.name}",
            category="steal"
        )

    if not item:
        print("[STEAL] No item specified.")
        return False

    location = npc.location

    # Ensure location has inventory and that item exists
    if not hasattr(location, "inventory") or item not in location.inventory.items.values():
        print(f"[STEAL FAIL] {item.name} not found in {location.name}'s inventory.")
        return False

    # Theft difficulty setup
    employees = location.employees_there if isinstance(location, WorkplaceMixin) else []
    observation = max((e.skills.get("observation", 0) for e in employees), default=0)
    stealth = npc.skills.get("stealth", 0)
    resistance_mod = getattr(location, "security_level", 0)
    attempt_mod = getattr(npc, "criminal_modifier", 0)

    from attribute_tests import adversarial_attribute_test
    verbose = getattr(npc, "debug_role", None) == "primary"
    success = adversarial_attribute_test(
        attempt_value=stealth,
        resistance_value=observation,
        attempt_mod=attempt_mod,
        resistance_mod=resistance_mod,
        simulate=False,
        
    )
    if getattr(npc, "debug_role", None) == "primary":
        debug_print(
            npc,
            f"Intimidation result → success={success}",
            category="event"
        )

    if not success:
        debug_print(
            npc,
            f"Failed to steal {item.name} from {location.name}",
            category="steal"
        )

        return False

    # ============================
    # ✅ SUCCESSFUL STEAL BEGINS
    # ============================

    # Remove real item and give NPC a copy
    #stolen_item = item.clone()


    location.inventory.remove_item(item)
    #may need to add an overload for this if remove_item currently expects a name:
    #location.inventory.remove_item(item.name)

    item.owner = npc
    npc.inventory.add_item(item)
    #npc.inventory.add_item(stolen_item)
    npc.inventory.recently_acquired.append(item)

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
    
    #from memory.memory_entry import MemoryEntry
    #already at top

    state = get_game_state()

    memory = MemoryEntry(
        subject=npc.name,
        object_=item.name,#was stolen_item
        verb="stole",
        details=f"I stole a {item.name} from {location.name}.",#was stolen_item
        type="theft",
        initial_memory_type="episodic",
        description="Theft of a ranged weapon enabling robbery.",
        tags=["theft", "weapon", "ranged_weapon", "enabling"],
        target=location.name,
        payload={"item": item, "location": location},#was stolen_item
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
            content=f"I stole a {item.name}.",#was stolen_item
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
    if hasattr(item, "intimidation"):
        npc.skills["intimidation"] = npc.skills.get("intimidation", 0) + item.intimidation
        debug_print(
            npc,
            f"Intimidation increased due to {item.name}",
            category="attribute"
        )


    debug_print(
            npc,
            f"Successfully stole {item.name} from {location.name}",
            category="steal"
        )

    return True

def exit_location_auto():
    print (f"npc exit location called")

def eat_auto(npc, region=None, *, item):

    debug_print(
        npc,
        f"[EATING] eat_auto called for {npc.name}",
        category="eat"
    )

    debug_print(
        npc,
        f"[EAT DEBUG] owner={getattr(item.owner,'name',None)} npc={npc.name}",
        category="eat"
    )

    if item.owner != npc:
        debug_print(npc, "[EAT] Ownership mismatch", category="eat")
        return False

    # reduce hunger immediately
    npc.hunger = max(0, npc.hunger - item.nutrition)
    # soften hunger thought
    npc.mind.reduce_thought_urgency("hunger", 5)
    
    #tmp
    
    print(f"[EAT PURPOSE CHECK] purpose='{npc.location_purpose}' type={type(npc.location_purpose)} == 'eat': {npc.location_purpose == 'eat'}")
    if npc.location_purpose == "eat":
        npc.location_purpose_fulfilled = True
    print(f"[EAT COMPLETE] location_purpose={npc.location_purpose} fulfilled={npc.location_purpose_fulfilled}")

    # 🔥 NEW: remove if no longer hungry
    t = npc.mind.get_thought_with_tag("hunger")
    if t and t.urgency <= 1:#edited
        npc.mind.remove_thoughts_with_tag("hunger")

    # reduce motivation strongly
    npc.motivation_manager.set_urgency("eat", 0)
    
    # 🔥 NEW: optional full suppression
    npc.motivation_manager.suppress("eat", reason="recent_meal", duration=3)

    # 🔥 Promote next motivation
    next_m = npc.motivation_manager.get_highest_priority_motivation(exclude={"eat"})

    # TC2 Specific targeted have_fun boost
    fun_m = npc.motivation_manager.get_motivation("have_fun")
    if fun_m:
        boost = max(2, item.nutrition // 2)
        npc.motivation_manager.set_urgency("have_fun", fun_m.urgency + boost)
        #In the future we could initialize problematic protect_family very low, but boost it hugely when necessary
        debug_print(npc, f"[POST-EAT] Boosting have_fun → {fun_m.urgency + boost}", category="motive")
        #print(f"[POST-EAT RAW] have_fun boost firing")
    # remove from inventory
    try:
        npc.inventory.remove_item(item)
    except Exception as e:
        print("REMOVE_ITEM CRASH:", e)
        import traceback
        traceback.print_exc()
        raise

    from inventory import debug_inventory
    debug_inventory(npc)
    debug_print(
        npc,
        f"[EAT] Ate {item.name} nutrition={item.nutrition} hunger now={npc.hunger}",
        category="action"
    )

    # inventory debug
    for inv in npc.inventory.items.values():
        debug_print(
            npc,
            f"[INV] {inv.name} id={id(inv)} owner={getattr(inv.owner,'name',inv.owner)}",
            category="eat"
        )

    # apply digestion effect
    npc.apply_effect(RecentMealEffect())

    # soften hunger instead of hard delete
    npc.mind.reduce_thought_urgency("hunger", 5)

    # reduce motivation strongly (not just resolve)
    npc.motivation_manager.set_urgency("eat", 0)#hmm is this necessary here?

    # inject leave pressure
    leave_boost = 8 + item.nutrition // 2
    npc.mind.reinforce_or_create_thought(
        "leave_location",
        amount=leave_boost,
        content=f"I should leave {npc.location.name}.",
        tags=["leave_location", "movement"]
    )

    #print_region_fun(npc.location.region)
    
    # memory
    from memory.memory_entry import MemoryEntry

    entry = MemoryEntry(
        subject=npc,
        object_=item,
        details=f"Ate {item.name} at {npc.location.name}",
        importance=1,
        owner=npc,
        tags=["eat", "food"]
    )

    npc.mind.memory.add_episodic(entry)

    return True

def buy_auto(npc, region, *, item):
    location = npc.location

    if not hasattr(location, "cash_register"):
        debug_print(npc, "[BUY] No register here", category="error")
        return False

    if item not in location.items_available:
        debug_print(
            npc,
            f"[BUY] Item {item.name} no longer available",
            category="error"
        )
        return False

    price = item.price

    # buyer pays
    if not npc.wallet.spend_bank(price):
        debug_print(npc, "[BUY] Not enough funds", category="action")
        return False

    # seller receives
    location.cash_register.deposit(price)

    # decrement stock
    item.quantity -= 1
    """ But item is also the template object in the shop list.
    This means if multiple NPCs buy it simultaneously you may get weird behavior.
    Eventually you'll want a stock item vs instance item separation, but that's not urgent. """

    if item.quantity <= 0:
        location.items_available.remove(item)


    # create owned item
    owned_food = item.__class__(quantity=1)
    owned_food.owner = npc
    owned_food.human_readable_id = f"{npc.name}'s {item.name}"

    npc.inventory.add_item(owned_food, quantity=1)


    debug_print(
        npc,
        f"[BUY DEBUG] owned_food id={id(owned_food)} owner={owned_food.owner.name}",
        category="buy"
    )

    debug_print(
        npc,
        f"[BUY] Purchased {item.name} for {price}. "
        f"Wallet now bank={npc.wallet.bankCardCash}, cash={npc.wallet.cash}",
        category="action"
    )

    return True


    """ npc.inventory.add_item(item.clone(quantity=1))
    item.quantity -= 1 """


def procure_food_auto(self):
    npc = self
    debug_print(npc, f"[EATING] procure_food_auto called for {npc.name}", category="eat")
    



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
    

