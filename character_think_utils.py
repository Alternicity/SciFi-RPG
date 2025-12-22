#character_think_utils.py
from character_thought import Thought
from motivation.motivation import Motivation
from debug_utils import debug_print


def promote_relevant_thoughts(npc, thoughts):  # thoughts is a deque of Thought objects
    from motivation.motivation_presets import MotivationPresets
    from characters import GangMember
    # HARD GATE
    if isinstance(npc, GangMember):
        if not getattr(npc, "is_test_npc", False):
            return
        if npc.debug_role != "primary":
            return

    for thought in thoughts:
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

                npc.motivation_manager.consider_adding_motivation(
                    motivation.type,
                    urgency=motivation.urgency,
                    target=motivation.target,
                    source=thought,
                )
#character_think_utils.py
def social_thoughts(self):
    npc = self.npc

    for connection in npc.social_connections["co_workers"]:#this should include more than just friend connections, at least in potential
        if npc.world.recently_interacted(npc, connection):
            npc.mind.add_thought({
                "type": "social_thought",
                "about": connection,
                "tags": ["unwind", "co_worker", "social"]
            })

def should_promote_thought(thought):
    return thought.urgency >= 4 or "weapon" in thought.tags#very test case 1 centric

def debug_recent_thoughts(npc, mind, n=5):
    recent = list(mind.thoughts)[-n:]
    thought_contents = [t.content for t in recent]
    debug_print(npc, f"[THOUGHTS] Recent thoughts: {thought_contents}", category="think")

    # Show obsessions (separate objects)
    if mind.obsessions:
        obsessions_data = [o.content for o in mind.obsessions if not o.resolved]
        debug_print(npc, f"[THOUGHTS] Active obsessions: {obsessions_data}", category="think")


    # Show corollaries (either Thought.corollary_of or Mind.corollaries)
    corollary_map = {}
    for t in mind.thoughts:
        if getattr(t, "corollary_of", None):
            corollary_map.setdefault(t.corollary_of, []).append(t.content)

    if mind.corollaries:
        # Include top-level corollary set if used
        for c in mind.corollaries:
            corollary_map.setdefault("global", []).append(getattr(c, "content", str(c)))

    if corollary_map:
        debug_print(npc, f"[THOUGHTS] Corollary structure: {corollary_map}", category="think")