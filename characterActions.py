# characterActions.py

from location import Shop, CorporateStore
from base_classes import Location
from functools import partial

# In characterActions.py
#from combat_actions import combat_actions placeholders
#from stealth_actions import stealth_actions

def handle_actions(character):
    """Handle character actions dynamically."""

    if character.location is None:
        print(f"{character.name} is not in any location.")
        return
    
    location = character.location
    available_actions = location.get_available_actions(character)

    def action_is_available(action_name):
        """Check if the action is available based on character behavior."""
        return character.prefers_action(action_name)

    # Filter actions before showing menu
    filtered_options = {name: func for name, func in available_actions.items() if action_is_available(name)}

    choice = get_menu_choice(filtered_options)

    if choice:
        _, action_func = available_actions[choice]
        action_func()

def visit_location(character, region, location):
    """Handles the process of visiting a selected location."""
    from display import show_locations_in_region
    from menu_utils import get_menu_choice
    from location import Region #tmp for debug below
    region = character.region  # Get character's current region

    # 🚨 Debugging: Check if region is valid
    if not isinstance(region, Region):
        print(f"🚨 ERROR: character.region is {type(region)}, expected Region object!")
        return  # Exit the function early

    locations = getattr(region, "locations", [])
    if not locations:
        print(f"No locations available in {region.name}.") #line 59

    
    # If the character is already in a location, remove them from the old one
    if character.location:
        character.location.characters_there.remove(character)

    character.location = location  # Update the character's current location
    
    #character.region = location.region  this line caused a region/string error

    # Add the character to the new location's character list
    location.characters_there.append(character)

    print(f"{character.name} enters {location.name}.")
    
    # Check if it's a vendor
    if isinstance(location, Shop):
        #show a shop specific menu, see also location_menu
        from display import show_shop_inventory
        show_shop_inventory(location)


    elif isinstance(location, CorporateStore):
        print(f"{location.name} is a corporate store. Items are issued based on status.")
    else:
        print(f"{location.name} is not a vendor.")

        return
    
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

from menu_utils import get_menu_choice #line 113
def action_is_available(character, action_name, action_tuple):
    """Check if the action is available based on character behavior and location actions."""
    
    if character.location is None:
        return False  # No actions if no location
    
    location = character.location
    options = location.get_available_actions(character)

    return action_name in options



def talk_to_character(location):
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