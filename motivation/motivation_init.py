#motivation.motivation_init.py

from motivation.motivation import MotivationManager, Motivation
from motivation.motivation_presets import MotivationPresets

def initialize_motivations(character, passed_motivations=None):
    passed_motivations = passed_motivations or []
    # 1 - Apply inline motivations first
    if passed_motivations:
        for m in passed_motivations:
            if isinstance(m, tuple):
                mtype, urgency = m
                character.motivation_manager.create_initial(mtype, urgency)

            elif isinstance(m, dict):
                character.motivation_manager.create_initial(
                    m["type"],
                    m.get("urgency", 1),
                    target=m.get("target"),
                    source=m.get("source", "initial"),
                    status_type=m.get("status_type")
                )

            elif isinstance(m, Motivation):
                character.motivation_manager.add(m)

    # 2 — Load preset motivations
    preset_list = MotivationPresets.for_class(character.__class__.__name__)
    for preset in preset_list:
        character.motivation_manager.add(preset)

    return character.motivation_manager
