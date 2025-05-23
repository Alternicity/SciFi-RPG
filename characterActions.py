# characterActions.py

from location import Shop, CorporateStore
from base_classes import Location
import copy
import random
from visual_effects import loading_bar, RED, color_text
from conversation import Conversation
from menu_utils import get_menu_choice
from typing import Dict, Tuple, Any
from weapons import Weapon
# In characterActions.py
#from combat_actions import combat_actions placeholders
#from stealth_actions import stealth_actions


def attribute_test(attribute_value, difficulty=10, modifiers=0, verbose=False):
    """
    Simple attribute test: pass if attribute + mods > random threshold.
    """
    roll = random.randint(1, 20)
    total = attribute_value + modifiers
    if verbose:
        print(f"Attribute Test → Roll: {roll}, Attribute+Mods: {total}, Difficulty: {difficulty}")

        # Swiz tries to pick a lock with Dexterity 12
        #success = attribute_test(attribute_value=12, difficulty=14, modifiers=1, verbose=True)

    return total >= difficulty


def adversarial_attribute_test(
    attempt_value,
    resistance_value,
    attempt_mod=0,
    resistance_mod=0,
    wildcard_mod=0,
    simulate=False,
    verbose=False
):
    """
    General-purpose adversarial attribute test.
    Compares an attempt (e.g., intimidation, stealth) against a resistance (e.g., loyalty, intercept).
    Optional modifiers and wildcard allow contextual bonuses.
    Parameters:
    - simulate (bool): If True, skip random elements for AI decision planning.
    - verbose (bool): Print breakdown of the score if debugging.
    Returns:
    - bool: True if the attempt succeeds, False otherwise.
    """
    base_attempt = attempt_value + attempt_mod + wildcard_mod
    base_resist = resistance_value + resistance_mod

    if not simulate:
        attempt_roll = random.randint(0, 10)
        resist_roll = random.randint(0, 10)
        base_attempt += attempt_roll
        base_resist += resist_roll
        if verbose:
            print(f"[Verbose] Random roll → Attempt +{attempt_roll}, Resistance +{resist_roll}")

    if verbose:
        print(f"[Verbose] Final Attempt score: {base_attempt} vs Resistance score: {base_resist}")

    return base_attempt > base_resist

def handle_actions(character):

    """Handle character actions dynamically based on location and character behavior."""

    if character.location is None:
        print(f"{character.name} is not in any location.")
        return
    
    location = character.location
    available_actions = location.get_available_actions(character)

    # Filter actions before showing menu
    filtered_options = {
        name: func for name, func in available_actions.items() if action_is_available(character, name)
    }

    if not filtered_options:
        print(f"No available actions for {character.name} in this location.")
        return

    choice = get_menu_choice(filtered_options)

    if choice:
        _, action_func = filtered_options[choice]
        action_func()

def action_is_available(character, action_name):
    """Check if the action is available based on character behavior and location actions."""
    
    if character.location is None:
        return False  # No actions if no location
    
    location = character.location
    options = location.get_available_actions(character)

    return action_name in options


def visit_location(character, location=None):
    """Presents a menu to visit a location within the region."""
    from menu_utils import display_menu, get_available_options
    from location_utils import get_visitable_locations
    from characterActions import choose_location
    region = character.region
    locations = {}

    # If no location is passed, ask the player to choose one
    if location is None:
        locations = get_visitable_locations(region)
        if not locations:
            #print(f"There are no locations to visit in {region.name}.")
            return

    if not locations:
        #print(f"There are no locations to visit in {region.name}.")
        location = choose_location(character, region)

        if not location:  # If no valid location is selected, return early
            print("Error: No location was chosen! Returning to main menu.")
            return
    #is the following code now deprecated? choose_location(region) has already been called..
    choice = display_menu(locations)
    if not choice:
        print("Returning to the main menu.")
        return
    location = locations[choice][1]()  # Retrieve the selected location object
    
    #the following code is essential
    character.location = location
    location.characters_there.append(character)
    print(f"{character.name} enters {location.name} in {character.region}.")

    """ if isinstance(location, Shop):
        print(f"🧾 {location.name} shows you their current stock:")
        location.debug_print_inventory() """

    if not location:  # If no valid location is selected, exit
        print("Error: No location was chosen!")

        return
    


    # This code relates to dynamic menu options, does it belong in visit_location?
    options = get_available_options(location, character)  # Ensures options is a dict
    if not options:  # Prevent passing an empty list or dict
        print(f"There is nothing to do at {location.name}.")
        return
    
    print(f"Debug: from visit_location() - options type before display_menu() call: {type(options)}, value: {options}")
    while True:#This keeps the player in the location menu until they choose to leave
        choice = display_menu(options)  # Ensure display_menu gets a dict
    
        if choice and choice in options:
            _, action_func = options[choice]
            action_func()

        # Optionally, allow the player to return to location selection
            leave_option = next((key for key, (desc, _) in options.items() if "leave" in desc.lower()), None)
            if choice == leave_option:
                print(f"{character.name} leaves {location.name}.")
                return
        
def choose_location(character, region):
    """Displays available locations and allows player to select one."""
    from menu_utils import display_menu
    if not region.locations:
        print("Error: No locations available in this region!")  # Debugging print
        return None  #not  crash
    #print(f"Debug: Available locations: {[loc.name for loc in region.locations]}")  # Debugging line


    options = {idx: (loc.name, loc) for idx, loc in enumerate(region.locations, 1)}
    
    while True:#while True: loop for retrying input
        choice = display_menu(options)
        print(f"Debug: Raw input received from display_menu(): {repr(choice)}")  # Debugging line

        if not choice:  # Handle empty input
            print("Error: No input detected!")
            continue
        try:
            choice = int(choice)
        except ValueError:
            print("Error: Invalid choice (not a number)!")
            continue

        if choice not in options:
            print("Error: Invalid choice!")
            continue
        chosen_loc = options[choice][1]  # This is the actual Location object
        character.location = chosen_loc
        print(f"Chosen location: {chosen_loc.name}")
        return chosen_loc

def select_item_to_buy(shop):
    from menu_utils import get_menu_choice_from_list

    item_names = list(shop.inventory.items.keys())

    if not item_names:
        print("Nothing is available for sale.")
        return None

    choice = get_menu_choice_from_list(item_names, "Select an item to buy:")
    return choice

def buy(character, shop, item):
    location = character.location
    if not isinstance(shop, Shop):
        print("You can't buy things here!")
        return

    # Show inventory and funds
    from display import show_shop_inventory
    show_shop_inventory(character, shop)
    print(f"{character.name}'s bank card balance: ${character.wallet.bankCardCash}")
    print(f"{shop.name} current funds before purchase: ${shop.bankCardCash}")

    # Let player pick an item
    item_name = item.name  # Trust the passed-in item
    if not item or item.quantity <= 0:
        print("Item is out of stock.")
        return

    # Look up item object and price
    item_obj = shop.inventory.items.get(item_name)
    if not item_obj or item_obj.quantity <= 0:
        print("Item is out of stock.")
        return

    price = item_obj.price

    if character.wallet.bankCardCash < price:
        print(f"{character.name} can't afford the {item_name}.")
        character.adjust_self_esteem(-5)
        character.fun -= 1
        return

    print(f"\n📉 BEFORE purchase, shop inventory for {item_name}:")

    # Deduct funds. 
    character.wallet.bankCardCash -= price

    print(f"  Quantity in shop: {shop.inventory.items[item_name].quantity}")
    print(f"  Object ID: {id(shop.inventory.items[item_name])}")

    # Deepcopy item before giving it to character
    item_copy = copy.deepcopy(item_obj)
    item_copy.quantity = 1  # Important: avoid giving full stock amount
    character.inventory.add_item(item_copy)

    # Set ownership data after buying
    if hasattr(item_copy, "owner_name"):
        item_copy.owner_name = character.name
        item_copy.human_readable_id = f"{character.name}'s {item_copy.name}"

    # ✅ Decrease stock in the shop
    item_obj.quantity -= 1
    if item_obj.quantity <= 0:
        del shop.inventory.items[item_name]
    else:
        shop.inventory.items[item_name] = item_obj

    # Give money to shop
    location.bankCardCash += price
    print(f"{shop.name} funds after transaction: ${shop.bankCardCash}")

    # Mood & self-esteem logic
    if character.wallet.bankCardCash == 0:
        character.adjust_self_esteem(-5)
        print(f"{character.name} feels anxious after spending their last money.")
    else:
        character.adjust_self_esteem(5)
        print(f"{character.name} feels good after buying a {item_name}.")

    # Optional: boost fun
    if hasattr(character, "fun"):
        character.fun += 1

    print(f"{character.name} bought a {item_name} for ${price}.")
    print(f"{character.name}'s wallet after purchase: ${character.wallet.bankCardCash}")
    from display import show_character_details
    show_character_details(character)


def make_black_market_purchase(self, amount):
    """Make a purchase on the black market (only cash can be used)."""
    if self.wallet.spend_cash(amount):
        print(f"Black market purchase of {amount} successful.")
    else:
        print(f"Not enough cash for black market purchase.")

    

def pick_up_cashwad(self, cashwad):
    """Pick up a CashWad and add the value to the wallet."""
    print(f"Picked up a CashWad worth {cashwad.get_value()} cash.")
    cashwad.add_to_wallet(self.wallet)
    
    from create_game_state import get_game_state
    game_state = get_game_state()
    
def exit_location(character):
    from game_logic import gameplay
    """Handles exiting a location and return to gameplay."""

    if character.location:
        print(f"{character.name} leaves {character.location.name}.")

        # Remove character from location's character list
        if character in character.location.characters_there:
            character.location.characters_there.remove(character)

        # Reset character's location to None (they are not in any specific place)
        character.location = None

        # Return to main gameplay loop
        gameplay(character, character.region)
            
def eat():
    pass

def sleep():
    pass

def enjoy(character, location, object, otherCharacter):
    pass
    # character or group of them tries to raise their fun attribute which
    #might also raise their health and maybe morale

def steal(character, location, target_item=None, simulate=False, verbose=True):
    """Attempt to steal an item from the location inventory."""
    if not hasattr(location, 'inventory') or not location.inventory.items:
        if verbose:
            print(f"[Verbose] {location.name} has no items to steal.")
        print(f"{location.name} has no items to steal.")
        return

    # If no target item is specified, take the first available item
    if not target_item:
        target_item = next(iter(location.inventory.items.values()))

    # Defensive check
    if target_item.name not in location.inventory.items:
        if verbose:
            print(f"[Verbose] {target_item.name} not found in {location.name}'s inventory.")
        return

    # -- STEP 1: Prepare for adversarial test --

    # --- Verbose debug info ---
    if verbose:
        print(f"[Verbose] Attempting to steal {target_item.name} from {location.name}")

    # Attempt: Character's stealth
    stealth = character.skills.get("stealth", 0)

    # Resistance: Employees' observation (average, max, or total)
    employees = getattr(location, 'employees_there', [])
    if not employees:
        observation = 0  # Nobody watching!
    else:
        # Could use max, sum, or average depending on desired difficulty
        observation = max([e.skills.get("observation", 0) for e in employees])

    # Optional modifiers/hooks (for future)
    resistance_mod = getattr(location, "security_level", 0)  # placeholder
    attempt_mod = getattr(character, "criminal_modifier", 0)  # placeholder

    if verbose:
        print(f"[Verbose] Stealth: {stealth} | Observation: {observation}")
        print(f"[Verbose] Modifiers - Attempt: {attempt_mod}, Resistance: {resistance_mod}")

    success = adversarial_attribute_test(
        attempt_value=stealth,
        resistance_value=observation,
        attempt_mod=attempt_mod,
        resistance_mod=resistance_mod,
        wildcard_mod=0,
        simulate=simulate,
        verbose=verbose
    )

    if success:
        stolen_item = copy.deepcopy(target_item)
        location.inventory.remove_item(target_item.name)
        print(f"{character.name} {color_text('steals', RED)} a {stolen_item.name} from {location.name}.")
        character.inventory.add_item(stolen_item)
        
        if isinstance(stolen_item, Weapon):
            character.inventory.update_primary_weapon()
        character.update_motivations()

        # Update intimidation if item has intimidate attribute
        if hasattr(stolen_item, "intimidate"):
            character.skill["intimidation"] = character.skill.get("intimidation", 0) + stolen_item.intimidate
            if verbose:
                print(f"[Verbose] {character.name}'s intimidation increased by {stolen_item.intimidate} due to the {stolen_item.name}.")        
        loading_bar()
    else:
        print(f"{character.name} failed to steal the {target_item.name} from {location.name}.")
        # Optional: consequences or alerts go here (e.g., witnesses, reputation drop, security alert)



def influence(actor, target):
    print(f"{actor.name} influences {target.name}.")
    # Add influence logic here.
    #experiment with other data structures for action functions, and maybe kwargs
    #An influencer or other charcter with some scepticism attribute or function negates psy if they are in the same loaction or ..
    #VIP class currently has a self.influence = influence attribute
""" they attach/spread an anti-psy effect (Object?) to other characters which works the same

this can be generalised to other things, a
 spread(X) function for beliefs, loyalties, etc Contrast with charm() """


def talk_to_character(location, character):
    # legacy/general version
    people = getattr(location, "characters_there", [])
    if not people:
        print("No one here to talk to.")
        return

    # Build options from the 'people' list, not from 'character'
    options = {
        i + 1: (p.name, p)
        for i, p in enumerate(people)
    }

    selected = _select_with_cancel(options, cancel_label="Back")
    if not selected:
        return

    convo = Conversation(speaker=selected, listener=character)
    convo.start()
        
def talk_to_character_group(entity, initiator, context_name="here"):
    people = getattr(entity, "characters_there", [])
    if not people:
        print(f"No one is {context_name} to talk to.")
        return

    options = {
        i+1: (p.name, p)
        for i, p in enumerate(people)
    }


    selected = _select_with_cancel(options, cancel_label="Back")
    if not selected:
        return  # or re-display the shop menu if you're nested in a loop

    convo = Conversation(speaker=selected, listener=initiator)
    convo.start()

def talk_to_customer(location, character):
    non_employees = [
        c for c in location.characters_there
        if c not in getattr(location, "employees_there", [])
    ]
    if not non_employees:
        print("No customers here to talk to.")
        return

    options = {
    i + 1: (cust.name, cust)
    for i, cust in enumerate(non_employees)
}

    selected = _select_with_cancel(options, cancel_label="Back")
    if not selected:
        return

    convo = Conversation(speaker=selected, listener=character)
    convo.start()

def talk_to_employee(location, character):
    employees = getattr(location, "employees_there", [])
    if not employees:
        print("No employees here to talk to.")
        return

    options = {
        i+1: (emp.name, emp)
        for i, emp in enumerate(employees)
    }

    selected = _select_with_cancel(options, cancel_label="Back")
    if not selected:
        return

    convo = Conversation(speaker=selected, listener=character)
    convo.start()

def _select_with_cancel(options: Dict[int, Tuple[str, Any]], cancel_label="Cancel"):
    """Displays a selection menu with a cancel option and returns the selected item or None."""
    # Add cancel option at key 0
    menu = {0: (cancel_label, None)}
    menu.update(options)

    for key, (label, _) in menu.items():
        print(f"{key}: {label}")

    while True:
        choice = input("Choose an option (or 0 to cancel): ").strip()

        if not choice:
            print("No input detected. Please enter a number.")
            continue

        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        choice = int(choice)
        if choice in menu:
            _, value = menu[choice]
            return value
        else:
            print("Invalid choice. Try again.")    

def flirt(actor, target):
    print(f"{actor.name} flirts with {target.name}.")
    # Add flirt logic here.
    # success creates an attraction goal in a target character. cumulative. Can create simps
    #overuse with too many characters causes a status lowering event

def charm(actor, target):
    print(f"{actor.name} charms {target.name}.")
    # Add charm logic here.
    #target either individual or defined group
    #if succesfful their loyalty and maybe love increases

def switchPartner(actor, target, currentPartner):
    print(f"{actor.name} charms {target.name}.")
    # Add mechanic here, include animosity creation/increment
    #currentPartner = dumped AND newly_single AND enraged
    #newPartner = attached AND has_limerance 
    #character Status adjustments, loyalty adjutsments
    #may trigger judgement Event

def create_psyop(actor, target_group):
    print(f"{actor.name} creates a psyop targeting {target_group}.")
    # Add psyop logic here, creates event.
    #Create demand for a product or action or judgement or status adjustment

def reduceTax(accountant, faction):
    print(f"accountant.name lowers the tax burden on {faction.name} by x% until further notice")
    #actions for a private sector accountant

def squeezeTaxes(taxman, faction):
    print(f"taxman.name increases tax burden on {faction.name} by x% until further notice")

def reassureRivals(Boss, rivals):
    print(f"I sent them a message, I want no more hostilities")

def offerTruce(Boss, rivals):
    print(f"A cease to hostilities, I can't lose another son")

def offerFauxTruce(Boss, rivals):
    print(f"A cease to hostilities, I can't lose another son")
    #think(Until I know which one of you organized the hit, and then...)

def rob(character, location, target_item=None):
    print(f"{character.name} attempts to rob {location.name}")
    from events import Robbery
    from InWorldObjects import CashWad
    robbery_event = Robbery(instigator=character, location=location, weapon_used=True)
    robbery_event.target_item = target_item

    #if character attempts robbery sans weapon, handle it
    outcome = robbery_event.resolve()

    # This will depend on your Robbery.resolve() implementation
    if outcome == "success":
        character.update_motivations()

    elif outcome == "resisted":
        print(f"The robbery was resisted! Civilians may call guards.")
    elif outcome == "detected":
        print(f"Authorities have been alerted to the robbery at {location.name}!")

    return robbery_event


def sowDissent(Character, rivals):
    print(f"I sent them a message, I want no more hostilities")

def examine_item(item):
    return getattr(item, "human_readable_id", item.name)

def shakeDown(character, location, targetResource):
    print(f"Your regular protection payment is due")

def patrol(character, region, targetObjects):
    print(f"What do we have here?")
    # a character moves through a list of locations, or regions and locations, noticing objects
    #and matching them against a table of actions appropriate given that objects attributes, faction etc
    #this is a (maybe) behaviour tree level AI action
    #examples: look for rival gang members shaking down or robbing locations or characters in own territory
    #look for stealable objects
    #look for new economic sources to shakedown
    #look for rival gang members, adn if disposition to violence if high enough and resources permit, and morale
    #is high enough (morale minus rivals apparent power level) then attack them

def snitch(character, target, location):
    print(f"Im calling the cops")
    #non aligned, corporate and especially VIP characters will do this if they feel their interests are threatened
    #or they have a high law loyalty. Might gain some snithc reputation from it, and enmity from a gang or
    #the character they are snitching on. Violent and loyal gangs might seek revenge or deterene actions
    #which if succesful might deter further snitchings

def get_available_actions(character):
#possibly deprecated in favour of menu options
    location = character.location
    available_actions = {
        "Eat": eat(),
        "Talk": talk_to_character(location),
        "Flirt": flirt(),
        "Steal": steal(),
    }

# Merge actions dynamically, here for future compatibility
#available_actions.update(combat_actions)
#available_actions.update(stealth_actions)



def call_police(self, crime_type, region, location):
    print(f"{self.name} calls the police: '{crime_type} at {location.name}, {region}!'")
    # Then trigger a new Event or dispatch responders

def interact_with_partner(self):
    if self.partner:
        print(f"{self.name} talks to {self.partner.name} affectionately.")
        self.adjust_self_esteem(2)
        self.partner.adjust_self_esteem(2)
