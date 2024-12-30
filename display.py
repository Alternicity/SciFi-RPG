from tabulate import tabulate

# Only import what you need from display.py. For example,
# if there are other display functions, import them selectively


def print_table(data, headers):
    """Print data in a tabular format."""
    # Convert list of dictionaries to a list of lists (values of dicts)
    table_data = [list(item.values()) for item in data]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def print_region_data(region):
    """Display the generated region data in a tabular format."""
    print("\n--- Generated Region ---")

    print("\nLocations:")
    print_table(region["locations"], ["Name", "Type", "Economic Level"])

    print("\nGangs:")
    print_table(region["gangs"], ["Name", "Members"])

    print("\nCorporations:")
    print_table(region["corporations"], ["Name", "Members", "Economic Level"])

    print("\nStores:")
    print_table(region["stores"], ["Store Name", "Economic Level", "Items for Sale"])


def display_factions_data():
    """Load and display factions data."""
    try:
        factions_data = load_data("data/loyalties/factions/factions.json")
        print("\n--- Factions Data ---")

        if not factions_data:
            print("No factions data found.")
        else:
            for faction in factions_data:
                if isinstance(faction, dict):  # Check if the faction is a dictionary
                    print(f"\nFaction Name: {faction.get('name', 'N/A')}")
                    print(f"Faction Type: {faction.get('type', 'N/A')}")
                    print(f"Members: {', '.join(faction.get('members', []))}")
                else:
                    print("Invalid data format in factions list.")

        print("\n---------------------")
    except FileNotFoundError as e:
        print(f"Error loading factions data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def display_state_data():
    """Display the state data in a formatted manner."""
    state_data = load_data("data/loyalties/factions/state.json")

    print("--- State Data ---\n")

    # Extract state information
    state_info = state_data.get("state_name", "N/A")
    capital = state_data.get("capital", "N/A")
    population = state_data.get("population", "N/A")
    economy = state_data.get("economy", {})
    factions = state_data.get("factions", [])

    # Print state info in a clean format
    print(f"State Name: {state_info}")
    print(f"Capital: {capital}")
    print(f"Population: {population}")

    # Print economy information
    print("\nEconomy:")
    if economy:
        industries = economy.get("industries", [])
        gdp = economy.get("gdp", "N/A")
        print(f"  Industries: {', '.join(industries) if industries else 'N/A'}")
        print(f"  GDP: {gdp}")
    else:
        print("  Economy data not available.")

    # Print factions data
    print("\nFactions:")
    if factions:
        for faction in factions:
            name = faction.get("name", "N/A")
            f_type = faction.get("type", "N/A")
            leader = faction.get("leader", "N/A")
            territory = faction.get("territory", "N/A")
            main_product = faction.get("main_product", "N/A")

            print(f"  - {name} (Type: {f_type}):")
            print(f"    Leader: {leader}")
            if f_type == "gang":
                print(f"    Territory: {territory}")
            if f_type == "corporation":
                print(f"    Main Product: {main_product}")
    else:
        print("  No factions found.")


def print_faction_details(faction):
    """Print details for a single faction."""
    name = faction.get("name", "N/A")
    f_type = faction.get("type", "N/A")
    leader = faction.get("leader", "N/A")
    territory = faction.get("territory", "N/A")
    main_product = faction.get("main_product", "N/A")

    print(f"  - {name} (Type: {f_type}):")
    print(f"    Leader: {leader}")
    if f_type == "gang":
        print(f"    Territory: {territory}")
    if f_type == "corporation":
        print(f"    Main Product: {main_product}")


def list_existing_characters(character_registry):
    """Display a list of existing characters and their entity IDs."""
    if not character_registry:
        print("No existing characters.")
        return None

    print("\nExisting characters:")
    for entity_id, character in character_registry.items():
        print(f"ID: {entity_id}, Name: {character.name}")

    return character_registry
