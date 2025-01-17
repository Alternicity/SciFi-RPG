# generate.py
# City and character data generation.
import random
import logging
from generateRegions import generate_region
from generateShops import generate_shops
"""
There are now folders called Characters, Factions, Locations, Loyalties, Regions and Shops.
Inside Factions are folders called Civilians, Corps, Gangs and The State.
"""
# Centralize the regions and wealth levels here
regions_with_wealth = {
    "North": "Rich", #high
    "South": "Normal", #medium
    "East": "Poor", #low
    "West": "Normal", #medium
    "Central": "Rich", #high
}

from .generateLocation import generate_locations
from generators.generateRegions import generate_region
from generators.generateShops import generate_shops
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
        logging.info("Generating regions...")
        region_data = generate_region(regions_with_wealth)
        logging.info("Regions generated successfully.")

        logging.info("Generating shops...")
        generate_shops(region_data)  # Pass the region data with wealth levels
        logging.info("Shops generated successfully.")

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
