#world.scenarios.setup_tc3.py
from characters import Civilian
from simulation_utils import pick_civilian
from create.create_game_state import get_game_state
from objects.jewellery import Necklace
from objects.InWorldObjects import SmartPhone
from weapons import Pistol
from location.locations import Nightclub
import random
from world.placement import place_character, place_character_in_sublocation
from social.social_utils import link_relationship, create_social_group
from social.social_groups import SocialGroup

from augment.augmentLocations import add_classy_plants, add_classy_furniture
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

    boss_candidates = [
        b for b in game_state.all_gang_bosses
        if not getattr(b, "is_scenario_npc", False)
    ]

    debug_gang_boss1 = random.choice(boss_candidates) if boss_candidates else None
    debug_gang_boss2 = random.choice(boss_candidates) if boss_candidates else None#we must ensure that boss1 is not selected here


    assassin_candidates = [
        b for b in game_state.all_assassins
        if not getattr(b, "is_scenario_npc", False)
    ]
    
    debug_assassin = random.choice(assassin_candidates) if assassin_candidates else None 

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

    if debug_assassin:
        debug_assassin.debug_role = "first_assassin"
        debug_assassin.is_scenario_npc = True
        game_state.debug_npcs["first_assassin"] = debug_assassin
        debug_assassin.inventory_component.inventory.add_item(Pistol())

    if debug_gang_boss1:
        debug_gang_boss1.debug_role = "first_Boss"
        debug_gang_boss1.is_scenario_npc = True
        game_state.debug_npcs["first_Boss"] = debug_gang_boss1

    if debug_gang_boss2:
        debug_gang_boss1.debug_role = "Second_Boss"
        debug_gang_boss1.is_scenario_npc = True
        game_state.debug_npcs["Second_Boss"] = debug_gang_boss2


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

    if vip_lounge:
        add_classy_furniture(vip_lounge)

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
    
    if debug_assassin and vip_lounge:
        place_character_in_sublocation(
            debug_assassin,
            nightclub,
            vip_lounge
        )

    if debug_gang_boss1 and vip_lounge:
        place_character_in_sublocation(
            debug_gang_boss1,
            nightclub,
            vip_lounge
        )
    if debug_gang_boss2 and vip_lounge:
        place_character_in_sublocation(
            debug_gang_boss2,
            nightclub,
            vip_lounge
        )

    #Shorter name versions
    vip = debug_civilian_vip
    babe = debug_civilian_babe
    assassin = debug_assassin
    boss1 = debug_gang_boss1
    boss2 = debug_gang_boss2

    #VIP
    vip_social = (
        debug_civilian_vip
        .mind.memory.semantic["social"]
    )

    rel = vip_social.get_relation(
        debug_civilian_babe
    )

    rel.current_type = "acquaintance"

    link_relationship(
        debug_civilian_vip,
        debug_civilian_babe,
        familiarity=8,
        attraction=15,
        interest=12,
        trust=6,
    )

    #Babe
    babe_social = (
        debug_civilian_babe
        .mind.memory.semantic["social"]
    )

    rel = babe_social.get_relation(
        debug_civilian_vip
    )

    rel.current_type = "acquaintance"

    link_relationship(
        debug_civilian_babe,
        debug_civilian_vip,
        
        familiarity=8,
        attraction=4,
        interest=6,
        trust=5,
    )

    vip_group = create_social_group(#vip_group not accessed here,
    vip,
    babe,
    label="Courting"
)



    boss1_social = (
        boss1
        .mind.memory.semantic["social"]
    )

    rel = boss1_social.get_relation(
        boss2
    )

    rel.current_type = "acquaintance"

    link_relationship(
        boss1,
        boss2,
        familiarity=8,
        attraction=15,
        interest=12,
        trust=6,
    )

    boss2_social = (
        boss2
        .mind.memory.semantic["social"]
    )

    rel = boss2_social.get_relation(
        boss1
    )

    rel.current_type = "frenemy"

    link_relationship(#persistent social knowledge.
        boss2,
        boss1,
        familiarity=8,
        attraction=15,
        interest=12,
        trust=6,
    )

    boss_group = create_social_group(#establishes the current interaction
    boss1,
    boss2,
    label="Planning"
)


    #TMP
    print(vip.current_social_group)
    print(babe.current_social_group)
    print(boss1.current_social_group)
    print(boss2.current_social_group)


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

    assassin.motivation_manager.update_motivations(
        "surveil",
        urgency=10,
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