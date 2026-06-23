#world.scenarios.setup_tc3.py
from characters import Civilian
from simulation_utils import pick_civilian
from create.create_game_state import get_game_state
from objects.jewellery import Necklace
from objects.InWorldObjects import SmartPhone
from location.locations import Nightclub
import random
from world.placement import place_character, place_character_in_sublocation
from social.social_utils import seed_social_relations
from social.social_groups import SocialGroup
from augment.augmentLocations import add_classy_plants
from augment.augmentLocations import add_table_decorations
game_state = get_game_state()

def setup_tc3_world(all_characters):

    nightclub = next(
        (
            loc for loc in game_state.all_locations
            if isinstance(loc, Nightclub)
            and getattr(loc, "is_tc2_nightclub", False)
        ),
        None
    )
    add_table_decorations(nightclub)
    #is this block now deprecated? civilians is not accessed now
    """ civilians = [
        c for c in all_characters
        if isinstance(c, Civilian)
        and not getattr(c, "is_scenario_npc", False)
    ] """


    vip_candidates = [
        b for b in game_state.all_VIPs
        if not getattr(b, "is_scenario_npc", False)
    ]

    debug_civilian_vip = random.choice(vip_candidates) if vip_candidates else None

    #tmp
    """ print(
        "[TC3] VIP selected:",
        debug_civilian_vip,
        debug_civilian_vip.__class__.__name__
    ) """

    babe_candidates = [
        b for b in game_state.all_babes
        if not getattr(b, "is_scenario_npc", False)
    ]

    debug_civilian_babe = random.choice(babe_candidates) if babe_candidates else None

#can this section be made more concise?

    if debug_civilian_vip:
        debug_civilian_vip.debug_role = "civilian_vip"
        debug_civilian_vip.is_scenario_npc = True
    if debug_civilian_babe:
        debug_civilian_babe.debug_role = "civilian_babe"

    if debug_civilian_vip:
        game_state.debug_npcs["civilian_vip"] = debug_civilian_vip
        debug_civilian_vip.inventory_component.inventory.add_item(SmartPhone())

    if debug_civilian_babe:
        game_state.debug_npcs["civilian_babe"] = debug_civilian_babe
        debug_civilian_babe.inventory_component.inventory.add_item(Necklace())
        debug_civilian_babe.is_scenario_npc = True
    pass

    vip_lounge = next(
        (
            subloc
            for subloc in nightclub.sublocations
            if subloc.name == "VIP Lounge"
        ),
        None
    )

    #tmp, once a nightclub might be tagged classy
    if vip_lounge:
        add_classy_plants(vip_lounge)#note also added in seed_nightclub_furniture

    print(
    "VIP LOUNGE OBJECTS:",
    [
        type(obj).__name__
        for obj in vip_lounge.objects_present
    ]
)
    print(
        vip_lounge.objects_present
    )
    print(
        len(vip_lounge.objects_present)
    )

    if debug_civilian_vip and vip_lounge:
        place_character_in_sublocation(
            debug_civilian_vip,
            nightclub,
            vip_lounge
        )

    if debug_civilian_babe and vip_lounge:
        place_character_in_sublocation(
            debug_civilian_babe,
            nightclub,
            vip_lounge
        )
    
    vip_social = (
        debug_civilian_vip
        .mind.memory.semantic["social"]
    )

    rel = vip_social.get_relation(
        debug_civilian_babe
    )

    rel.current_type = "acquaintance"

    rel.familiarity = 8
    rel.attraction = 15
    rel.interest = 12
    rel.trust = 6
    seed_social_relations(debug_civilian_vip)

    babe_social = (
        debug_civilian_babe
        .mind.memory.semantic["social"]
    )

    rel = babe_social.get_relation(
        debug_civilian_vip
    )

    rel.current_type = "acquaintance"

    rel.familiarity = 8
    rel.attraction = 4
    rel.interest = 6
    rel.trust = 5
    seed_social_relations(debug_civilian_babe)

    vip_group = SocialGroup()

    vip_group.members.append(debug_civilian_vip)
    vip_group.members.append(debug_civilian_babe)

    debug_civilian_vip.current_social_group = vip_group
    debug_civilian_babe.current_social_group = vip_group

    debug_civilian_vip.current_interaction_target = debug_civilian_babe
    debug_civilian_babe.current_interaction_target = debug_civilian_vip
    
    vip = debug_civilian_vip
    babe = debug_civilian_babe

    #motivations
    vip.motivation_manager.update_motivations(
        "seek_attention",
        urgency=2,
        target=babe
    )

    vip.motivation_manager.update_motivations(
        "offer_validation",
        urgency=5,
        target=babe
    )

    vip.motivation_manager.update_motivations(#but does he already have one?
        "find_partner",
        urgency=6,
        target=babe
    )

    babe.motivation_manager.update_motivations(
        "seek_attention",
        urgency=8,
        target=vip
    )

    babe.motivation_manager.update_motivations(
        "have_fun",
        urgency=5,
        target=vip
    )

    babe.motivation_manager.update_motivations(
        "find_partner",
        urgency=6,
        target=vip
    )

    first_meeting = random.choice(
        [True, False]
    )

    if not first_meeting:

        rel.memories.append(
            "Met her at the VIP Lounge last week."
        )

        rel.memories.append(
            "Enjoyed talking with her."
        )

        rel.interaction_count = 3

    else:

        rel.interaction_count = 0
        rel.familiarity = 0