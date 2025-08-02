#character_think_utils.py
from character_thought import Thought
from motivation import Motivation

def promote_relevant_thoughts(npc, thoughts):  # thoughts is a deque of Thought objects
    from motivation_presets import MotivationPresets

    for thought in thoughts:  # iterate over each Thought object
        if not hasattr(thought, 'tags'):
            continue  # skip any object that doesn't have .tags

        for tag in thought.tags:
            if tag in MotivationPresets.tag_to_motivation_presets and should_promote_thought(thought):
                template = MotivationPresets.tag_to_motivation_presets[tag]

                # Create a Motivation using the template but override urgency and source info
                motivation = Motivation(
                    template.type,
                    urgency=thought.urgency,  # Use urgency from the thought
                    target=thought.source,    # Source becomes the new motivation's target?
                    source=thought,
                    status_type=getattr(template, "status_type", None),
                )

                npc.motivation_manager.update_motivations(
                    motivation.type,
                    motivation.urgency,
                    target=motivation.target,
                    source=motivation.source,
                )


def should_promote_thought(thought):
    return thought.urgency >= 4 or "weapon" in thought.tags

