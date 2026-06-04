#Docs_md.economy.md

# Economy System

## Current Ownership Model

Ownership is moving toward ECS style ownership objects.

Location currently contains:

    owner        # legacy compatibility
    ownership    # source of truth

Ownership component:

    Ownership(
        owner_type,
        owner_ref
    )

All new ownership assignments should go through:

    assign_location_owner(location, owner)

Never directly assign:

    location.owner = owner

outside the helper.

Long term:
- owner becomes compatibility only
- ownership becomes authoritative

## Owner Types

Current:

    corporation
    gang
    state
    family
    individual

## Workforce System

Corporations:
- available_workers
- active_workers
- owned_locations

Nightclubs:
- Bartender
- Bouncer
- DJ
- Club Manager

Staff assigned through:

    assign_staff_to_club()

## Current Nightclub Ownership Rules

40% Corporation
30% Gang
30% Individual NPC

Future:
- gang-owned clubs may become owned by GangBoss/GangCaptain instead of faction itself

## Known Technical Debt

- remaining direct location.owner assignments
- Family ownership still uses older code path
- HQ ownership not yet migrated
- SportsCentre ownership not yet migrated