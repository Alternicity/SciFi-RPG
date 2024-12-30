#generate.py
#city and character data generation.

from generateLocation import generate_locations
from generateRegion import generate generate_region
from generateStore import generate_stores
from generateCharacters import generate_characters  # Assuming you have this function
from generateFactions import generate_factions  # Assuming you have this function
from generateGang import generateGang
from generateCorp import generate_corporations

def generate_city_data():
    generate_stores()  # Example of generating stores
    generate_characters()  # Example of generating characters
    generate_factions()  # Example of generating factions
