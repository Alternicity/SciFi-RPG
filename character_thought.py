class Thought:
    def __init__(self, content, origin, urgency=1, tags=None):
        self.content = content  # e.g., "Robbery", "Debt", "DateTonight"
        self.origin = origin  # object that triggered the thought
        self.urgency = urgency
        self.tags = tags or []
