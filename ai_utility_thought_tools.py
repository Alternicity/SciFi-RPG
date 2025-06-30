#ai_utility_thought_tools
from character_thought import Thought, FailedThought
from salience import Anchor
from typing import Optional

class UtilityAIThoughtTools():

    def emotion_corollary(self, thought):
            if "sad" in thought.content.lower():
                return Thought("Maybe crying is like releasing static.", tags=["emotion", "corollary"])
            
    def retroduct(self):
        failed = [t for t in self.npc.mind.thoughts if isinstance(t, FailedThought)]
        if failed:
            print(f"[RETRODUCT] {self.npc.name} reviewing failed ideas...")
            # Process or compare to generate new strategy

    def get_corollaries_by_tag(self, tag):
        return [c for c in self.corollaries if tag in c.tags]
    

class DoubtMixin:
    def evaluate(self, threshold=0.3):
        return self.confidence < threshold
    """ Attach this to Thoughts, Memories, Dreams, Beliefs
    A doubt in one corollary led her to refine the pattern
    and birth a stronger Thought. """

def extract_anchor_from_action(action: dict) -> Optional[Anchor]:#line 108
        if "anchor" in action:
            return action["anchor"]
        elif "motivation" in action:
            return Anchor(name=action["motivation"], type="motivation", weight=1.0)
        return None