#display.py
from tabulate import tabulate
import logging

import loader
import os
from collections import defaultdict
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, GangMember, Child, Influencer,
                           Babe, Detective)

from location import Region, UndevelopedRegion, VacantLot
import json
from region_startup import get_region_wealth
from LoaderRuntime import load_locations_from_yaml
from create import create_regions
from menu_utils import get_user_choice
from common import get_file_path, BASE_REGION_DIR, BASE_SHOPS_DIR
from typing import List, Union
from game import character_and_region_selection
from character_creation_funcs import player_character_options

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_region_mappings():

    # List of region names
    valid_regions = ["North", "East", "West", "South", "Central"]

    region_mappings = {}
    for region in valid_regions:
        # Construct the region file path using BASE_REGION_DIR
        region_file_path = os.path.join(BASE_REGION_DIR, f"{region}.json")
        #print(f"Looking for region file at: {region_file_path}")  # Debugging print
        
        try:
            # Open the respective region file
            with open(region_file_path, "r") as file:
                data = json.load(file)
                region_mappings[region] = data  # Add region mappings to the dictionary
                # Only print brief info about the region here
                print(f"Loaded region data for {region}: {data.get('name', 'Unknown Region Name')}")

        except FileNotFoundError:
            print(f"Error loading region mappings for {region}: {region_file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error: {region_file_path} contains invalid JSON.")
    
    return region_mappings

def select_region_menu(regions: List[Union['Region', 'UndevelopedRegion']]):
    """Displays region selection and returns the selected region."""
    if not regions:
        print("No regions available.")
        return None

    table = [[i + 1, region.name] for i, region in enumerate(regions)]
    print(tabulate(table, headers=["#", "Region"], tablefmt="grid"))

    choice = get_user_choice(len(regions))
    return regions[choice] if choice is not None else None

from tabulate import tabulate

def show_character_details(character):
    """Display character details in tabulated format."""
    print("\nCharacter Details:")
    
    # First table with the first header row
    character_table_1 = [
        ["Name", "Health", "Faction", "Money", "Whereabouts", "Hunger", "Inventory"],
        [
            character.name,
            getattr(character, "xxx", character.health),
            character.faction,
            f"${getattr(character, 'bankCardCash', 0):.2f}",
            character.whereabouts,  # Uses the @property
            getattr(character, "hunger", "N/A"),
            ", ".join(getattr(character, "inventory", [])),
        ],
    ]

    # Second table with the second header row
    character_table_2 = [
        ["Race", "Status", "Intelligence", "Fun", "Motivations", ""],  # Empty fields for alignment
        [
            getattr(character, "lorem", character.race),
            character.status.value.title(),
            #character.status.value retrieves the string value of the enum ("high")
            #.title() capitalizes the first letter of the string, turning "high" into "High"

            getattr(character, "xxx", self.intelligence),

            getattr(character, "idk", character.fun),
            ", ".join(character.motivations),  # Motivations (joined list)
            ""
        ],
    ]
    # Print the first table
    print(tabulate(character_table_1, headers="firstrow", tablefmt="grid"))
    
    # Print the second table
    print(tabulate(character_table_2, headers="firstrow", tablefmt="grid"))

def display_filtered_character_summary(characters, gang_limit=3, corp_limit=3, civilian_limit=3):
    """Displays filtered character summaries with limits."""
    print("\n=== CHARACTER SUMMARY ===\n")

    # Categorize characters by faction
    faction_groups = defaultdict(list)
    non_faction_characters = []

    for char in characters:
        if char.faction and char.faction != "None":
            faction_groups[char.faction].append(char)
        else:
            non_faction_characters.append(char)

    # Display faction characters
    for faction, members in faction_groups.items():
        print(f"\n--- {faction.upper()} ---")

        bosses = [c for c in members if isinstance(c, Boss)]
        captains = [c for c in members if isinstance(c, Captain)]
        gang_members = [c for c in members if isinstance(c, GangMember)]

        ceos = [c for c in members if isinstance(c, CEO)]
        managers = [c for c in members if isinstance(c, Manager)]
        employees = [c for c in members if isinstance(c, Employee)]
        corp_security = [c for c in members if isinstance(c, CorporateSecurity)]

        vip = [c for c in members if isinstance(c, VIP)]
        riot_cops = [c for c in members if isinstance(c, RiotCop)]
        detectives = [c for c in members if isinstance(c, Detective)]

        # Show limited number of characters
        for b in bosses[:1]: show_character_details(b)
        for c in captains[:3]: show_character_details(c)
        for g in gang_members[:gang_limit]: show_character_details(g)

        for ceo in ceos[:1]: show_character_details(ceo)
        for m in managers[:3]: show_character_details(m)
        for e in employees[:corp_limit]: show_character_details(e)
        for sec in corp_security[:corp_limit]: show_character_details(sec)

        for v in vip[:1]: show_character_details(v)
        for r in riot_cops[:3]: show_character_details(r)
        for d in detectives[:2]: show_character_details(d)

    # Display non-faction characters
    print("\n--- NON-FACTION CHARACTERS ---")
    civilians = [c for c in non_faction_characters if isinstance(c, Civilian)]
    children = [c for c in non_faction_characters if isinstance(c, Child)]
    babes = [c for c in non_faction_characters if isinstance(c, Babe)]

    # Show one of each category
    if civilians: show_character_details(civilians[0])
    if children: show_character_details(children[0])
    if babes: show_character_details(babes[0])

    # Display message for remaining
    print(f"... and {max(0, len(civilians)-1)}x similar Civilians.")
    print(f"... and {max(0, len(children)-1)}x similar Children.")
    print(f"... and {max(0, len(babes)-1)}x similar Babes.")



def show_locations_in_region(region, locations):
    """Display locations in the specified region."""
    #locations_data = load_locations_from_yaml(region)

    if not locations:
        print(f"No locations found in {region.name}.")
        return
    
    # Prepare the data for tabulation
    table_data = []
    for location in locations:
        # Extract relevant fields
        name = getattr(location, "name", "Unknown Name")
        condition = getattr(location, "condition", "Unknown Condition")
        fun = getattr(location, "fun", "N/A")
        security_level = getattr(location.security, "level", "N/A") if hasattr(location, "security") else "N/A"

        # Add to table data
        table_data.append([name, condition, fun, security_level])

    # Display the table
    headers = ["Name", "Condition", "Fun", "Security Level"]
    print(tabulate(table_data, headers=headers, tablefmt="grid")) #try also tablefmt="pretty"

#Shop:
def show_shop_inventory(shop):
    """Display the inventory of a shop in a tabulated format."""
    if not shop.inventory:
        print(f"{shop.name} has no items available.")
        return

    # Prepare the data for tabulation
    table_data = []
    for item, details in shop.inventory.items():
        table_data.append([item, details.get("price", "N/A"), details.get("quantity", 0)])

    # Display the table
    headers = ["Item", "Price", "Quantity"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def display_selected_character_current_region(character, region):
    print(f"{character.name} is in {region.name}.")

def list_characters(characters):
    #Display a list of existing characters in a table format.
   
    for char in characters:
        if isinstance(char, dict):
            print(f"Character dictionary: {char}")
            name = char.get('name', 'Unknown')  # Safely access dictionary attributes
    else:
        print(f"Character object: {char}")
        name = char.name  # Access object attribute
        print(f"Character Name: {name}")


    print("Listing Characters, list_characters().")

    if not characters:
        print("No existing characters.")
        return

    # Extract data from object instances
    table_data = [
        [
            char.name,
            char.char_role,
            char.faction,
            char.bankCardCash,
            char.fun,
            char.hunger,
        ]
        for char in characters
    ]
    headers = ["Name", "Role", "Faction", "Bank Card Cash", "Fun", "Hunger"]
    return tabulate.tabulate(table_data, headers=headers, tablefmt="fancy_grid")