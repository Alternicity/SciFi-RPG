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
        "join_gang": 5,
        "join_faction": 5,
        "obtain_weapon": 5,
        "obtain_ranged_weapon": 5,
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

    def update_motivations(self, motivation=None, urgency=None):
        """Update motivations with optional new data."""
        
        if motivation:
            if motivation in self.motivations:
                self.motivations[motivation] += urgency or 1
            else:
                self.motivations[motivation] = urgency or 5
            return  # Early exit after update

        # Default case: just make sure something is in motivations
        if not self.motivations:
            self.motivations["earn_money"] = 5

    def refresh_from_memory(self, memories):
        """Reinforce motivations based on memory importance or tags."""
        for mem in memories:
            for tag in mem.tags:
                if tag in VALID_MOTIVATIONS:
                    urgency_boost = mem.importance
                    if tag in self.motivations:
                        self.motivations[tag] += urgency_boost
                    else:
                        self.motivations[tag] = urgency_boost
                        """ The NPC can now reinforce motivations like this:
                        mm.refresh_from_memory(npc.memory_list) """

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







    

    