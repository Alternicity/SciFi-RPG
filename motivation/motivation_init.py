#motivation.motivation_init.py

from motivation.motivation import MotivationManager, Motivation, CORE_MOTIVES
from motivation.motivation_presets import MotivationPresets
from debug_utils import debug_print
def initialize_motivations(character, passed_motivations=None):

    if character.motivation_manager is None:
        character.motivation_manager = MotivationManager(character)

    passed_motivations = passed_motivations or []

    # ✅ Ensure core motivations always exist
    for mtype in CORE_MOTIVES:
        character.motivation_manager.create_initial(mtype, urgency=1)

        debug_print(
            character,
            f"[CORE CREATED] {mtype} persistent=True",
            category="motive"
        )

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
