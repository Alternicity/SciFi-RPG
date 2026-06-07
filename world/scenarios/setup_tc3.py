#world.scenarios.setup_tc3.py
from characters import Civilian
from simulation_utils import pick_civilian
from create.create_game_state import get_game_state
from objects.jewellery import Necklace
from objects.InWorldObjects import SmartPhone
from location.locations import Nightclub
import random
from world.placement import place_character, place_character_in_sublocation
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
    


    civilians = [#is this block now deprecated? civilians is not accessed now
        c for c in all_characters
        if isinstance(c, Civilian)
        and not getattr(c, "is_scenario_npc", False)
    ]


    vip_candidates = [
        b for b in game_state.all_VIPs
        if not getattr(b, "is_scenario_npc", False)
    ]

    debug_civilian_vip = random.choice(vip_candidates) if vip_candidates else None

    #tmp
    print(
        "[TC3] VIP selected:",
        debug_civilian_vip,
        debug_civilian_vip.__class__.__name__
    )

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

    print(f"[TC3] Found nightclub: {nightclub}")
    print(f"[TC3] Sublocations: {[s.name for s in nightclub.sublocations]}")
    print(f"[TC3] VIP lounge found: {vip_lounge}")

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

    print(
        debug_civilian_babe.name,
        debug_civilian_babe.location,
        debug_civilian_babe.sublocation
    )

    print(
        debug_civilian_vip.name,
        debug_civilian_vip.location,
        debug_civilian_vip.sublocation
    )