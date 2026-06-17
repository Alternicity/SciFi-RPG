#social.setup_social.py
import random

def randomize_first_meeting(npc_a, npc_b):

    if npc_a.partner is npc_b:
        return False

    if npc_a.faction == npc_b.faction:
        return False

    first_meeting = random.choice(
        [True, False]
    )
    return first_meeting

def seed_relation(source, target, *, relation_type="acquaintance", familiarity=0, attraction=0, trust=0, interest=0, memories=None,):
    pass
#ooops no, see seed_social_relations