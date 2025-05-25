#menu_utils.py
from tabulate import tabulate
from display import display_world, show_shop_inventory
from typing import Dict, Any
from create_game_state import get_game_state
from InWorldObjects import ObjectInWorld
# Ensure game_state is initialized correctly before use
game_state = get_game_state()
    

def main_menu(all_locations, all_characters):
    global game_state
    game_state = get_game_state()

    while True:
        """Display the main menu and return the user choice. Not a gameplay menu itself"""
        print("\n=== Main Menu ===")
        print("1: Play/Test Game")
        print("2: Show world")
        print("3: Run Simulation")
        print("6: Exit")

        choice = get_user_choice(6)
        if choice == 0:  # User chose "Play/Test Game"
            selected_character, region = select_character_menu()
            if selected_character:
                from game import gameplay  # Import gameplay here to avoid circular imports
                gameplay(selected_character, region)  # Start gameplay

        elif choice == 1:  # User chose "Show World"
            from create import all_regions
            display_world(all_regions)
        elif choice == 2:  # Simulation mode
            from simulation import run_simulation
            run_simulation(all_characters, num_days=int(input("How many days to simulate? ")))

        elif choice == 5:  # User chose "Exit"
            print("Exiting game...")
            break  # Exit the loop and end the program
        else:
            print("Invalid selection. Please try again.")


from location import Shop
from display import display_employees
from typing import List

class GameplayMenu:
    def __init__(self):# the static  menu options
        self.menu_options: List[str] = [
            "Visit Location",
            "Move to another Region",
            "Display Characters Summary",
            "Display Factions",  # New consolidated option
            "Dev",
            "Exit Gameplay",  # Always last
        ]

    def get_options(self):
        """Convert menu_options to the format required"""
        return self.menu_options

class DisplayFactionsMenu:
    def __init__(self):
        self.menu_options: List[str] = [
            "Display Corporations",
            "Display Gangs",
            "Display The State",
            "Display Civilian Population",
            "Display Filtered Character Summary",
            "Return to previous menu",
        ]

def get_display_factions_option_functions(self, game_state):
    from display import display_corporations, display_gangs, display_state, display_civilians, display_filtered_character_summary
    return {
        1: ("Display Corporations", lambda: display_corporations(game_state.corporations)),
        2: ("Display Gangs", lambda: display_gangs(game_state)),
        3: ("Display The State", lambda: display_state(game_state.state)),
        4: ("Display Civilian Population", lambda: display_civilians(game_state.civilians)),
        5: ("Display Filtered Character Summary", lambda: display_filtered_character_summary(game_state.characters)),
        6: ("Return to previous menu", lambda: None)
    }

def run(self, game_state):# This name must change, also game:state is passed in and this breaks the design pattern
    while True:
        print("\n=== Display Factions ===")
        options = self.get_option_functions(game_state)
        choice = get_menu_choice(options)
        if choice == "Return to previous menu":
            break

def show_shop_inventory_and_run_menu(character, location):
    show_shop_inventory(character, location)# just print
    ShopPurchaseMenu(character, location).run()# just one run call

def get_available_options(location, character):
    """Determine available menu options based on character and location."""
    from characterActions import talk_to_character, talk_to_employee, talk_to_customer, rob, steal
    from game_logic import gameplay
    available_options = {}

    if location is None:
        print(f"In transit; {character.name} is in {character.region} but no specific location")
        return available_options  # Return empty dict instead of list

    option_list = []  # Collect options before converting to dict

    #print(f"Debug: Checking available options for {location.name}.")

    # Location-based actions
    if hasattr(location, "employees_there"):
        employee_names = {emp.name for emp in location.employees_there}
    else:
        employee_names = set()
        print(f"Debug: {location.name} has employees_there: {[emp.name for emp in location.employees_there]}")

    if hasattr(location, "characters_there"):
        non_employee_chars = [char for char in location.characters_there if char.name not in employee_names]
        print(f"Debug: {location.name} has characters_there (non-employees): {[char.name for char in non_employee_chars]}")

    #consolidate
    if hasattr(location, "employees_there") and location.employees_there:
        option_list.append(("Display Employees", lambda: display_employees(location)))


    if hasattr(location, "employees_there") and location.employees_there:
        option_list.append(("Talk to an Employee", lambda: talk_to_employee(location, character)))

    if hasattr(location, "characters_there") and location.characters_there:
        non_employees = [char for char in location.characters_there if char not in location.employees_there]
        if non_employees:
            option_list.append(("Talk to a Customer", lambda: talk_to_customer(location, character)))
    
    region = character.location.region
    option_list.append(("Exit Shop", lambda: return_to_region_menu(character)))
    #should this unindented one space? It aligns with if hasattr(location, "characters_there") above

    # Character-based actions
    #print(f"Debug: {character.name} preferred actions: {character.get_preferred_actions()}")

    from base_classes import Location
    if not isinstance(location, Location):
        print(f"Error: Expected a Location, but got {type(location).__name__}")
        return {}
    if location.robbable and "Rob" in character.get_preferred_actions():
        option_list.append(("Rob the Place", lambda: rob(character, location, target_item=None)))
        #update above line to pass specified target
        #should we be instantiating a Robbery object here_
        #print(f"Debug: {character.name} can rob {location.name}, adding 'Rob' option.")

    # Allow stealing if location has stealable inventory and character prefers stealth
    # Check if there are any stealable ObjectInWorld items present
    if hasattr(location, "inventory"):
        #print(f"[DEBUG] {location.name} has inventory attribute.")
        if location.inventory.items:
            # Cleanest (uses your custom __iter__)
            #print(f"[DEBUG] {location.name} has items in inventory: {[item.name for item in location.inventory]}")
            if "Steal" in character.get_preferred_actions():
                print(f"[DEBUG] {character.name} prefers stealing.")
                for item in location.inventory:
                    #print(f"[DEBUG] Checking item {item.name} ({type(item).__name__})")

                    if isinstance(item, ObjectInWorld):
                        #print(f"[DEBUG] {item.name} is an ObjectInWorld. Adding to steal options.")
                        option_list.append((f"Steal {item.name}", lambda i=item: steal(character, location, i)))
            else:
                print(f"[DEBUG] {character.name} does not prefer stealing.")
        else:
            print(f"[DEBUG] {location.name} inventory is empty.")
    else:
        print(f"[DEBUG] {location.name} has no inventory.")

                #If you have some locations like Park or Alley that don’t carry an inventory at all, this code will now safely skip them.


    # Include predefined `menu_options` in `Shop`
    if hasattr(location, "menu_options") and isinstance(location.menu_options, list):
        for action_name in location.menu_options:
            if action_name == "View Shop Inventory":
                option_list.append((
                    action_name,
                    lambda loc=location: show_shop_inventory_and_run_menu(character, loc)
                ))
    # Convert the list to a dictionary
    available_options = {idx + 1: (desc, func) for idx, (desc, func) in enumerate(option_list)}

    #print(f"Debug: Final available options for {location.name}: {available_options}")

    return available_options  # Now always a dictionary

def return_to_region_menu(character):
    from game_logic import gameplay

    region = character.location.region  #perhaps we should experiment with alternatives to these
    location = character.location

    # Remove character from current location
    if location and character in location.characters_there:
        location.characters_there.remove(character)

    # Optionally, reset character's location to None if you want to simulate "wandering" the region
    character.location = None

    # Add character back to region-level character list if not already present
    if character not in region.characters_there:
        region.characters_there.append(character)

    print(f"{character.name} exits and returns to {region.name}.")

    gameplay(character, region)


def get_menu_choice_from_list(options, prompt="Choose one:"):
    #for now this is only used for buying in shops
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = input(prompt + " ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(options):
            return options[index]
    except ValueError:
        pass
    print("Invalid choice.")
    return None


def get_event_menu_options(character, location):
    active_events = [] #placeholder to avoid this being marked as undefined below
    menu_items = []
    for event in active_events:# active_events should be a global or passed-in list
        if event.affects(location):
            menu_items.extend(event.get_menu_options(character))
    return menu_items

def build_gameplay_menu(location, character):
    """Currently Combines location-based options with general gameplay menu."""
    location = character.location  # Get location from character
    region = character.region
    
    #print(f"Debug: From build_gameplay_menu calling get_available_options() with {type(location).__name__} instead of Location")
    options = get_available_options(location, character) #add event

    if not isinstance(options, dict):
        print(f"Error: get_available_options did not return a dictionary! Type: {type(options)}")
        options = {}  

    # Ensure options is in the correct format; deduplication logic
    seen = set()
    deduped_options = {}
    idx = 1
    for _, (desc, func) in options.items():
        if desc not in seen:
            deduped_options[idx] = (desc, func)
            seen.add(desc)
            idx += 1

    options = deduped_options 
    return options 


def get_menu_choice(options, filter_func=None):
    """Displays a menu and returns the chosen option, filtering actions if needed."""
    if filter_func:
        options = {k: v for k, v in options.items() if filter_func(v)}

    if not options:
        print("No available options, from get_menu_choice")
        return None

    print("\nAvailable actions:")
    for key, (desc, action) in options.items():
        print(f"{key}: {desc}")

    while True:
        choice = input("Choose an option: ").strip()


        if not choice:  # Handle empty input
            print("Error: No input detected! Please enter a number.from get_menu_choice")
            continue

        if choice.isdigit():
            choice = int(choice)
            if choice in options:
                desc, action = options[choice]
                print(f"You selected: {desc}")
                if action:
                    action()  # Call the associated function
                return desc
            else:
                print("Invalid choice. Try again.")
        else:
            print("Please enter a number.")

class ShopPurchaseMenu:
    def __init__(self, character, shop):
        assert hasattr(shop, "inventory"), "ShopPurchaseMenu expects a Shop object with an 'inventory' attribute"
        assert hasattr(character, "wallet"), "ShopPurchaseMenu expects a Character object with a 'wallet' attribute"
        print(f"[DEBUG] ShopPurchaseMenu created with shop: {shop.name}, character: {character.name}")
        self.character = character
        self.shop = shop

    def get_purchase_options(self):
        from characterActions import buy
        """Returns a dict of {index: (desc, func)} for items the player can buy."""
        purchase_options = {}
        for i, item in enumerate(self.shop.inventory, start=1):
            label = f"Buy {item.name} - ${item.price} ({item.quantity} in stock)"
            purchase_options[i] = (label, lambda it=item: buy(self.character, self.shop, it))  # Bind item
            
        cancel_index = len(purchase_options) + 1
        purchase_options[cancel_index] = ("Cancel", lambda: None)
        return purchase_options

    def run(self):
        print("\n=== Buy Items from Shop ===")
        options = self.get_purchase_options()
        choice = get_menu_choice(options)
        
        if choice:
            desc, action = options.get(choice, (None, None))
            if action:
                action()  # Perform the selected action


def shop_options(shop, character):
    return ShopPurchaseMenu(shop, character).get_options()
    #allow future dynamic menus to incorporate ShopPurchaseMenu logic without 
    #entering its run loop, useful for faction-directed purchases or auto-buy logic.

def get_user_choice(max_choice: int) -> int:
    """Gets user input for main menu selection safely."""
    try:
        choice = int(input("Enterx your choice: ")) - 1
        if 0 <= choice < max_choice:
            return choice
        print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return None

from character_creation_funcs import player_character_options, instantiate_character
from display import show_character_details

#from main import get_all_regions, get_factions
def select_character_menu():
    """Displays the character selection menu, instantiates the chosen character, and returns it."""
    
    # Get character options
    from create_game_state import get_game_state
    game_state = get_game_state()

    all_regions = game_state.all_regions
    factions = game_state.factions
    character_options = player_character_options(all_regions, factions)
    #print("Factions available:", [f.name for f in factions])

    if not character_options:
        print("No characters available for selection.")
        return None, None

    print("\nSelect a character:")

    for idx, char_data in enumerate(character_options, start=1):
        #print(f"[DEBUG] char_data = {char_data}")
        #print(f"{idx}. {char_data['name']} the {char_data['class'].__name__}")
        faction_name = char_data.get("faction_name") or "Factionless"
        char_class = char_data.get("class", type(char_data)).__name__
        name = char_data.get("name", "Unknown")
        print(f"{idx}. {name}, {char_class}, Faction: {faction_name}")
    else:
        # Fallback if somehow a string or object snuck in
        faction_name = "Factionless"
        char_class = type(char_data).__name__
        name = getattr(char_data, "name", str(char_data))

    #print(f"{idx}. {name}, {char_class}, Faction: {faction_name}")

    while True:
        try:
            choice = int(input("Enter the number of your chosen character: ")) - 1
            if 0 <= choice < len(character_options):
                selected_data = character_options[choice]
                selected_character = instantiate_character(selected_data, all_regions, factions)
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"[DEBUG] Selected character: {selected_character}")
    print(f"[DEBUG] Selected character type: {type(selected_character)}")

    # Show selected character details
    show_character_details(selected_character)
    #print("show_character_details(selected_character) has been called.")

    return selected_character, selected_character.region



def location_menu(character, location):#deprecated?
    """Menu for interacting with a location dynamically."""
    while True:
        available_options = get_available_options(character, location)
        print(f"Debug: location_menu() - get_available_options() returned {type(available_options)}, {available_options}")
        
        #here associate the menu_options from the location with appropriate functions
        
        if not available_options:
            print("No actions available here.")
            return
        
        # Show menu dynamically
        print("\nAvailable actions:")
        for index, (desc, _) in enumerate(available_options, start=1):
            print(f"{index}: {desc}")

        choice = input("location_menu> Choose an option: ").strip()
        
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(available_options):
                _, action_func = available_options[choice_index]
                action_func()
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

        if location.is_workplace:  # Example condition to exit after an action
            break


def display_menu(options: dict):
    """Displays a dynamic menu and returns the chosen action."""
    if not options:
        print("No available options, from display_menu")
        return None
    
    while True:
        print("\nAvailable options:")
        for key, (desc, _) in options.items():
            print(f"{key}: {desc}")
    
    
        choice = input("Choose an option: ").strip()
        print(f"Debug: User entered {repr(choice)}")  # Debugging line

        if choice.isdigit():
            choice = int(choice)
            if choice in options:
                return choice  # Return valid selection

        print("Invalid choice. Try again.")
        
        return choice  # Ensure input is returned

def select_item_for_purchase(shop):
    """Let the player choose an item to buy."""
    if not shop.inventory.items:  # Ensure inventory exists and has items
        print("The shop is empty.")
        return None

    shop.show_inventory()  # This should print the inventory

    # Allow player to select an item
    item_name = input("Enter the name of the item you want to buy: ").strip()
    return item_name if item_name else None  # Return the item name if provided

#marked for deletion
    """ print("Available items:")
    item_options = {str(i+1): item for i, item in enumerate(shop.inventory)}

    choice = get_menu_choice(item_options)
    return item_options.get(choice) """
