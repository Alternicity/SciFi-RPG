# characterActions.py

from location import Shop, CorporateStore
from base_classes import Location
from functools import partial
import copy
# In characterActions.py
#from combat_actions import combat_actions placeholders
#from stealth_actions import stealth_actions

def handle_actions(character):
    from menu_utils import get_menu_choice
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
    
    # If no location was passed, prompt the player to choose one
    if not locations:  #line 65
        #print(f"There are no locations to visit in {region.name}.")
        location = choose_location(character, region)

        if not location:  # If no valid location is selected, return early
            print("Error: No location was chosen! Returning to main menu.")
            return
    #is the following code now deprecated? choose_location(region) has already been called..
    print("\nWhere would you like to go?")
    choice = display_menu(locations)
    if not choice:
        print("Returning to the main menu.")
        return
    location = locations[choice][1]()  # Retrieve the selected location object
    
    #the following code is essential
    character.location = location
    location.characters_there.append(character)
    print(f"{character.name} enters {location.name} in {character.region}.")

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

    # Let player pick an item
    item_name = select_item_to_buy(location)
    if not item_name:
        print("Purchase cancelled.")
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

    # Deduct funds. 
    character.wallet.bankCardCash -= price

    # Deepcopy item before giving it to character
    item_copy = copy.deepcopy(item_obj)
    item_copy.quantity = 1  # Important: avoid giving full stock amount
    character.inventory.add_item(item_copy)

    # ✅ Decrease stock in the shop
    item_obj.quantity -= 1
    if item_obj.quantity <= 0:
        del shop.inventory.items[item_name]
    else:
        shop.inventory.items[item_name] = item_obj

    # Give money to shop
    location.bankCardCash += price

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
    # cahracte or group of them tries to raise their fun attribute which
    #might also raise their health and maybe morale

def steal(character, location, targetResource):
    print(f"Ok, I got it, let's go")
    #this action might trigger an event
    possibleEvents = {
    "success": "leave_quietly",
    "detected": "escape_fast",
    "parsimony_opportunity": "secondarySteal",
    "triggered_trap": "consequences",
    }


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
    """Let the player talk to a character in the location."""
    if not location.characters:
        print("No one is here to talk to.")
        return

    # Display characters present
    character_options = {str(i+1): (char.name, char) for i, char in enumerate(location.characters)}
    choice = get_menu_choice(character_options)

    if choice and choice in character_options:
        selected_character = character_options[choice][1]
        print(f"You start talking to {selected_character.name}.")  # Placeholder for dialogue system
    else:
        print("Invalid choice.")
        
def flirt(actor, target):
    print(f"{actor.name} flirts with {target.name}.")
    # Add flirt logic here.
    # success creates an attraction goal in a target character. cumulative.
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

def rob(character, location, targetResource):
    print(f"Gimme the CASH!")

def sowDissent(Character, rivals):
    print(f"I sent them a message, I want no more hostilities")

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

    location = character.location
    available_actions = { #line 200
        "Eat": eat(),
        "Talk": talk_to_character(location),
        "Flirt": flirt(),
        "Steal": steal(),
    }

# Merge actions dynamically, here for future compatibility
#available_actions.update(combat_actions)
#available_actions.update(stealth_actions)

def observe (location):
    #include noticing increased xyz activity
    pass