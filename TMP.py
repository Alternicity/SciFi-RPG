#TMP

def display_region_factions(all_regions): #use display, tabulate
    for region in all_regions:
        print(f"Region: {region.name}")
        print("  Gangs:")
        for gang in region.region_gangs:
            print(f"    - {gang.name} (Race: {gang.race})")
        print("  Corporations:")
        for corp in region.region_corps:
            print(f"    - {corp.name}")