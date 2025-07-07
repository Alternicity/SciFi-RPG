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
from visual_effects import loading_bar, color_text
#from menu_utils import get_user_choice
#This file cannot import from menu_utils here, maybe lazy imports are ok
from common import get_file_path, BASE_REGION_DIR
from typing import List, Union
from character_creation_funcs import player_character_options
from base_classes import Faction, Location
from perceptibility import extract_appearance_summary
from shop_name_generator import format_shop_debug
from salience import compute_salience

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def load_region_mappings():
    # List of region names
    valid_regions = ["North", "East", "West", "South", "Central"]
    region_mappings = {}
    return region_mappings

def select_region_menu(regions: List[Union['Region', 'UndevelopedRegion']]):
    """Displays region selection and returns the selected region."""
    if not regions:
        print("No regions available.")
        return None

    table = [[i + 1, region.name] for i, region in enumerate(regions)]
    print(tabulate(table, headers=["#", "Region"], tablefmt="grid"))

    from menu_utils import get_user_choice
    choice = get_user_choice(len(regions))
    return regions[choice] if choice is not None else None

from tabulate import tabulate

def show_character_details(character):
    """Display character details in tabulated format."""
    print("\nCharacter Details:")
   # In display.py:
    print(character.display_location(verbose=True))

    # First table with the first header row
    if character.faction:
            faction_name = character.faction.name
            faction_type = character.faction.type.capitalize()
    else:
        faction_name = "None"
        faction_type = "Indy"
        #f"{character.faction.name} {character.faction.type.capitalize()}",
        faction_name = character.faction.name if character.faction else "None"
        faction_type = character.faction.type.capitalize() if character.faction else "Unaffiliated"

    character_table_1 = [
    ["Name", "Health", "Faction", "Money", "Location", "Hunger", "Inventory"],
    [
        character.name,
        getattr(character, "xxx", character.health),
        f"{faction_name} ({faction_type})",
        f"${character.wallet.bankCardCash:.2f}",
        character.display_location(),
        getattr(character, "hunger", "N/A"),
        character.inventory.get_inventory_summary() if character.inventory else "(Ch Tab Empty)"

    ],
]
        # Retrieve motivations, defaulting to an empty list if not found
    motivations = character.motivation_manager.get_motivations()

    # Find the highest urgency value
    highest_urgency = max((m.urgency for m in motivations), default=0)
    top_motivations = [m.type for m in motivations if m.urgency == highest_urgency]

    
    from visual_effects import RESET, RED, GREEN, PURPLE, BROWN
    from status import StatusLevel, get_primary_status_display
    # 👇 Get the character's primary status (move this above the table definition)
    status_obj = character.status.get_status(character.primary_status_domain)
    status_display = (
        color_text(f"{status_obj.title} ({status_obj.level.name})", GREEN)
        if status_obj and status_obj.level == StatusLevel.HIGH
        else f"{status_obj.title} ({status_obj.level.name})"
        if status_obj else "Unknown"
    )
    # Second table with the second header row
    character_table_2 = [
        ["Race", "Status", "Intelligence", "Fun", "Motivations", ""],  # Empty fields for alignment
        [
            getattr(character, "lorem", character.race),
            status_display,#later use get_primary_status_display(character)
            getattr(character, "xxx", getattr(character, "intelligence", "N/A")),
            color_text(str(character.fun), RED) if character.fun < 4 else str(character.fun),
        ", ".join(str(m) for m in top_motivations)
        ],
    ]
    # Print the first table
    print(tabulate(character_table_1, headers="firstrow", tablefmt="grid"))
    
    print("Loading", end="", flush=True)
    loading_bar()

    # Print the second table
    print(tabulate(character_table_2, headers="firstrow", tablefmt="grid"))
    #print("\n🎒 Debugging Inventory:")
    if character.inventory.items:
        for name, item in character.inventory.items.items():
            print(f"  {name} - Qty: {item.quantity}, Type: {type(item).__name__}, ID: {id(item)}")
    else:
        print("  (Debug: Empty)")

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
        if isinstance(faction, Faction):  # Ensure faction is an instance
        
            print(f"\n--- {faction.name} ---")
        else:
            print(f"WARNING: Expected an instance of Faction, but got {faction} of type {type(faction)}")
            print(f"DEBUG: faction is {faction} of type {type(faction)}")

        
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

def display_character_whereabouts(character):
    """Displays the character's current location and region using direct attributes."""
    location_name = character.location.name if isinstance(character.location, Location) else str(character.location)
    print(f"Current Location: {location_name}")  # Removed extra region


def display_civilians():
    pass

from location import Shop

def display_employees(location):

    # Check if the location itself has employees
    if location.employees_there:
        table_data = [
            [employee.name, employee.__class__.__name__, ""]  # Name, Position, Notes
            for employee in location.employees_there
        ]

        headers = ["Name", "Position", "Notes"]
        print(f"\nEmployees at {location.name}:\n")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print(f"No employees present at {location.name}.")

def display_corporations():
    pass

from tabulate import tabulate

def display_gangs(game_state):
    for gang in game_state.gangs:
        # Table 1: Gang overview
        boss_name = gang.boss.name if gang.boss else "No Boss"
        hq_region = gang.region if gang.region else "Unknown Region"
        num_captains = len([member for member in (gang.members or []) if isinstance(member, Captain)])
        num_gangers = len([member for member in gang.members if isinstance(member, GangMember)])  # Assuming 'GangMember' class exists

        gang_table = [
            ["Name", "Boss", "Captains", "Gangers", "HQ"],
            [gang.name, boss_name, num_captains, num_gangers, hq_region],
        ]
        print(tabulate(gang_table, headers="firstrow", tablefmt="grid"))

        # Table 2: Gang goals
        if gang.goals:
            goal = gang.goals[0].goal_type
            goal_status = gang.goals[0].status
            target = gang.goals[0].target if gang.goals[0].target else "None"
        else:
            goal = "No Goal"
            goal_status = "N/A"
            target = "None"

        goals_table = [
            ["Race", "Violence", "Goal", "Goal Status", "Target"],
            [gang.race, gang.violence_disposition, goal, goal_status, target],
        ]
        print(tabulate(goals_table, headers="firstrow", tablefmt="grid"))

        # Add a space between gang entries for clarity
        print("\n" + "-" * 50 + "\n")


def display_state(state):
    if not hasattr(state, 'state_staff') or not state.state_staff:
        print("No staff members available for this State.")
        return

    # Group characters by class type
    grouped_staff = {}
    for character in state.state_staff:
        class_name = character.__class__.__name__
        if class_name not in grouped_staff:
            grouped_staff[class_name] = []
        grouped_staff[class_name].append([
            character.name,
            class_name,
            character.location.name if character.location else "Unknown", #ALERT
            ", ".join(m.type for m in character.motivation_manager.get_motivations())
        ])

    # Display tables
    for class_type, staff_data in grouped_staff.items():
        print(f"\n{class_type} Staff:\n")
        print(tabulate(staff_data, headers=["Name", "Class", "Whereabouts", "Motivations"], tablefmt="fancy_grid"))

def display_world(all_regions):
    """Display all regions, their locations, and danger levels in a tabulated format."""
    table_data = []

    for region in all_regions:
        region_name = region.name if region.name else "Unknown Region" #ALERT
        location_names = ", ".join(loc.name for loc in region.locations) if region.locations else "No known locations"
        danger_level = region.danger_level.name if region.danger_level else "Unknown"#ALERT

        table_data.append([region_name, location_names, danger_level])

    print("\n🌍 **World Overview:**")
    print(tabulate(table_data, headers=["Region", "Locations", "Danger Level"], tablefmt="grid"))

def display_character_vicinity():
    #shows where the character is in a table and what has got their attention there
    #The columns should be charcter name, wherebouts and a third dynamic column called percepts that displays
    #other proximal data, for example if there is danger or an attracive other character, or a partner, friend or event
    #
    pass

def display_character_Summary():
    #shows on what the characters attention is on. This will be a dynamic list, called Attention including motivations, goals, and environmental 
    #proximal factors like friends, partners, enemies or dangers nearby.
    pass

def show_locations_in_region(region):
    """Display locations in the specified region."""

    # Ensure region has locations
    if not hasattr(region, "locations") or not region.locations:
        print(f"No locations available in {region.name}.")
        return
    
    # Prepare the data for tabulation
    table_data = []
    for location in region.locations:  # Accessing locations directly
        # Extract relevant fields
        name = getattr(location, "name", "Unknown Name")
        condition = getattr(location, "condition", "Unknown Condition")
        fun = getattr(location, "fun", "N/A")
        security_level = getattr(location.security, "level", "N/A") if hasattr(location, "security") else "N/A"

        # Add to table data
        table_data.append([name, condition, fun, security_level])

    # Display the table
    headers = ["Name", "Condition", "Fun", "Security Level"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))  # Try also tablefmt="pretty"

#Shop:
def show_shop_inventory(character, shop):
    """Display the inventory of a shop in a tabulated format."""
    from menu_utils import ShopPurchaseMenu
    if not shop.inventory.items:
        print(f"{shop.name} has no items available.")
        return

    table_data = []
    for item in shop.inventory:
        #properly iterate over the Item objects, shop.inventory.items is a dictionary
        if isinstance(item, str):
            print(f"⚠️ Warning: Expected Item object, got string '{item}'. Skipping.")
            continue
        table_data.append([item.name, item.price, item.quantity])

    headers = ["Item", "Price", "Quantity"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    

def display_selected_character_current_region(character, region):
    region = character.region
    if isinstance(region, str):
        print(f"Warning: character.region is a string: {region}")
        # Optional: auto-convert using get_region_by_name(region)
    else:
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

def compare_locations(all_locations, all_regions):
    """Compares locations in all_locations vs. region.locations and lists missing ones."""
    
    all_location_names = {loc.name for loc in all_locations}  # Names from all_locations
    region_location_names = set()  # Will store all locations from regions

    for region in all_regions:
        for loc in region.locations:
            region_location_names.add(loc.name)

    # Find missing locations
    missing_from_all_locations = region_location_names - all_location_names
    extra_in_all_locations = all_location_names - region_location_names

    if missing_from_all_locations:
        print("🚨 WARNING: These locations exist in regions but are missing from all_locations:")
        for loc in missing_from_all_locations:
            print(f" - {loc}")

    if extra_in_all_locations:
        print("⚠️ NOTICE: These locations exist in all_locations but are not assigned to any region:")
        for loc in extra_in_all_locations:
            print(f" - {loc}")

    if not missing_from_all_locations and not extra_in_all_locations: #line 402
        pass
        #print("✅ All locations are correctly assigned.")

    
    missing_locations = []
    
    for region in all_regions:
        for loc in region.locations:
            if loc not in all_locations:
                missing_locations.append(f"⚠️⚠️ MISSING: {loc.name} from {region.name}")

    if missing_locations:
        print("\n".join(missing_locations))
    else:
        pass
        #print("✅ All locations are correctly assigned in all_locations!")


def print_character_brief(char, *, show_name=True, show_class=True, show_location=True, show_faction=True):
    parts = []
    if show_name:
        parts.append(char.name)
    if show_class:
        parts.append(char.__class__.__name__)
    if show_location and getattr(char, "location", None):
        loc = char.location
        parts.append(f"{loc.__class__.__name__} in {loc.region.name}")
    if show_faction and getattr(char, "faction", None):
        parts.append(f"Faction: {char.faction.name}")
    print(" | ".join(parts))
    #use it like this
    """ if self.is_test_npc:
        print_character_brief(self) """

def get_display_name(obj):
    """
    Safely get a display-friendly name from an object, whether it's a
    Character, Location, Thought, or anything else with a .name or .origin.
    """
    if obj is None:
        return "[None]"

    # If object has .origin, recurse into it
    if hasattr(obj, "origin"):
        return get_display_name(obj.origin)

    # If object has .name, return it
    if hasattr(obj, "name"):
        return str(obj.name)

    # Fallback: Use class name
    return obj.__class__.__name__


def display_region_knowledge_summary(knowledge_list, npc=None):
    """
    Display two tables:
    1. Region overview (name, gangs, enemies, etc.)
    2. Social overview (friends, enemies, partners)
    """
    if not knowledge_list:
        return "No region knowledge entries found."

    # Table 1: Region Summary
    region_table = []
    for rk in knowledge_list:
        is_home = npc and rk.region_name == getattr(npc.home_region, "name", None)
        region_label = "🏠 " if is_home else ""

        region_table.append([
            f"{region_label}{rk.region_name}",
            len(rk.region_gangs),
            len(rk.hostile_factions),
            len(rk.locations),
            len(rk.active_events),
            len(rk.known_characters),
            ", ".join(rk.tags) if rk.tags else ""
        ])

    region_headers = [
        "Region",
        "Gangs",
        "Hostile",
        "Locations",
        "Events",
        "Known People",
        "Notes"
    ]

    region_table_output = tabulate(region_table, headers=region_headers, tablefmt="fancy_grid")

    # Table 2: Social Summary (one row per region, even if many values are 0)
    social_table = []
    for rk in knowledge_list:
        if hasattr(rk, "social_map"):
            smap = rk.social_map
        else:
            smap = {"friends": 0, "enemies": 0, "allies": 0, "neutral": 0, "partners": 0}

        social_table.append([
            rk.region_name,
            smap.get("friends", 0),
            smap.get("enemies", 0),
            smap.get("allies", 0),
            smap.get("neutral", 0),
            smap.get("partners", 0),
        ])

    social_headers = [
        "Region",
        "Friends",
        "Enemies",
        "Allies",
        "Neutral",
        "Partners"
    ]

    social_table_output = tabulate(social_table, headers=social_headers, tablefmt="fancy_grid")

    return f"{region_table_output}\n\n{social_table_output}"


def format_origin(origin):
    if origin == "—":
        return "[MISSING]"
    elif hasattr(origin, "name"):
        return f"{origin.__class__.__name__}('{origin.name}')"
    elif hasattr(origin, "__class__"):
        return origin.__class__.__name__
    else:
        return str(origin)[:40]  # truncate long fallback

def display_percepts_table(npc):
    """
    Prints a clean tabular debug summary of an NPC's percepts.
    Only intended for debug characters or test NPCs.
    """
    anchor = getattr(npc, "current_anchor", None)
    if not getattr(npc, "is_test_npc", False):
        return
    print(f"\n[DEBUG] {npc.name} - Percepts Table After Observation:")

    table_data = []

    for i, (key, v) in enumerate(npc._percepts.items()):
        # Step 1: Safely access nested data
        data = v.get("data", {})
        origin = v.get("origin", data.get("origin", "—"))

        # Step 2: Get description/type
        desc = data.get("description") or data.get("type") or "UNKNOWN"

        type_ = data.get("type", "—")
        
        # Remove redundant ": Type" or "(Type)" if it matches the actual type
        if isinstance(desc, str) and type_ in desc:
            desc = desc.replace(f": {type_}", "").replace(f"({type_})", "").strip()

        # Simplify verbose character description
        if isinstance(desc, str) and "," in desc and " of " in desc:
            desc = desc.split(",")[0]

        # NEW: Add controlling faction to location descriptions
        origin = v.get("origin", data.get("origin", "—"))

        if type_ == "Location" and isinstance(origin, Location):
            faction = getattr(origin, "controlling_faction", None)
            if faction:
                desc = f"{origin.name}, {faction.name}"
            else:
                desc = origin.name

        # Step 3: Replace origin with Appearance summary
        if origin != "—":
            appearance = extract_appearance_summary(origin)
        else:
            appearance = "[MISSING]"

        # Step 4: Count keys inside data block
        n_keys = len(data.keys())

        salience = 0
        anchor = getattr(npc, "current_anchor", None)
        if hasattr(origin, "compute_salience") and callable(origin.compute_salience):#a problem line?
            try:
                salience = origin.compute_salience(npc, anchor)
            except Exception as e:
                salience = f"ERR: {e}"

        salience_score = compute_salience(data, npc, anchor) #compute_salience here marked as not defined
        table_data.append([
            i,
            desc,
            type_,
            appearance,
            n_keys,
            f"{salience_score:.2f}"
        ])

    print(tabulate(
        table_data,
        headers=["#", "Description", "Type", "Appearance", "#Keys", "Salience"],
        tablefmt="rounded_outline"
    ))

def display_npc_mind(npc):
    thoughts_data = []
    for thought in npc.mind.thoughts:
        corollary_count = len(thought.corollary) if thought.corollary else 0
        thoughts_data.append([
            f"{thought.content} ({corollary_count} corollaries)",
            thought.subject,
            thought.origin,
            ", ".join(thought.tags),
            f"{thought.urgency:.1f}"
        ])

    print("\n--- Thought Table ---")
    print(tabulate(thoughts_data, headers=["Thought", "Subject", "Origin", "Tags", "Urgency"]))

    focus_data = []
    if npc.attention_focus:
        focus = npc.attention_focus
        focus_data.append([
            focus.content,
            focus.subject,
            focus.origin,
            ", ".join(focus.tags),
            f"{focus.urgency:.1f}"
        ])

    print("\n--- Focus ---")
    print(tabulate(focus_data, headers=["Thought", "Subject", "Origin", "Tags", "Urgency"]))

    obsessions_data = []
    for ob in npc.mind.obsessions:
        obsessions_data.append([
            ob.name,
            f"{ob.strength:.1f}",
            ", ".join(ob.tags)
        ])

    print("\n--- Obsessions ---")
    print(tabulate(obsessions_data, headers=["Source", "Weight", "Tags"]))


def display_sellers(shops: list):
    """Display a nicely formatted table of sellers (shops)."""
    if not shops:
        print("No shops to display.")
        print(f"[DEBUG] {len(shops)} shops to display")
        return

    rows = [format_shop_debug(shop) for shop in shops]
    headers = rows[0].keys() if rows else []
    print(tabulate(rows, headers="keys", tablefmt="fancy_grid"))

def debug_display_all_shops(all_regions):
    print("[DEBUG] Displaying all shops:")

    all_shops = []
    for region in all_regions:
        if hasattr(region, "shops"):
            all_shops.extend(region.shops)

    display_sellers(all_shops)

