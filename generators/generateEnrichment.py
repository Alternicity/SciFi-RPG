"""
generateEnrichment.py

This module enriches the game world by adding buffs to important characters 
and introducing unique traits to locations and factions.

Placeholder implementation for future expansion.
"""
from common import get_project_root, get_file_path
#ALL files use this to get the project root

#I am considering having one enricher file for each generator
#Will Enrichment affect serialized population data files, or instantiated game objects?
from loader import initialize_shops
from typing import List, Union
from location import Shop, CorporateStore, Stash


region = "North"
try:
    shops = initialize_shops(region)
    for shop in shops:
        print(type(shop), shop.name, getattr(shop, "corporation", "N/A"))
except Exception as e:
    print(f"Error during initialization: {e}")

def enrich_characters(characters):
    """
    Enrich characters with buffs or unique traits.
    
    Args:
        characters (list): A list of character dictionaries or objects.
        
    Returns:
        list: The updated list of enriched characters.
    """
    print("Enriching characters... (placeholder)")
    # Placeholder logic
    return characters


def enrich_locations(locations):
    """
    Enrich locations with unique traits or buffs.
    
    Args:
        locations (list): A list of location dictionaries or objects.
        
    Returns:
        list: The updated list of enriched locations.
    """
    print("Enriching locations... (placeholder)")
    # Placeholder logic
    return locations


def enrich_factions(factions):
    """
    Enrich factions with unique traits or buffs.
    
    Args:
        factions (list): A list of faction dictionaries or objects.
        
    Returns:
        list: The updated list of enriched factions.
    """
    print("Enriching factions... (placeholder)")
    # Placeholder logic
    return factions


def generate_enrichment(characters, locations, factions):
    """
    Main function to enrich the game world by enriching characters, locations, 
    and factions. Calls the individual enrichment functions.
    
    Args:
        characters (list): The list of characters in the game world.
        locations (list): The list of locations in the game world.
        factions (list): The list of factions in the game world.
        
    Returns:
        dict: A dictionary containing the enriched characters, locations, and factions.
    """
    print("Generating enrichment for the game world...")
    enriched_characters = enrich_characters(characters)
    enriched_locations = enrich_locations(locations)
    enriched_factions = enrich_factions(factions)
    print("Game world enrichment generated. (placeholder)")
    return {
        "characters": enriched_characters,
        "locations": enriched_locations,
        "factions": enriched_factions
    }

def enrich_shops_with_faction_data(shops: List[Union[Shop, CorporateStore, Stash]]) -> List[Union[Shop, CorporateStore, Stash]]:
    """
    Adds faction-related data or other enhancements to shop objects.
    """
    for shop in shops:
        if isinstance(shop, CorporateStore):
            # Example: Set up faction-specific inventory adjustments
            shop.inventory.append("Exclusive Corporate Item")
        elif isinstance(shop, Stash):
            # Example: Modify stash security based on some logic
            shop.security += 10
    return shops

# Example usage (placeholder)
if __name__ == "__main__":
    dummy_characters = [{"name": "Hero"}]
    dummy_locations = [{"name": "City Center"}]
    dummy_factions = [{"name": "Rebels"}]

    enriched_data = generate_enrichment(dummy_characters, dummy_locations, dummy_factions)
    print("Enriched Data:", enriched_data)


