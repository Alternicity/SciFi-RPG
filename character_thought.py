class Thought:
    def __init__(self, content, origin, urgency=1, tags=None, source=None, weight=0):
        self.content = content  # e.g., "Robbery", "Debt", "DateTonight"
        self.origin = origin  # object that triggered the thought
        self.urgency = urgency
        self.tags = tags or []
        self.source = None
        self.weight = 0