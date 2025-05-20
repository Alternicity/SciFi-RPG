# observe.py
#interpretation and reaction

def handle_observation(character, event_type, instigator, region, location):
    pass
    # deprecated for now. observations handled in event objects, starting with robbery

def update_escape_logic(character):
    mm = character.motivation_manager
    if hasattr(mm, "update_motivations"):
        mm.update_motivations("escape_danger", urgency=9)
        mm.update_motivations("snitch", urgency=5)
        mm.update_motivations("virtue_signal", urgency=2)
    if getattr(character, "observation", 0) >= 6:
        print(f"{character.name} becomes alert and distressed!")
    urgent = mm.get_highest_priority_motivation()
    print(f"{character.name}'s most urgent motivation is now: {urgent}")

def observe (location):
    #include noticing increased xyz activity
    pass

def examine_item(item):
    return getattr(item, "human_readable_id", item.name)
#hook here to utilise Characters observe attribute and any memeories and skills