#memory.social.social_relation.py
from base.character import Character
from dataclasses import dataclass, field

@dataclass
class SocialRelation:
    subject: "Character"  # who this relation is about

    # Interaction history
    interaction_count: int = 0
    positive_count: int = 0
    negative_count: int = 0

    # Temporal
    last_interaction_hour: int | None = None
    last_interaction_day: int | None = None

    # Classification
    current_type: str = "acquaintance"#coworker
    past_types: list[str] = field(default_factory=list)

    # Affective scalars
    envy: int = 0
    pity: int = 0
    trust: int = 0
    fear: int = 0
    #Valence = positive vs negative emotional impact
    
    # Network awareness (lightweight, optional)
    mutual_friends: list["Character"] = field(default_factory=list)
    mutual_enemies: list["Character"] = field(default_factory=list)

    def record_interaction(self, *, hour, day, valence=0, new_type=None):
        self.interaction_count += 1
        self.last_interaction_hour = hour
        self.last_interaction_day = day

        if valence > 0:
            self.positive_count += 1
        elif valence < 0:
            self.negative_count += 1

        if new_type and new_type != self.current_type:
            self.past_types.append(self.current_type)
            self.current_type = new_type

    @property
    def is_partner(self) -> bool:
        return self.current_type == "partner"        