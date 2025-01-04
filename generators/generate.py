# generate.py
# City and character data generation.
"""
There are now folders called Characters, Factions, Locations, Loyalties, Regions and Stores.
Inside Factions are folders called Civilians, Corps, Gangs and The State.
"""
from .generateLocation import generate_locations
from generators.generateRegions import generate_region
from generators.generateShops import generate_shop
from generators.generateCharacters import generate_character_data
from generators.generateFactions import generate_factions
from generators.generateGangs import generate_gangs
from generators.generateCorps import generate_corporations
from generators.generateEnrichment import generate_enrichment
import logging

# Set up logging for debugging and progress tracking
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_city_data():
    """
    Generate city data, including regions, locations, stores, characters, factions, and gangs.
    """
    logging.info("Starting city generation process...")

    try:
        # Generate regions first, as they determine where locations and stores can go
        logging.info("Generating regions...")
        generate_region()  # Generate city regions (North, South, East, West, Central)
        logging.info("Regions generated successfully.")

        # Generate locations based on the regions, ensuring no ports are in Central
        logging.info("Generating locations...")
        generate_locations()  # Locations for the regions, including port exclusions
        logging.info("Locations generated successfully.")

        # Generate stores in the city
        logging.info("Generating stores...")
        generate_stores()  # Stores located in various regions
        logging.info("Stores generated successfully.")

        # Generate characters
        logging.info("Generating characters...")
        generate_characters()  # Civilians, non-aligned characters
        logging.info("Characters generated successfully.")

        # Generate factions, ensuring that each faction's members are properly placed
        logging.info("Generating factions...")
        generate_factions()  # Factions, including Civilians, Corps, Gangs, and The State
        logging.info("Factions generated successfully.")

        # Generate gangs for the city
        logging.info("Generating gangs...")
        generate_gangs()  # Gang members and their associated territories
        logging.info("Gangs generated successfully.")

        # Generate corporations for the city
        logging.info("Generating corporations...")
        generate_corporations()  # Corporate structures, employees, and business locations
        logging.info("Corporations generated successfully.")

        # Generate enrichment to add color and buffs to existing data
        logging.info("Generating enrichment...")
        generate_enrichment()
        logging.info("Enrichment generated successfully.")

    except Exception as e:
        logging.error(f"Error during city generation: {e}")
    else:
        logging.info("City data generation complete.")
