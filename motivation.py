#motivation.py 
from status import Status

class Motivation:
    VALID_MOTIVATIONS = {
        "earn_money": 5,
        "eat": 0,  # Starts at 0, increases with hunger
        "sleep": 0,  # Increases with fatigue
        "shelter": 3,
        "have_fun": 2,
        f"gain_{Status.LOW.value}": 4,
        f"gain_{Status.MID.value}": 5,
        f"gain_{Status.HIGH.value}": 6,
        f"gain_{Status.ELITE.value}": 7,
        "protect_vip": 5,
        "steal_money": 4,
        "steal_object": 3,
        "rob": 3,
        "shakedown": 3, #shakeDown(character, location, targetResource) #extract value through implied threat
        "escape_danger": 8,  # Very urgent in dangerous situations
        "virtue_signal": 1,
        "find_partner": 3,
        "switch_partner": 2, #hypergamy exists here, see switchPartner(actor, target, currentPartner): Must be a perceived upgrade
        "influence": 4, #influence(actor, target): Change some other characters variables. See Charm() and create_psyop() and influece()
        "increase_popularity": 3, #see charm(actor, target):
        "decrease_hostilities": 4, #see reassureRivals(Boss, rivals): and offerTruce(Boss, rivals): but also offerFauxTruce(Boss, rivals):
        "sow_dissent": 4, #sowDissent(Character, rivals) #weaken a rival or enemy factions loyalities
        "patrol": 3, #patrol(character, region, targetObjects) A key FSM action for low level faction members
        "snitch": 6, #snitch(character, target, location) If a character sees a crime, or feels threatened by faction behaviour
    }

    def __init__(self, initial_motivation="earn_money"):
        if initial_motivation not in self.VALID_MOTIVATIONS:
            print(f"Warning: Invalid motivation '{initial_motivation}'. Defaulting to 'earn_money'.")
            initial_motivation = "earn_money"
        self.current = initial_motivation


    def change_motivation(self, new_motivation):
        if new_motivation in self.VALID_MOTIVATIONS:
            print(f"Motivation changed to {new_motivation}")
            self.current = new_motivation
        else:
            print(f"Invalid motivation: {new_motivation}")

    def __str__(self):
        return self.current

    """ def __init__(self, name, behaviour="passive", motivation="earn_money"):
        self.name = name
        self.behaviour = self.Behaviour(behaviour)
        self.motivation = self.Motivation(motivation) """

    """ def display_character_state(self):
        print(
            f"{self.name}'s behaviour: {self.behaviour.current}, motivation: {self.motivation.current}"
        ) """

def check_needs(character, is_player=False):
    """Check character needs, determine the strongest motivation, and print messages."""
    
    messages = []
    motivations = {}

    # Link needs to motivations
    if character.needs["physiological"] > 7:
        messages.append("hungry")
        motivations["eat"] = character.needs["physiological"]

    if character.needs["physiological"] > 9:
        messages.append("starving")
        motivations["eat"] = max(motivations.get("eat", 0), character.needs["physiological"] + 1)

    if character.needs["physiological"] > 8:
        messages.append("tired")
        motivations["sleep"] = character.needs["physiological"]

    if character.needs["safety"] > 8:
        messages.append("worried about safety")
        motivations["escape_danger"] = character.needs["safety"]

    if character.needs["love_belonging"] > 8:
        messages.append("lonely")
        motivations["find_partner"] = character.needs["love_belonging"]

    # Determine the most urgent motivation
    if motivations:
        strongest_motivation = max(motivations, key=motivations.get)
    else:
        strongest_motivation = "earn_money"  # Default fallback

    # Display status messages
    if messages:
        status_msg = ", ".join(messages)
        if is_player:
            print(f"I am {status_msg}.")
        else:
            print(f"{character.name} is {status_msg}.")

    return strongest_motivation