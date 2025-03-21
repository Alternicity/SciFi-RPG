# characterActions.py

from location import Shop, CorporateStore
from base_classes import Location
from functools import partial

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


def visit_location(character, region):
    """Handles visiting a location dynamically."""
    chosen_location = choose_location(region)  # This function should let the player pick

    if chosen_location is None:
        print("Error: No location was chosen!")  # Debugging print
        return
    
    character.location = chosen_location
    chosen_location.characters_there.append(character)

    print(f"{character.name} enters {chosen_location.name}.")
    
    # Get menu dynamically
    from menu_utils import display_menu
    while True:
        options = chosen_location.get_menu_options(character)
        choice = display_menu(options)
        if choice == "3":  # "Leave" option
            break
        action = options.get(choice, (None, None))[1]
        if action:
            action()

def choose_location(region):
    """Displays available locations and allows player to select one."""
    from menu_utils import display_menu
    
    locations = region.get_locations()
    if not locations:
        print("Error: No locations available in this region!")  # Debugging print
        return None  # Ensure function doesn't crash

    options = {idx: (loc.name, loc) for idx, loc in enumerate(locations, 1)}
    
    choice = display_menu(options)
    
    if choice not in options:
        print("Error: Invalid choice!")  # Debugging print
        return None

    print(f"Chosen location: {options[int(choice)][1].name}")  # Debugging print
    return options[int(choice)][1]  # Returns the selected location object


def buy(character, location):
    """Handle buying an item from a shop."""
    if not isinstance(location, Shop):
        print("You can't buy things here!")
        return
    
    # Display shop inventory and get user's choice
    chosen_item = location.select_item_for_purchase()
    
    if not chosen_item:
        print("You didn't select anything to buy.")
        return
    
    amount = character.calculate_item_cost(chosen_item)

    # Determine if legal or black market purchase
    if chosen_item.legality is True:
        payment_method = input("Pay with (1) Cash or (2) Bank Card? ")
        use_bank_card = payment_method == "2"
        
        if use_bank_card:
            if character.wallet.spend_bankCardCash(amount):
                print(f"Purchase of {chosen_item.name} using bank card successful.")
            else:
                print(f"Not enough bank card balance for purchase.")
        else:
            if character.wallet.spend_cash(amount):
                print(f"Purchase of {chosen_item.name} using cash successful.")
            else:
                print(f"Not enough cash for purchase.")
    elif chosen_item.legality is False:
        character.make_black_market_purchase(amount)
    else:
        raise ValueError(f"Unknown legality type: {chosen_item.legality}")


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
    
from create_game_state import game_state
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