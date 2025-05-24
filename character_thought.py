class Thought:
    def __init__(self, content, origin=None, urgency=1, tags=None, source=None, weight=0):
        self.content = content              # Description of the thought (str or object)
        self.origin = origin                # What caused it (e.g., percept source)
        self.urgency = urgency              # How pressing it is
        self.tags = tags or []              # Useful for filtering (e.g., ["crime", "money"])
        self.source = source                # Who/what told them (e.g., another character)
        self.weight = weight                # How impactful (can be salience or derived)
    
    def __repr__(self):
        return f"<Thought: {self.content} (urgency={self.urgency}, weight={self.weight})>"
