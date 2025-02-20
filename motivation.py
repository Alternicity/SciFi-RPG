#motivation.py 
from status import Status

#see also def gameplay for some motivation code, when making AI
VALID_MOTIVATIONS = {
        "earn_money": 5,
        "eat": 0,  # Starts at 0, increases with hunger
        "sleep": 0,  # Increases with fatigue
        "shelter": 3,
        "have_fun": 2,
        "find_safety": 9,
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
        "snitch": 2, #snitch(character, target, location) If a character sees a crime, or feels threatened by faction behaviour
    }

class MotivationManager:
    """Handles NPC motivations dynamically, allowing updates without wiping existing motivations."""

    def __init__(self, character):
        self.character = character
        self.motivations = {}  # Store motivations with urgency levels

    def update_motivations(self):
        """Dynamically update motivations based on needs but without removing existing ones."""
        
        # Define need-motivation links
        need_mappings = {
            "physiological": [("eat", 7), ("sleep", 8)],  
            "safety": [("escape_danger", 8)],
            "love_belonging": [("find_partner", 8)],
            "esteem": [("gain_status", 7)],
            "self_actualization": [("pursue_dreams", 7)],
        }

        # Update motivation urgency based on needs
        for need, mappings in need_mappings.items():
            for motivation, threshold in mappings:
                if self.character.needs[need] >= threshold:
                    urgency = self.character.needs[need]  # Use need level as motivation urgency
                    self.motivations[motivation] = urgency

        # Ensure at least one default motivation exists
        if not self.motivations:
            self.motivations["earn_money"] = 5

    def get_highest_priority_motivation(self):
        """Returns the most urgent motivation."""
        return max(self.motivations, key=self.motivations.get, default="earn_money")

    def get_motivations(self):
        """Returns motivations sorted by urgency."""
        return sorted(self.motivations.items(), key=lambda x: x[1], reverse=True)

    def get_urgent_motivations(self, threshold=7):
        """Returns a list of motivations with urgency above a threshold."""
        return [motivation for motivation, urgency in self.motivations.items() if urgency >= threshold]

    def get_default_urgency(motivation):
        """Returns the default urgency for a given motivation."""
        return VALID_MOTIVATIONS.get(motivation, 5)  # Default fallback


#This function might be useful for If you want manual motivation
#  overrides (e.g., forcing an NPC to change behavior suddenly)
def change_motivation(self, name, urgency=None):
    """Manually overrides a motivation's urgency or adds a new one."""
    if name not in VALID_MOTIVATIONS:
        print(f"Invalid motivation: {name}")
        return

    if urgency is None:
        urgency = VALID_MOTIVATIONS[name]  # Default urgency

    self.motivation_manager.motivations[name] = urgency  # Update urgency dynamically




    

    