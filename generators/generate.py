#generate.py
import os
import json
import logging
import sys

from common import get_project_root, get_file_path
#ALL files use this to get the project root

# Add the project root directory to sys.path(REMOVE THIS?)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Debug: Print current directory and sys.path
print(f"Running generate.py from: {os.getcwd()}")
print(f"sys.path: {sys.path}")


# Import and run other generators
from generators.generateRegions import generate_region
from generators.generateShops import generate_shops
from generators.generateCorps import generate_corporations
from generators.generateCharacters import generate_character_data
from generators.generateFactions import generate_factions
from generators.generateGangs import generate_gangs
from generators.generateEnrichment import generate_enrichment
from generators.generateCity import aggregate_city_data

#print("Imported all generators successfully!")


def generate_city_data():
    """
    Generate city data, including regions, locations, stores, characters, factions, and gangs.
    """
    logging.info("Starting city generation process...")
    regions_with_wealth = {
        "North": "Rich",
        "South": "Normal",
        "East": "Poor",
        "West": "Normal",
        "Central": "Rich",
    }

    try:
        # Generate regions
        logging.info("Generating regions...")
        region_data = generate_region(regions_with_wealth)

        # Pass generated region data to other generators
        logging.info("Generating shops...")
        generate_shops(region_data)

        logging.info("Generating characters...")
        generate_character_data()

        logging.info("Generating factions...")
        generate_factions()

        """ logging.info("Generating gangs...")
        generate_gangs() """

        """ logging.info("Generating corporations...")
        generate_corporations() """ #<- these two deprecated

        logging.info("Generating enrichment...")
        generate_enrichment()

        # Aggregate city data after individual generators have run
        aggregate_city_data()

    except Exception as e:
        logging.error(f"Error during city generation: {e}")
    else:
        logging.info("City data generation completed successfully.")
