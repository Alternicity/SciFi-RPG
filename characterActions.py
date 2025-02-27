# characterActions.py

from location import Shop, CorporateStore
from base_classes import Location
from functools import partial

def move_character(character, new_region=None, new_location=None):
    """Moves a character to a new region or location."""
    if character.current_location:
        # Remove character from the current location's character list
        character.current_location.remove_character(character)

    # Update character's current location
    character.current_location = Location(region=new_region, location=new_location)

    if new_location:
        # Add character to the new location's character list
        new_location.add_character(character)

    print(f"{character.name} has moved to {new_location.name if new_location else new_region.name}.")

def visit_location(character, region):
    """Allows a character to visit a location in their current region."""

    from display import show_locations_in_region
    from menu_utils import get_menu_choice

    region = character.region  # Get character's current region
    locations = getattr(region, "locations", [])

    if not locations:
        print(f"No locations available in {region.name}.")
        return

    # Build menu options
    
    options = {
            "1": ("Show Locations in Detail", lambda: show_locations_in_region(region, region.locations))
        }

    for idx, location in enumerate(region.locations, start=2):  # Use region.locations directly
        options[str(idx)] = (f"Visit {location.name}", partial(visit_selected_location, character, location))

        options[str(len(region.locations) + 2)] = ("Back", lambda: print("Returning to previous menu."))  # Back option

        # Display menu and get user choice
        choice = get_menu_choice(options)  # Get user input safely

        # Execute selected action
        if choice:
            selected_action = options[choice][1]
            selected_action()  # Call the function directly HERE location
        else:
            print("Invalid selection. Please try again.")


def visit_selected_location(character, location):
    """Handles the process of visiting a selected location."""

    character.location = location  # Update the character's current location
    character.region = location.region  # Ensure the region updates if needed
    print(f"{character.name} enters {location.name}.")
    #note there also exists move_character()

    # Check if it's a vendor
    if isinstance(location, Shop):
        from display import show_shop_inventory
        show_shop_inventory(location)
    elif isinstance(location, CorporateStore):
        print(f"{location.name} is a corporate store. Items are issued based on status.")
    else:
        print(f"{location.name} is not a vendor.")

            
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