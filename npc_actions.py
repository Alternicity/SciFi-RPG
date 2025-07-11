# npc_actions.py
from memory_entry import MemoryEntry
import copy

def visit_location_auto(character, region, location):
    if location is None:
        return False
    print(f"[AUTO VISIT] {character.name} is going to {location.name}")
    character.location = location
    character.just_arrived = True
    location.recent_arrivals.append(character)
    return True

# npc_actions.py
def steal_auto(character, region, item=None):
    print(f"[STEAL] {character.name} tries to steal {item.name if item else 'something'} at {character.location.name}")

    if not item:
        print("[STEAL] No item specified.")
        return

    location = character.location

    # Check if the location has the item in its inventory
    if not hasattr(location, "inventory") or item.name not in location.inventory.items:
        print(f"[STEAL FAIL] {item.name} not found in {location.name}'s inventory.")
        return

    # Skill-based theft logic
    employees = getattr(location, 'employees_there', [])
    observation = max([e.skills.get("observation", 0) for e in employees]) if employees else 0
    stealth = character.skills.get("stealth", 0)

    resistance_mod = getattr(location, "security_level", 0)
    attempt_mod = getattr(character, "criminal_modifier", 0)

    from attribute_tests import adversarial_attribute_test
    success = adversarial_attribute_test(
        attempt_value=stealth,
        resistance_value=observation,
        attempt_mod=attempt_mod,
        resistance_mod=resistance_mod,
        simulate=False,
        verbose=character.is_test_npc
    )
    from weapons import Weapon
    if success:
        stolen_item = copy.deepcopy(item)
        location.inventory.remove_item(item.name)
        character.inventory.add_item(stolen_item)
        print(f"[STEAL SUCCESS] {character.name} stole {stolen_item.name}!")

        if isinstance(stolen_item, Weapon):
            character.inventory.update_primary_weapon()

        # Optional memory entry
        memory_entry = MemoryEntry(
            subject=character.name,
            object_=stolen_item.name,
            verb="stole",
            details=f"Stole {stolen_item.name} from {location.name}",
            importance=7,
            type="theft",
            tags=["theft", "weapon", "crime"],
            initial_memory_type="episodic"
        )
        character.mind.memory.add_episodic(memory_entry)

        # Reduce related motivation
        character.motivation_manager.resolve_motivation("obtain_ranged_weapon")

        # Update intimidation stat if relevant
        if hasattr(stolen_item, "intimidate"):
            character.skills["intimidation"] = character.skills.get("intimidation", 0) + stolen_item.intimidate
            print(f"[STEAL] {character.name}'s intimidation increased due to {stolen_item.name}.")

    else:
        print(f"[STEAL FAIL] {character.name} failed to steal {item.name} from {location.name}.")

        #You could generalize this further later by checking containers within containers, 
        #or using location.get_all_items() if you add that kind of method

def rob_auto(npc, region=None, location=None, **kwargs):
    
    pass
    #print (f"npc rob called")

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
    

