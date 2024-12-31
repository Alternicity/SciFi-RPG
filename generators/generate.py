*# generate.py
# City and character data generation.
"""Inside C:\Users\Stuart\Python Scripts\scifi RPG\data\Test City
There are now folders called Characters, Factions, Locations, Loyalties, Regions and Stores.
Inside Factions are folders called Civilians, Corps, Gangs and The State.
"""

# Import necessary generators
from generateLocation import generate_locations
from generateRegion import generate_region
from generateStore import generate_stores
from generateCharacters import generate_characters
from generateFactions import generate_factions
from generateGang import generate_gangs
from generateCorp import generate_corporations
from generateEnrichment import generate_enrichment

def generate_city_data():
    """
    Generate city data, including regions, locations, stores, characters, factions, and gangs.
    """
    print("Starting city generation process...")

    # Generate regions first, as they determine where locations and stores can go
    generate_region()  # Generate city regions (North, South, East, West, Central)

    # Generate locations based on the regions, ensuring no ports are in Central
    generate_locations()  # Locations for the regions, including port exclusions

    # Generate stores in the city
    generate_stores()  # Stores located in various regions

    # Generate characters
    generate_characters()  # Civilians, non-aligned characters

    # Generate factions, ensuring that each faction's members are properly placed
 *   generate_factions()  # Factions, including Civilians, Corps, Gangs, and The State

    # Generate gangs for the city
    generate_gangs()  # Gang members and their associated territories

    # Generate corporations for the city
    generate_corporations()  # Corporate structures, employees, and business locations

    generate_enrichment()
    # To add: GeneateEnrichment. Modifies existing datafiles.
    #This stage makes more colorful the CEOs, VIPs, and Bosses from another file, adding characteistics and buffs to the ones that already exist. 
    #Eventually it might also add colour to locations etc
    

    print("City data generation complete.")

*