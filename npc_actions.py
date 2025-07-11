# npc_actions.py
from memory_entry import MemoryEntry
def visit_location_auto(character, region, location):
    if location is None:
        return False
    print(f"[AUTO VISIT] {character.name} is going to {location.name}")
    character.location = location
    character.just_arrived = True
    location.recent_arrivals.append(character)
    return True

def steal_auto(character, region, item=None):
    print(f"[STEAL] {character.name} tries to steal {item.name if item else 'something'} at {character.location.name}")
    
    if not item:
        print("[STEAL] No item specified.")
        return

    if item in character.location.contents:
        character.location.contents.remove(item)
        character.inventory.append(item)
        print(f"[STEAL SUCCESS] {character.name} stole {item.name}!")

        # Optional: create memory entry
        memory_entry = MemoryEntry(
            subject=character.name,
            object_=item.name,
            verb="stole",
            details=f"Stole {item.name} from {character.location.name}",
            importance=7,
            type="theft",
            tags=["theft", "weapon", "crime"],
            initial_memory_type="episodic"
        )
        character.mind.memory.add_episodic(memory_entry)

        # Optional: reduce obtain weapon motivation
        character.motivation_manager.resolve_motivation("obtain_ranged_weapon")

    else:
        print(f"[STEAL FAIL] {item.name} not found at location.")


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
    

