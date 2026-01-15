#simulation_utils.py
import random
from create.create_game_state import get_game_state
gamestate = get_game_state()
from debug_utils import debug_print

def setup_debug_npcs_in_game_state(
    debug_gang_npc,
    debug_gang_npc2,
    debug_civilian_worker,
    debug_civilian_liberty,
    debug_civilian_waitress
):

    game_state = get_game_state()
    
    game_state.debug_npcs = {
        "primary": debug_gang_npc,
        "secondary": debug_gang_npc2,
        "civilian_worker": debug_civilian_worker,
        "civilian_liberty": debug_civilian_liberty,
        "civilian_waitress": debug_civilian_waitress,
    }
    
    print(f"[DEBUG] Registered {len(game_state.debug_npcs)} debug NPCs")

def non_shop_or_cafe_locations(region):
    from location.locations import Shop, Cafe, CorporateStore, Restaurant

    excluded_types = (Shop, Cafe, CorporateStore, Restaurant)

    return [
        loc for loc in region.locations 
        if not isinstance(loc, excluded_types)
    ]

def setup_tc2_debug_npcs(
    civilian_worker,
    civilian_liberty,
    civilian_waitress
):
    game_state = get_game_state()

    game_state.debug_npcs = {
        "civilian_worker": civilian_worker,
        "civilian_liberty": civilian_liberty,
        "civilian_waitress": civilian_waitress
    }

    game_state.show_background_debug = False

    print("[DEBUG] TC2 debug NPCs registered (3 civilians only)")


def pick_civilian(civilians, *, sex=None, exclude=None):
    candidates = []
    for c in civilians:
        if exclude and c in exclude:
            continue
        if sex and getattr(c, "sex", None) != sex:
            continue
        candidates.append(c)

    return random.choice(candidates) if candidates else None

#for homeless npc starts 
def assign_fallback_location(npc, region):
    if npc.location:
        return

    if not region or not hasattr(region, "locations"):
        debug_print(
            npc,
            "[HOUSING] Cannot assign fallback — region invalid",
            category=["housing", "error"]
        )
        return

    # Prefer Park
    park = next(
        (loc for loc in region.locations if loc.__class__.__name__ == "Park"),
        None
    )

    if not park:
        debug_print(
            npc,
            f"[HOUSING] No Park found in region '{region.name}' — NPC remains unhoused",
            category=["housing", "warning"]
        )
        npc.is_homeless = True
        return

    npc.location = park
    npc.region = region
    npc.is_homeless = True

    if hasattr(park, "characters_there"):
        park.characters_there.append(npc)

    debug_print(
        npc,
        f"[HOUSING] Assigned fallback location: {park.name}",
        category=["housing"]
    )


