#population.population.py

from collections import Counter, defaultdict
from debug_utils import debug_print
from create.create_game_state import get_game_state

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

    debug_print(None, "==============================", category="population")

