#motivation.py 
from status import StatusLevel

class Motivation:
    def __init__(self, type, urgency, target=None, status_type=None, source=None):
        self.type = type  #  "join_gang"
        self.urgency = urgency  # integer
        self.target = target  #  "e.g. Red Fangs"
        self.status_type = status_type  #  "criminal"
        self.source = source  #  memory, event, etc.

    def __repr__(self):
        desc = f"{self.type} (urgency {self.urgency})"
        if self.target:
            desc += f", target: {self.target}"
        if self.status_type:
            desc += f", status: {self.status_type}"
        return desc

    def to_dict(self):
        return {
            "type": self.type,
            "urgency": self.urgency,
            "target": self.target,
            "status_type": self.status_type,
            "source": self.source,
        }

    @property
    def tags(self):
        from motivation_presets import get_tags_for_motivation
        return get_tags_for_motivation(self.type)

    @classmethod
    def from_dict(cls, data):
        return cls(
            type=data["type"],
            urgency=data.get("urgency", 5),
            target=data.get("target"),
            status_type=data.get("status_type"),
            source=data.get("source"),
        )

VALID_MOTIVATIONS = {
        "earn_money": 5,
        "eat": 0,
        "sleep": 0,  # Increases with fatigue
        "shelter": 3,
        "have_fun": 2,
        "find_safety": 9,
        f"gain_{StatusLevel.LOW.value}": 4,
        f"gain_{StatusLevel.MID.value}": 5,
        f"gain_{StatusLevel.HIGH.value}": 6,
        f"gain_{StatusLevel.ELITE.value}": 7,
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
        "switch_partner": 2,#hypergamy exists here, see switchPartner(actor, target, currentPartner): Must be a perceived upgrade
        "seek_attention": 2,
        "seek_validation": 2,
        "offer_validation": 4,
        "influence": 4, #influence(actor, target): Change some other characters variables. See Charm() and create_psyop() and influece()
        "increase_popularity": 3, #see charm(actor, target):
        "decrease_hostilities": 4, #see reassureRivals(Boss, rivals): and offerTruce(Boss, rivals): but also offerFauxTruce(Boss, rivals):
        "sow_dissent": 4, #sowDissent(Character, rivals) #weaken a rival or enemy factions loyalities
        "patrol": 3, #patrol(character, region, targetObjects) A key FSM action for low level faction members
        "snitch": 2, #snitch(character, target, location) If a character sees a crime, or feels threatened by faction behaviour
        "explore_math": 8,
        "use_advanced_python_features": 8,
        "stimulate_programmer": 8,
        "charm U7s": 20,
    }
    

class MotivationManager:
    def __init__(self, character):
        self.character = character
        self.motivations = []  # Now a list of Motivation instances

    def update_motivations(self, motivation_type=None, urgency=None, **kwargs):
        """Add or boost a motivation."""
        if motivation_type:
            for m in self.motivations:
                if m.type == motivation_type:
                    m.urgency += urgency or 1
                    return
            # If not found, create new
            new_motivation = Motivation(
                type=motivation_type,
                urgency=urgency or VALID_MOTIVATIONS.get(motivation_type, 5),
                **kwargs
            )
            self.motivations.append(new_motivation)

        # Ensure at least one default
        if not self.motivations:
            self.motivations.append(Motivation("earn_money", 5))

    def get_highest_priority_motivation(self):
        if not self.motivations:
            return Motivation("earn_money", 5)
        return max(self.motivations, key=lambda m: m.urgency)

    def clear_highest_priority_motivation(self):
        """Remove the motivation with the highest urgency."""
        if not self.motivations:
            return None  # Nothing to clear

        top = max(self.motivations, key=lambda m: m.urgency)
        self.motivations.remove(top)
        return top

    def resolve_motivation(self, type_name: str):
        self.motivations = [m for m in self.motivations if m.type != type_name]
        #removes a specific type

    """ def clear_highest_priority_motivation(self):
        for
            max(self.motivations, key=lambda m: m.urgency)

        return  """

    def get_motivations(self):
        return sorted(self.motivations, key=lambda m: m.urgency, reverse=True)

    def get_urgent_motivations(self, threshold=7):
        return [m for m in self.motivations if m.urgency >= threshold]

    def sorted_by_urgency(self, descending=True):
        """Returns motivations sorted by urgency."""
        return sorted(self.motivations, key=lambda m: m.urgency, reverse=descending)

    def has(self, motivation_type):
        return any(m.type == motivation_type for m in self.motivations)

    def reduce_urgency(self, type_name: str, amount=1):
        for m in self.motivations:
            if m.type == type_name:
                m.urgency = max(0, m.urgency - amount)

    def increase(self, motivation_type, amount=1):
        self.update_motivations(motivation_type, urgency=amount)

    def get_urgency(self, motivation_type):
        for m in self.motivations:
            if m.type == motivation_type:
                return m.urgency
        return 0  # or a sensible fallback
    
    

class PoeticMotivation(Motivation):
    metaphor: str
    #You could later generate quests based on poetic triggers