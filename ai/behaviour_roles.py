#ai.behaviour_roles.py

#defines authority boundaries - which npc roles can do what, so that GangMemberAI test case 1 logic doesnt affect all GangMembers
#until we can develop non test case 1 motivations and actions. 

"""
    Returns the NPC's behaviour role.

    Defaults to 'background' to ensure safety.
    Background NPCs should observe but not initiate
    high-impact behaviours.
    """

def role(npc):
    r = getattr(npc, "debug_role", None) or "background"
    if r not in ROLE_PERMISSIONS:
        return "background"
    return r


ROLE_PERMISSIONS = {
    "primary": {
        "weapon_reasoning": True,
        "percept_to_motivation": True,
        "thought_to_motivation": True,
        "anchor_creation": True,
    },
    # Secondary NPCs: may act, but not Test Case 1 logic
    "secondary": {
        "visit": True,
        "weapon_reasoning": False,
        "percept_to_motivation": False,
        "thought_to_motivation": False,
        "anchor_creation": False,# until their anchors are defined
    },
    "civilian_worker": {
        "percept_to_motivation": True,
        "thought_to_motivation": True,
        "anchor_creation": True,
    },
    "civilian_liberty": {
        "percept_to_motivation": True,
        "thought_to_motivation": True,
        "anchor_creation": True,
    },
    # Default safe state, npc is locked down hard
    "background": {
        "visit": False,
        "weapon_reasoning": False,
        "percept_to_motivation": False,
        "thought_to_motivation": False,
        "anchor_creation": False,
    },
}

"""
Behaviour roles define AI authority boundaries.

They control:
- Which NPCs may convert percepts → motivations
- Which NPCs may convert thoughts → motivations
- Which NPCs may create anchors
- Which NPCs may perform certain high-impact behaviours

This exists to:
- Isolate Test Case 1 logic (e.g. obtain_ranged_weapon, robbery)
- Prevent unfinished AI logic from affecting all NPCs
- Allow multiple NPCs to act simultaneously with different permissions

IMPORTANT:
- Behaviour roles are NOT employment roles.
- Behaviour roles are NOT debug visibility flags.
- Behaviour roles MUST be checked at the three AI boundaries:
    1) Percept → Motivation
    2) Thought → Motivation
    3) Anchor Creation
"""