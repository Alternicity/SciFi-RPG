#social.social_utils.py

from create.create_game_state import get_game_state
game_state = get_game_state
from debug_utils import debug_print
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
    Assume other NPCs exist (yet) """

#Future 
""" def finalize_social_seeding(all_characters):
    link_coworkers(all_characters)
    link_faction_members(all_characters) """

def capture_social_snapshot(char, location):
    social = char.mind.memory.semantic.get("social")#established social ties belong in npc semantic memory
    assert isinstance(social, SocialMemory), f"{npc.name} has invalid social memory, from capture_social_snapshot"
    # npc marked not defined. Does char refer to the active npc, or the other one? The subject or the object?
    
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
