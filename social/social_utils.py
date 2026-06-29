#social.social_utils.py

from create.create_game_state import get_game_state
game_state = get_game_state
from debug_utils import debug_print
from focus_utils import set_attention_focus
from memory.social.social_memory import SocialMemory
def get_socially_favoured(self):
    if self.partner:
        return self.partner
    if hasattr(self, "get_close_friend"):
        return self.get_close_friend()
    #placeholder code, this function can also call:
    #get_close_friend()

    #get_friend()

    #get_partner()

    #get_pet()

    return None #to be granular, maybe this function should return an identity and presumed location?

def has_recent_interaction(a, b, *, window_hours=2):

    debug_print(
            a,
            f"[RECENT INTERACTION] participants={a.name}, {b.name}",
            category="interaction"
        )

    social = a.mind.memory.semantic.get("social")#I think this should be episodic rather tahn semantic memory
    if not social:
        return False

    gs = get_game_state()
    return social.had_recent_interaction(
        b,
        hour=gs.hour,
        day=gs.day,
        window_hours=window_hours
    )

def seed_social_relations(npc):#this is called in augment.augment_character.py in augment_character()
    social = npc.mind.memory.semantic.get("social")
    if not social:
        return

    # Partner
    if getattr(npc, "partner", None):
        rel = social.get_relation(npc.partner)
        rel.current_type = "partner"
        rel.trust = 5

    # Faction placeholder
    if getattr(npc, "faction", None):
        # NOTE: actual linking deferred until faction members exist
        pass

    # Employment placeholder
    if getattr(npc, "employment", None):
        pass

    """ What seed_social_relations should and should not do
    It SHOULD:

    Look at existing attributes:
    npc.partner
    npc.faction
    npc.employment
    Create relations, not behaviors
    Be safe to call early

    It should NOT:

    Scan regions
    Create thoughts
    Create anchors
    """

#Future 
""" def finalize_social_seeding(all_characters):
    link_coworkers(all_characters)
    link_faction_members(all_characters) """

def finalize_social_seeding(all_characters):#not yet called

    link_partners(all_characters)#see existing family code

    #These three functions dont yet exist:
    link_coworkers(all_characters)

    link_faction_members(all_characters)

    create_initial_memories(all_characters)

def capture_social_snapshot(char, location):#not yet called
    social = char.mind.memory.semantic.get("social")#established social ties belong in npc semantic memory
    assert isinstance(social, SocialMemory), f"{char.name} has invalid social memory"
    #Does char refer to the active npc, or the other one? The subject or the object?
    
    if not social:
        return None

    snapshot = {"friends": [], "enemies": [], "allies": []}

    for other in location.characters_there:
        if other is char:
            continue

        rel = social.get_relation(other)
        if rel.current_type in snapshot:
            snapshot[rel.current_type].append(other.name)

    return snapshot


def social_scan(npc):

    loc = npc.location
    if not loc:
        return

    social = npc.mind.memory.semantic.get("social")
    if not social:
        return

    for other in loc.characters_there:

        if other is npc:
            continue

        rel = social.get_relation(other)

        # optional: record interaction time
        gs = get_game_state()
        rel.last_interaction_hour = gs.hour
        rel.last_interaction_day = gs.day
        """It should:

        create relations
        initialize counters
        do nothing else

        It should not:
        create thoughts
        create motivations
        create anchors
        interpret intent """



from status import StatusLevel

def calculate_respect(target):
    from status import get_primary_status_level
    level = get_primary_status_level(
        target
    )

    if level is None:
        return 0

    return min(level * 5, 20)

def get_status_display(target):

    if not target.status:
        return ("None", "None")

    domain = target.primary_status_domain

    status_level = target.status.get_status(domain)

    if status_level is None:
        return (domain, "None")

    return (
        domain,
        status_level.name
    )

def calculate_attraction(target):

    charisma = getattr(
        target,
        "charisma",
        10
    )

    return min(charisma, 20)

def calculate_familiarity(rel):
    #Once memories exist, then revisit.
    return rel.familiarity


def create_social_group(*members, label=None, interaction_targets=True,):#positional arguments are all NPCs
    from social.social_groups import SocialGroup

    group = SocialGroup()

    if label is not None:
        group.label = label

    group.members = list(members)

    for npc in members:
        npc.current_social_group = group

    if interaction_targets and len(members) == 2:
        members[0].current_interaction_target = members[1]
        members[1].current_interaction_target = members[0]

    return group

#create_social_group Dont let one call the other 
def link_relationship(
    npc_a,
    npc_b,
    *,
    relation_type="acquaintance",
    familiarity=0,
    trust=0,
    respect=0,
    affection=0,
    attraction=0,
    interest=0,
    fear=0,
    envy=0,
    pity=0,
):
    values = {
        "current_type": relation_type,
        "familiarity": familiarity,
        "trust": trust,
        "respect": respect,
        "affection": affection,
        "attraction": attraction,
        "interest": interest,
        "fear": fear,
        "envy": envy,
        "pity": pity,
    }

    for owner, subject in ((npc_a, npc_b), (npc_b, npc_a)):
        social = owner.mind.memory.semantic["social"]
        rel = social.get_relation(subject)

        for field, value in values.items():
            setattr(rel, field, value)

        seed_social_relations(owner)




    
class Interaction:
    def __init__(self, a, b, context=None):
        self.a = a
        self.b = b
        self.context = context
        self.first_encounter = not a.knows(b)
        self.opinion_delta = {}

    def begin(self):
        set_attention_focus(self.a, self.b)
        set_attention_focus(self.b, self.a)

        self.form_first_impression()

class ServiceInteraction(Interaction):
    def apply_norms(self):
    #politeness, service hierarchy
        pass