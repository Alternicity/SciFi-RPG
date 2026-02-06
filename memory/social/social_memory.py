# memory.social.social_memory.py
from base.character import Character
from dataclasses import dataclass, field

from memory.social.social_relation import SocialRelation

class SocialMemory:
    def __init__(self, owner):
        self.owner = owner
        self.relations = {}  # key: other.id → SocialRelation

    def get_relation(self, other):
        rel = self.relations.get(other.id)
        if not rel:
            rel = SocialRelation(subject=other)
            self.relations[other.id] = rel
        return rel

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
        for rel in self.relations.values():  # however you're storing them
            if current_type and rel.current_type != current_type:
                continue
            if min_interactions and rel.interaction_count < min_interactions:
                continue
            yield rel

    def is_known(npc, other):
        social = npc.mind.memory.semantic.get("social")
        return social and social.has_relation_with(other)


