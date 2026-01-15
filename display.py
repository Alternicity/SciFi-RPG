#display.py
from tabulate import tabulate
import logging
from textwrap import wrap

from base.character import Character
from social.social_utils import get_socially_favoured
import loader
import os
from collections import defaultdict
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian, GangMember, Child, Influencer,
                           Babe, Detective)

from location.locations import VacantLot
from region.region import UndevelopedRegion

from visual_effects import loading_bar, color_text
#from menu_utils import get_user_choice
#This file cannot import from menu_utils here, maybe lazy imports are ok
from common import get_file_path, BASE_REGION_DIR
from typing import List, Union
from character_creation_funcs import player_character_options
from base.faction import Faction
from base.location import Location
from region.region import Region
from perception.perceptibility import extract_appearance_summary

from config_npc_vitals import NPC_VITALS_CONFIG
from debug_utils import debug_print, ROLE_FILTERS
from create.create_game_state import get_game_state
game_state = get_game_state()
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

from location.locations import Shop

def display_employees(location):

    # Check if the location itself has employees
    if isinstance(location, WorkplaceMixin) and location.employees_there:
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

def debug_list_gang_hqs():
    
    print("\n[DEBUG] ===== GANG HQ DIAGNOSTICS =====\n")
    
    gangs = game_state.gangs if hasattr(game_state, "gangs") else []
    street_gangs = set(game_state.all_street_gangs) if hasattr(game_state, "all_street_gangs") else set()

    if not gangs:
        print("No gangs found in game_state.")
        return

    for gang in gangs:
        # NEW: race column (fallback if missing)
        race = getattr(gang, "race", "Unknown")

        hq_name = gang.HQ.name if getattr(gang, "HQ", None) else "Street Gang"
        member_count = len(getattr(gang, "members", []))

        print(
            f"• {gang.name:<35} | "
            f"• {race:<15} | "
            f"• {hq_name:<25} | "
            f"Members: {member_count}"
        )



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

def display_character_summary():#called from player flow
    #shows on what the characters attention is on. This will be a dynamic list, called Attention including motivations, and environmental 
    #proximal factors like friends, partners, enemies or dangers.
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
    if not characters:
        print("No existing characters.")
        return

    rows = []
    for char in characters:
        debug_flag = ""
        if hasattr(char, "debug_role"):
            debug_flag = f"[{char.debug_role}]"

        rows.append([
            char.name,
            char.__class__.__name__,
            getattr(char, "faction", None),
            debug_flag
        ])

    print(tabulate(
        rows,
        headers=["Name", "Class", "Faction", "Debug"],
        tablefmt="fancy_grid"
    ))

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

        # Clean tag list
        #cleaned_tags = [tag for tag in rk.tags if tag not in {"region", "region_knowledge"}]
        cleaned_tags = sorted(tag for tag in rk.tags if tag not in {"region", "region_knowledge"})

        # Wrap long tag strings at ~20 characters
        
        joined_tags = ", ".join(cleaned_tags)
        wrapped_tags = "\n".join(wrap(joined_tags, width=20)) if joined_tags else ""

        region_table.append([
            f"{region_label}{rk.region_name}",
            len(rk.region_gangs),
            len(rk.hostile_factions),
            len(rk.locations),
            len(rk.active_events),
            len(rk.known_characters),
            wrapped_tags
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


def format_origin(origin):#not called
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
    
    if npc is None:
        return
    
    gs = get_game_state()
    if gs and not gs.should_display_npc(npc):
        return
    
    debug_print(
        npc,
        f"[DEBUG] display_percepts_table: debug_role={getattr(npc, 'debug_role', None)}",
        category="percept"
    )

    role = getattr(npc, "debug_role", None)
    if role is None or not ROLE_FILTERS.get(role, False):
        return
    
    anchor = getattr(npc, "current_anchor", None)

    debug_print(
            npc,
            "Percepts table after observation",
            category="percept"
        )

    table_data = []

    for i, (key, v) in enumerate(npc.percepts.items()):

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


        origin = v.get("origin") or data.get("origin")
        # --- Unified, safe salience computation ---
        # Display is now anchor-centric: salience depends on the current anchor only.
        try:
            salience_score = anchor.compute_salience_for(origin, npc) if anchor else 0.0
        except Exception:
            salience_score = 0.0

                # --- Build Info Column ---
        info = "—"

        # Origin objects may be Location, Character, Item, etc.
        origin_obj = origin

        # Civilians
        if isinstance(origin_obj, Civilian):
            if getattr(origin_obj, "workplace", None) == npc.location:
                info = "Employee"
            else:
                info = "Civilian"

        # Gang Members
        elif isinstance(origin_obj, GangMember):
            fac = getattr(origin_obj, "faction", None)

            if fac:
                # Check if faction is a Gang object
                if getattr(fac, "type", None) == "gang":
                    if getattr(fac, "is_street_gang", False):
                        info = f"{fac.name} (street gang)"
                    else:
                        info = f"{fac.name} (gang)"
                else:
                    info = "GangMember (unknown faction)"
            else:
                info = "GangMember (unaffiliated)"

        if hasattr(origin_obj, "modulated_ambience"):
            ambience = origin_obj.modulated_ambience()
            if ambience:
                top = max(ambience.items(), key=lambda x: x[1])
                info = f"Enhances {top[0]}"

        # Append row
        table_data.append([
            i,
            desc,
            type_,
            appearance,
            info,
        ])


    print(tabulate(
        table_data,
        headers=["#", "Description", "Type", "Appearance", "Info"],
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
    if npc.mind.attention_focus:
        focus = npc.mind.attention_focus
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

    # --- Motivation Table ---
    print("\n--- Motivation Table ---")

    motivation_data = []

    top = npc.motivation_manager.get_highest_priority_motivation(npc)

    for m in npc.motivation_manager.get_motivations():
        motivation_data.append([
            m.type,
            f"{m.urgency:.1f}",
            "YES" if m is top else "",
            "YES" if m.suppressed else "NO",
            m.suppression_reason or "—",
        ])

    if motivation_data:
        print(tabulate(
            motivation_data,
            headers=["Motivation", "Urgency", "TOP", "Suppressed", "Reason"],
            tablefmt="rounded_outline"
        ))
    else:
        print("(no motivations)")

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
        if hasattr(region, "shops"):#perhaps there is a problem here. we should check this shops, and perhaps try testing for
            #other things
            all_shops.extend(region.shops)
    #temporarily commented to suppress this table in output, re-enable and update it later.
    #display_sellers(all_shops)

def format_shop_debug(shop) -> dict:
    return {
        "Name": shop.name,
        "Type": shop.__class__.__name__,
        "Region": shop.region.name if hasattr(shop, "region") else "?",
        "Specialization": shop.specialization,
        "OwnerType": "corporate" if any(corp for corp in getattr(shop.region, "region_corps", []) if corp.HQ == shop) else "family"
    }

def display_npc_vitals(npc, show_memories=True, show_thoughts=True):
    """
    Comprehensive display of NPC state.
    Call this from simulate_hours() for the 3 debug NPCs.
    """
    from debug_utils import ROLE_FILTERS

    if npc is None:
        return
    
    # Contextual suppression
    gs = get_game_state()
    if gs is not None and not gs.should_display_npc(npc):
        return

    # Optional role filter
    """ role = getattr(npc, "debug_role", None)
    if role is not None and not ROLE_FILTERS.get(role, False):
        return """

    #See: config_npc_vitals.py
    
    print("\n")
    print(f"NPC VITALS: {npc.name}")

    # === BASIC INFO ===
    if NPC_VITALS_CONFIG.get("identity", True):
        print(f"\n[IDENTITY]")
        print(f"  Name: {npc.name}")
        print(f"  Debug Role: {getattr(npc, 'debug_role', 'N/A')}")
        print(f"  Class: {npc.__class__.__name__}")
        print(f"  Race: {npc.race}, Sex: {npc.sex}")
    
    # === LOCATION ===
    if NPC_VITALS_CONFIG.get("location", True):
        print(f"\n[LOCATION]")
        print(f"  Region: {npc.region.name if npc.region else 'None'}")
        print(f"  Current Location: {npc.location.name if npc.location else 'None'}")
        
        if npc.current_destination and npc.current_destination != npc.location:
            print(f"  Destination: {npc.current_destination.name}")
        
        if npc.just_arrived:
            print(f"  Status: Just arrived")
        if npc.just_left_location:
            print(f"  Status: Just left")
    
    # === VITALS ===
    if NPC_VITALS_CONFIG.get("vitals", True):
        print(f"\n[VITALS]")
        if hasattr(npc, 'vitals'):
            v = npc.vitals
            print(f"  Hunger: {v.hunger:.1f}/20 {_vitals_indicator(v.hunger, 'hunger')}")
            print(f"  Effort: {v.effort:.1f}/20 {_vitals_indicator(v.effort, 'effort')}")
            print(f"  Fun: {v.fun:.1f}/20 {_vitals_indicator(v.fun, 'fun')}")
        else:
            # Fallback for NPCs without VitalsComponent
            print(f"  Hunger: {getattr(npc, 'hunger', 'N/A')}/20")
            print(f"  Effort: {getattr(npc, 'effort', 'N/A')}/20")
            print(f"  Fun: {getattr(npc, 'fun', 'N/A')}/20")
    
    # === EMPLOYMENT ===
    if NPC_VITALS_CONFIG.get("employment", True):
        print(f"\n[EMPLOYMENT]")
        if npc.employment and npc.employment.workplace:
            print(f"  Workplace: {npc.employment.workplace.name}")
            print(f"  Role: {npc.employment.role.name if npc.employment.role else 'None'}")
            print(f"  Shift: {npc.employment.shift} ({npc.employment.shift_start}:00-{npc.employment.shift_end}:00)")
            print(f"  On Shift: {'Yes' if npc.employment.is_on_shift else 'No'}")
            print(f"  Currently Working: {'Yes' if npc.employment.is_on_shift else 'No'}")
            if npc.employment.just_got_off_shift:
                print(f"  Status: Just got off shift")
        else:
            print(f"  Unemployed")
    
    # === MONEY ===
    if NPC_VITALS_CONFIG.get("finances", True):
        print(f"\n[FINANCES]")
        if npc.wallet:
            print(f"  Cash: ${npc.wallet.cash}")
            print(f"  Bank: ${npc.wallet.bankCardCash}")
            print(f"  Total: ${npc.wallet.balance}")
        else:
            print(f"  No wallet")
    
    # === MOTIVATIONS ===
    if NPC_VITALS_CONFIG.get("motivations", True):
        print(f"\n[MOTIVATIONS]")
        motivations = npc.motivation_manager.sorted_by_urgency(descending=True)
        if motivations:
            for i, m in enumerate(motivations[:5], 1):  # Show top 5
                print(f"  {i}. {m.type} (urgency: {m.urgency:.1f})")
                if m.target:
                    print(f"     → target: {m.target}")
        else:
            print(f"  No active motivations")
    
    # === ANCHORS ===
    if NPC_VITALS_CONFIG.get("anchors", True):
        print(f"\n[ANCHORS]")
        if hasattr(npc, 'anchors') and npc.anchors:
            for anchor in npc.anchors:
                print(f"  • {anchor.name} (weight: {anchor.weight:.1f}, priority: {anchor.priority:.1f})")
                if anchor.enables:
                    print(f"    Enables: {', '.join(anchor.enables)}")
        else:
            print(f"  No anchors")
    
    # === FOCUS ===
    if NPC_VITALS_CONFIG.get("focus", True):
        print(f"\n[MENTAL FOCUS]")
        if npc.mind.default_focus:
            print(f"  Default Focus: {npc.mind.default_focus.name if hasattr(npc.mind.default_focus, 'name') else npc.mind.default_focus}")
        else:
            print(f"  Default Focus: None")
        
        if npc.mind.attention_focus:
            focus = npc.mind.attention_focus
            if hasattr(focus, 'content'):
                print(f"  Attention: {focus.content} (urgency: {focus.urgency})")
            else:
                print(f"  Attention: {focus}")
        else:
            print(f"  Attention: None")
    
    # === THOUGHTS ===
    if NPC_VITALS_CONFIG.get("thoughts", True):
        if show_thoughts:
            print(f"\n[THOUGHTS] ({len(npc.mind.thoughts)} total)")
            urgent_thoughts = [t for t in npc.mind.thoughts if t.urgency >= 5]
            if urgent_thoughts:
                for i, thought in enumerate(sorted(urgent_thoughts, key=lambda t: t.urgency, reverse=True)[:5], 1):
                    print(f"  {i}. {thought.content}")
                    print(f"     Urgency: {thought.urgency}, Tags: {thought.tags}")
                    if thought.anchored:
                        print(f"     [ANCHORED]")
            else:
                print(f"  No urgent thoughts")
    
    # === MEMORIES ===
    if NPC_VITALS_CONFIG.get("memories", True):
        if show_memories:
            print(f"\n[RECENT EPISODIC MEMORIES] (last 5)")
            episodic = npc.mind.memory.get_episodic()
            if episodic:
                for i, mem in enumerate(reversed(episodic[-5:]), 1):
                    print(f"  {i}. {mem.subject} {mem.verb} {mem.object_}")
                    if mem.details:
                        print(f"     → {mem.details}")
            else:
                print(f"  No episodic memories")
            
            print(f"\n[SEMANTIC KNOWLEDGE]")
            semantic_count = {cat: len(mems) for cat, mems in npc.mind.memory.semantic.items() if mems}
            if semantic_count:
                for cat, count in semantic_count.items():
                    print(f"  {cat}: {count} entries")
            else:
                print(f"  No semantic knowledge")
    
    # === SOCIAL ===
    if NPC_VITALS_CONFIG.get("social", True):
        print(f"\n[SOCIAL]")
        if npc.partner:
            partner_name = npc.partner.name if hasattr(npc.partner, 'name') else str(npc.partner)
            print(f"  Partner: {partner_name}")
        else:
            print(f"  Partner: None")
        
        print(f"  Self-Esteem: {npc.self_esteem}/100")
        
        if npc.fun_prefs:
            print(f"  Fun Preferences: {npc.fun_prefs}")
        
        # === TIME CONTEXT ===
        print(f"\n[TIME]")
        print(f"  Hour: {game_state.hour}:00")
        print(f"  Day: {game_state.day}")
        

def _vitals_indicator(value, vital_type):
    """Return visual indicator for vital status."""
    if vital_type == 'hunger':
        if value >= 18:
            return "[CRITICAL ⚠️]"
        elif value >= 15:
            return "[URGENT ⚠]"
        elif value >= 10:
            return "[HUNGRY]"
        else:
            return "[OK ✓]"
    
    elif vital_type == 'effort':
        if value <= 3:
            return "[EXHAUSTED ⚠️]"
        elif value <= 8:
            return "[TIRED ⚠]"
        elif value >= 15:
            return "[ENERGETIC ✓]"
        else:
            return "[OK]"
    
    elif vital_type == 'fun':
        if value >= 18:
            return "[MISERABLE ⚠️]"
        elif value >= 15:
            return "[BORED ⚠]"
        elif value <= 5:
            return "[HAPPY ✓]"
        else:
            return "[OK]"
    
    return ""



def display_npc_summary(npc):
    """
    Condensed one-line summary for quick scanning.
    Useful for showing all NPCs at once.
    """
    hour = (get_game_state().tick % 24)
    
    hunger = getattr(npc.vitals, 'hunger', npc.hunger) if hasattr(npc, 'vitals') else npc.hunger
    effort = getattr(npc.vitals, 'effort', npc.effort) if hasattr(npc, 'vitals') else getattr(npc, 'effort', '?')
    
    top_mot = npc.motivation_manager.get_highest_priority_motivation()
    mot_str = f"{top_mot.type}({top_mot.urgency:.0f})" if top_mot else "none"
    
    loc = npc.location.name if npc.location else "nowhere"
    
    status = ""
    if npc.employment.is_on_shift:
        status = "🔧WORK"
    elif npc.employment.just_got_off_shift:
        status = "🏁OFF"
    elif npc.just_arrived:
        status = "📍ARR"
    
    print(f"{npc.name:20} | {loc:15} | H:{hunger:4.1f} E:{effort:4.1f} | {mot_str:20} | {status}")


def display_daily_schedule_preview(npc):
    """
    Show what NPC's schedule looks like for the day.
    Useful for understanding work/sleep patterns.
    """
    print(f"\n{'='*60}")
    print(f"DAILY SCHEDULE: {npc.name}")
    print(f"{'='*60}")
    
    schedule = []
    
    # Sleep
    schedule.append("00:00-06:00 | Sleep (home)")
    
    # Morning
    schedule.append("06:00-09:00 | Wake, breakfast, commute")
    
    # Work
    if npc.employment and npc.employment.workplace:
        start = npc.employment.shift_start
        end = npc.employment.shift_end
        schedule.append(f"{start:02d}:00-{end:02d}:00 | Work at {npc.employment.workplace.name}")
    else:
        schedule.append("09:00-17:00 | Free time (unemployed)")
    
    # Evening
    schedule.append("17:00-20:00 | Unwind, eat, social")
    
    # Night
    schedule.append("20:00-22:00 | Fun activities")
    schedule.append("22:00-00:00 | Prepare for sleep")
    
    for entry in schedule:
        print(f"  {entry}")
    
    print(f"{'='*60}\n")

#deprecate, at least for now, maybe useful when more active npcs added
""" def display_debug_npcs(npcs):
    
    if not npcs:
        return

    for npc in npcs:
        display_npc_vitals(npc) """

def summarize_npc_turns(all_characters):
    from collections import Counter

    counts = Counter()

    for npc in all_characters:
        cls = npc.__class__.__name__
        role = getattr(npc, "debug_role", "background")
        counts[(cls, role)] += 1

    parts = []
    for (cls, role), count in counts.items():
        parts.append(f"{cls}({role}) x{count}")

    gs = get_game_state()
    return f"Hour {gs.hour} — " + ", ".join(sorted(parts))

#remove
""" def display_tc2_npc_state(npc):
    gs = get_game_state()
    if not gs:
        return
    for npc in (
        gs.debug_npcs.get("civilian_worker"),
        gs.debug_npcs.get("civilian_liberty"),
    ):
        if npc:
            display_npc_vitals(npc) """

def display_civ_worker(npc):
    gs = get_game_state()
    if not gs or npc not in gs.debug_npcs.values():
        return

    emp = getattr(npc, "employment", None)

    workplace = emp.workplace.name if emp and emp.workplace else "—"
    role = emp.role.name if emp and emp.role else "—"
    shift = f"{emp.shift_start}–{emp.shift_end}" if emp else "—"


    working = emp.is_on_shift or emp.on_duty(game_state.hour)
    on_shift = "Working" if working else "Off"
    just_off = " | Just got off shift" if npc.just_got_off_shift else ""


    urgent = npc.motivation_manager.get_highest_priority_motivation()
    urgent_str = (
        f"{urgent.type}(+{urgent.urgency})"
        if urgent else "—"
    )

    print(
        f"[WORKER display] {npc.name} | {npc.location.name if npc.location else '—'}"
        f" | role={npc.debug_role}"
        f" | 💼 {on_shift}"
        f" | shift={shift}"
        f" | hunger={npc.hunger}"
        f" | fun={npc.fun}"
        f" | effort={getattr(npc, 'effort', '—')}"
        f" | €{npc.wallet.balance if npc.wallet else '—'}"
        f" | motive={urgent_str}"
        f" | esteem={npc.self_esteem}"
        f" | anchor={npc.current_anchor.__class__.__name__ if npc.current_anchor else '—'}"
        f" | Workplace={workplace}"
        f"{just_off}"
    )

def display_civ_waitress(npc):
    gs = get_game_state()
    if not gs or npc not in gs.debug_npcs.values():
        return

    emp = getattr(npc, "employment", None)

    workplace = emp.workplace.name if emp and emp.workplace else "—"
    role = emp.role.name if emp and emp.role else "—"
    shift = f"{emp.shift_start}–{emp.shift_end}" if emp else "—"


    working = emp.is_on_shift or emp.on_duty(game_state.hour)
    on_shift = "Working" if working else "Off"
    just_off = " | Just got off shift" if emp and emp.just_got_off_shift else ""

    urgent = npc.motivation_manager.get_highest_priority_motivation()
    urgent_str = (
        f"{urgent.type}(+{urgent.urgency})"
        if urgent else "—"
    )

    print(
        f"[WAITRESS display] {npc.name}"
        f" | {npc.location.name if npc.location else '—'}"
        f" | role={npc.debug_role}"
        f" | 💼 {on_shift}"
        f" | shift={shift}"
        f" | hunger={npc.hunger}"
        f" | fun={npc.fun}"
        f" | effort={getattr(npc, 'effort', '—')}"
        f" | €{npc.wallet.balance if npc.wallet else '—'}"
        f" | motive={urgent_str}"
        f" | esteem={npc.self_esteem}"
        f" | anchor={npc.current_anchor.__class__.__name__ if npc.current_anchor else '—'}"
        f" | Workplace={workplace}"
        f"{just_off}"
    )


def display_civ_liberty(npc):
    gs = get_game_state()
    if not gs or npc not in gs.debug_npcs.values():
        return

    urgent = npc.motivation_manager.get_highest_priority_motivation()
    urgent_str = (
        f"{urgent.type}(+{urgent.urgency})"
        if urgent else "—"
    )

    favoured = get_socially_favoured(npc)
    favoured_name = favoured.name if favoured else "—"

    print(
        f"[LIBERTY] {npc.name} | {npc.location.name if npc.location else '—'}"
        f" | role={npc.debug_role}"
        f" | hunger={npc.hunger}"
        f" | fun={npc.fun}"
        f" | effort={getattr(npc, 'effort', '—')}"
        f" | €{npc.wallet.balance if npc.wallet else '—'}"
        f" | motive={urgent_str}"
        f" | esteem={npc.self_esteem}"
        f" | anchor={npc.current_anchor.__class__.__name__ if npc.current_anchor else '—'}"
        f" | favoured={favoured_name}"
    )

def display_top_motivations(npc, top_n=2, category="motive"):
    """
    Print the top-N most urgent, unsuppressed motivations for an NPC.
    Intended for compact TC2 output.
    """

    mm = getattr(npc, "motivation_manager", None)
    if mm is None:
        return

    # Get unsuppressed motivations
    active = [m for m in mm.motivations if not m.suppressed]
    if not active:
        return

    # Sort by urgency descending
    active.sort(key=lambda m: m.urgency, reverse=True)

    # Take top N
    top = active[:top_n]

    motive_str = ", ".join(
        f"{m.type}({m.urgency:.1f})"
        for m in top
    )

    debug_print(
        npc,
        f"[TopMotives] {npc.name}: {motive_str}",
        category=category
    )

def summarize_action(action):
    if not isinstance(action, dict):
        return str(action)

    name = action.get("name", "?")
    params = action.get("params", {})

    summary_params = {}
    for k, v in params.items():
        summary_params[k] = getattr(v, "name", v)

    return f"{name}({summary_params})"
