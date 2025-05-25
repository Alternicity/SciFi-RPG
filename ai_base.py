class BaseAI:
    def __init__(self, npc):
        self.npc = npc

    def choose_action(self, region):
        raise NotImplementedError("AI must implement choose_action")

    def execute_action(self, action, region):
        raise NotImplementedError("AI must implement execute_action")
