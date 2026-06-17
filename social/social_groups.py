#social.social_groups.py

class SocialGroup:

    def __init__(self):
        self.members = []

    def contains(self, npc):
        return npc in self.members