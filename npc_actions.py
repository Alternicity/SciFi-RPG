# npc_actions.py
def visit_location_auto(character, location):
    if location is None:
        return False

    print(f"[AUTO VISIT] {character.name} is going to {location.name}")
    character.location = location
    location.enter(character)

    return True