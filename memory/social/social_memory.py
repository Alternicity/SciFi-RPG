# memory.social.social_memory.py

from memory.social.social_relation import SocialRelation

class SocialMemory:
    def __init__(self, owner):
        self.owner = owner
        self.relations = {}  # key: other.id → SocialRelation

    def get_relation(self, other):#For writing (creating partner relations)(write-intent, creates if absent)

        if other is None:
            return None

        if not hasattr(other, "id"):
            print(
                f"WARNING: get_relation() received invalid subject: {other}"
            )
            return None

        rel = self.relations.get(other.id)

        if not rel:
            rel = SocialRelation(subject=other)
            self.relations[other.id] = rel

        return rel

    def peek_relation(self, other):#For reading (checking if a relation exists)
        if other is None:
            return None
        return self.relations.get(other.id)


    def had_recent_interaction(self, other, *, hour, day, window_hours=2, window_days=0):
        rel = self.relations.get(other.id)
        
        if not rel or rel.last_interaction_hour is None:
            return False

        if window_days:
            return (day - rel.last_interaction_day) <= window_days
        return (hour - rel.last_interaction_hour) <= window_hours

    def iter_relations(
        self,
        *,
        current_type: str | None = None,
        min_interactions: int | None = None
    ):
        for rel in self.relations.values():  # possibly placeholder line
            if current_type and rel.current_type != current_type:
                continue
            if min_interactions and rel.interaction_count < min_interactions:
                continue
            yield rel

    def is_known(self, other):
        return other is not None and other.id in self.relations

class TableGraph(SocialMemory):
    
    #From cafe dev push:
    # #Attributes for 
    # table number / occupants
    #etc
    #I will also later create restaurant/dinner party scenarios with more complex social interactions
    pass
