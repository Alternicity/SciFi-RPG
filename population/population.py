#population.population.py

from collections import Counter, defaultdict
from debug_utils import debug_print
from create.create_game_state import get_game_state
from location.locations import House, ApartmentBlock
game_state = get_game_state()

def summarize_civilians(civilians, regions):
    # --- 1. Population by race ---
    race_counts = Counter(c.race for c in civilians)

    most_populous_race, pop_count = race_counts.most_common(1)[0]

    # --- 2. Partner statistics ---
    partnered = []

    for c in civilians:
        social = c.mind.memory.semantic.get("social")
        if not social:
            continue

        if any(
            rel.current_type == "partner"
            for rel in social.relations.values()
        ):
            partnered.append(c)
            #If you want to be stricter later (mutual partner only), you can refine this.



    partner_race_counts = Counter(c.race for c in partnered)
    if partner_race_counts:
        most_partnered_race, partnered_count = partner_race_counts.most_common(1)[0]
    else:
        most_partnered_race, partnered_count = None, 0

    # --- 3. Richest race ---
    race_wealth = defaultdict(int)
    for c in civilians:
        if c.wallet:
            race_wealth[c.race] += c.wallet.balance

    richest_race = max(race_wealth, key=race_wealth.get)
    richest_race_amount = race_wealth[richest_race]

    # --- 4. Richest region ---
    region_wealth = defaultdict(int)
    for c in civilians:
        if c.region:
            region_wealth[c.region.name] += c.wallet.balance

    richest_region = max(region_wealth, key=region_wealth.get)
    richest_region_amount = region_wealth[richest_region]

    # --- Print block ---
    debug_print(None, "====== CIVILIAN SUMMARY ======", category="population")


    debug_print(None, f"Total civilians: {len(civilians)}", category = "population")

    debug_print(None, f"Most populous race: {most_populous_race} ({pop_count})", category = "population")
    debug_print(None, f"Race with most partnerships: {most_partnered_race} ({partnered_count})", category = "population")

    debug_print(None, f"Richest race: {richest_race} "
          f"(total wealth {richest_race_amount})", category = "population")

    debug_print(None, f"Richest region: {richest_region} "
          f"(total wealth {richest_region_amount})", category = "population")

    # --- 5. Family statistics ---

    total_families = len(game_state.families)

    with_family = sum(1 for c in civilians if getattr(c, "family", None))
    without_family = len(civilians) - with_family

    homeless_count = sum(1 for c in civilians if getattr(c, "is_homeless", False))

    # --- Housing breakdown ---

    house_residents = 0
    apartment_residents = 0
    park_residents = 0
    vacantlot_residents = 0

    for c in civilians:
        loc = getattr(c, "location", None)
        if not loc:
            continue

        from location.locations import House, ApartmentBlock, Park, VacantLot

        if isinstance(loc, House):
            house_residents += 1
        elif isinstance(loc, ApartmentBlock):
            apartment_residents += 1
        elif isinstance(loc, Park):
            park_residents += 1
        elif isinstance(loc, VacantLot):
            vacantlot_residents += 1


    debug_print(None, f"Total families: {total_families}", category="population")
    debug_print(None, f"Civilians with family: {with_family}", category="population")
    debug_print(None, f"Civilians without family: {without_family}", category="population")
    debug_print(None, f"Homeless civilians: {homeless_count}", category="population")

    debug_print(None, f"Living in House: {house_residents}", category="population")
    debug_print(None, f"Living in ApartmentBlock: {apartment_residents}", category="population")
    debug_print(None, f"Living in Park: {park_residents}", category="population")
    debug_print(None, f"Living in VacantLot: {vacantlot_residents}", category="population")
    
    all_locations = game_state.all_locations

    total_houses = sum(
        1 for l in all_locations if isinstance(l, House)
    )

    total_apartment_blocks = sum(
        1 for l in all_locations if isinstance(l, ApartmentBlock)
    )

    debug_print(None, f"Total Houses in world: {total_houses}", category="population")
    debug_print(None, f"Total ApartmentBlocks in world: {total_apartment_blocks}", category="population")

    debug_print(None, "==============================", category="population")

