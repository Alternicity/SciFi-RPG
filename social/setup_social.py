#social.setup_social.py

import random
from create.create_game_state import get_game_state
gs = get_game_state

from social.social_utils import (
    link_relationship,
    seed_social_relations,
)
#shouldn't know anything about TC 3, 4, 5, readers, libraries, or gang members scenarios

#calculate the number of this group of npcs
#for each:
""" NPC

baseline number of connections here
potentially, later use normal distribution as a baseline or modifier to it here. Accidentally I typed midifier here at first.

├── extroversion     + Add 2 potential extra connections for each x above average extroversion
├── curiosity        + Add 1 potential extra connection
├── agreeableness     + Add 1 potential extra connection

#potentially later use normal distribution as a filter here

Populate npcs social graph here
Perhaps write to a new game_state field here, so later non selected npc centric social code can see the networks
Decide if any of these npcs are friends/enemies etc here
How does this function interact with SocialRelation objects, SocialMemory entries?
Worth keeping in mind that we are going to be outputting to npc percepts memories tab, but also the right
Panel inspector for more info, and potentially, eventually, a dedicated center panel entity page.
"""

def generate_social_network(npcs):

    if not npcs or len(npcs) < 2:
        return

    valid_npcs = [
        npc
        for npc in npcs
        if getattr(npc, "personality", None) is not None
    ]

    if len(valid_npcs) < 2:
        return

    # 1. Calculate group personality averages

    avg_extroversion = sum(
        npc.personality.extroversion
        for npc in valid_npcs
    ) / len(valid_npcs)

    avg_curiosity = sum(
        npc.personality.curiosity
        for npc in valid_npcs
    ) / len(valid_npcs)

    avg_agreeableness = sum(
        npc.personality.agreeableness
        for npc in valid_npcs
    ) / len(valid_npcs)


    # 2. Determine how socially connected each NPC
    #    wants / tends to be


    connection_targets = {}

    for npc in valid_npcs:

        personality = npc.personality

        connections = 1

        if personality.extroversion > avg_extroversion:
            connections += 2

        if personality.curiosity > avg_curiosity:
            connections += 1

        if personality.agreeableness > avg_agreeableness:
            connections += 1

        connections = min(
            connections,
            len(valid_npcs) - 1
        )

        connection_targets[npc] = connections


    # 3. Create direct relationships
    created_pairs = set()

    for npc in valid_npcs:

        candidates = [
            other
            for other in valid_npcs
            if other is not npc
        ]

        random.shuffle(candidates)

        for other in candidates:

            if connection_targets[npc] <= 0:
                break

            pair = frozenset((npc, other))

            if pair in created_pairs:
                continue

            created_pairs.add(pair)

            wrote = _create_initial_relationship(
                npc,
                other
            )

            if not wrote:
                # Existing non-stranger relation was preserved;
                # do not consume one of npc's connection slots.
                continue

            connection_targets[npc] -= 1

    # 4. Derive network information


    _populate_mutual_connections(valid_npcs)

    # 5. Run existing social seeding hook


    for npc in valid_npcs:
        seed_social_relations(npc)

    #can we now edit these print call to show which tc we are dealing with?
    print_social_network(valid_npcs)


def _populate_mutual_connections(npcs):

    for npc in npcs:

        social = npc.social_memory

        for other in npcs:

            if other is npc:
                continue

            relation = social.peek_relation(other)

            if relation is None:
                continue

            if relation.current_type != "acquaintance":
                continue

            # Friends
            for possible_friend in npcs:

                if (
                    possible_friend is npc
                    or possible_friend is other
                ):
                    continue

                other_social = possible_friend.social_memory

                other_relation = (
                    other_social.peek_relation(other)
                )

                if (
                    other_relation is not None
                    and other_relation.current_type == "friend"
                    and possible_friend
                    not in relation.mutual_friends
                ):
                    relation.mutual_friends.append(
                        possible_friend
                    )

            # Enemies
            for possible_enemy in npcs:

                if (
                    possible_enemy is npc
                    or possible_enemy is other
                ):
                    continue

                enemy_social = possible_enemy.social_memory

                enemy_relation = (
                    enemy_social.peek_relation(other)
                )

                if (
                    enemy_relation is not None
                    and enemy_relation.current_type == "enemy"
                    and possible_enemy
                    not in relation.mutual_enemies
                ):
                    relation.mutual_enemies.append(
                        possible_enemy
                    )
                    
def _create_initial_relationship(npc_a, npc_b):
    """
    Seed a *baseline* acquaintance relationship, but never overwrite an
    existing non-stranger relation.

    Returns True if a relation was written, False if skipped because an
    existing non-stranger relation was already present.

    The return value lets generate_social_network keep its connection_targets
    and created_pairs bookkeeping in sync with the actual graph.
    """
    existing = npc_a.social_memory.relations.get(npc_b.id)
    if existing is not None and existing.current_type != "stranger":
        return False

    personality_a = npc_a.personality
    personality_b = npc_b.personality

    familiarity = 3
    trust = 3
    interest = 3

    personality_difference = (
        abs(personality_a.extroversion - personality_b.extroversion)
        + abs(personality_a.agreeableness - personality_b.agreeableness)
        + abs(personality_a.curiosity - personality_b.curiosity)
    )

    if personality_difference < 10:
        interest += 2

    if (
        personality_a.agreeableness > 10
        and personality_b.agreeableness > 10
    ):
        trust += 1

    link_relationship(
        npc_a,
        npc_b,
        relation_type="acquaintance",
        familiarity=familiarity,
        trust=trust,
        interest=interest,
    )

    return True
    
def randomize_first_meeting(npc_a, npc_b):

    if npc_a.partner is npc_b:
        return False

    if npc_a.faction == npc_b.faction:
        return False

    first_meeting = random.choice(
        [True, False]
    )
    return first_meeting

def print_social_network(npcs, label=None):
    print()

    if label:
        print(f"=== FINAL SOCIAL NETWORK: {label} ===")
    else:
        print("=== FINAL SOCIAL NETWORK ===", [n.name for n in npcs][:1], "…")

    for npc in npcs:
        print()
        cls_name = type(npc).__name__
        fam_name = getattr(npc, "family_name", None) or "—"
        partner = getattr(npc, "partner", None)
        partner_str = f" (partner: {partner.name})" if partner is not None else ""
        print(f"NPC: {npc.name} [{cls_name}] family: {fam_name}{partner_str}")

        social = npc.social_memory
        if not social or not social.relations:
            print("  (no relations)")
            continue

        for other_id, rel in social.relations.items():
            markers = []
            if partner is not None and rel.subject is partner:
                markers.append("PARTNER")
            subj_fam = getattr(rel.subject, "family_name", None)
            if fam_name != "—" and subj_fam == fam_name:
                markers.append("SAME-FAMILY-NAME")
            marker_str = f" [{' '.join(markers)}]" if markers else ""

            print(
                "  ->",
                rel.subject.name,
                f"[{type(rel.subject).__name__}]",
                "|",
                rel.current_type,
                "| familiarity:",
                rel.familiarity,
                "| trust:",
                rel.trust,
                "| interest:",
                rel.interest,
                "| respect:",
                rel.respect,
                "| fear:",
                rel.fear,
                "| attraction:",
                rel.attraction,
                "| affection:",
                rel.affection,
                marker_str,
            )

            # Optional: mutual friends/enemies (P-enemies from restart)
            if rel.mutual_friends:
                print("     mutual_friends:", [f.name for f in rel.mutual_friends])
            if rel.mutual_enemies:
                print("     mutual_enemies:", [e.name for e in rel.mutual_enemies])