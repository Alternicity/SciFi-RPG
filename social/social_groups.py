#social.social_groups.py
from dataclasses import field
from base.character import Character

class SocialGroup:

    day_created = 1
    hour_created = 1
    conversation = None#current topic will likely be in here

    members: list[Character] = field(default_factory=list)

    location = None
    sublocation = None

    conversation = None

    purpose = None
    label = None
    leader = None

    created_tick = 0

    observers = []

    notes = []

    location = None#should these be set in init? npc.location etc
    sublocation = None

    def __init__(self):
        self.label = "Conversation"
        self.members = []

    def __str__(self):
        return self.label or "Social Group"

    def contains(self, npc):
        return npc in self.members

        #we have elsewhere made use of 
        #observer.mind.memory.semantic.get("social")

        #and
        #social.get_relation(target)

        #and
        #relation.current_type
        #though this doesnt exist except in one gui call

    @property
    def size(self):
        return len(self.members)

    @property
    def pair(self):
        return self.size == 2

    @property
    def leader_name(self):
        return self.leader.name if self.leader else "None"

    @property
    def member_names(self):
        return [m.name for m in self.members]