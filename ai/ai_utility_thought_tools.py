#ai.ai_utility_thought_tools
from character_thought import Thought, FailedThought
from anchors.anchor_utils import Anchor
from anchors.eat_anchor import ProcureFood#but ProcureFood is a class, is that ok?
from typing import Optional
from create.create_game_state import get_game_state
game_state = get_game_state
from debug_utils import debug_print

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

#utility functions
def extract_anchor_from_action(action: dict) -> Optional[Anchor]:#line 108
        if "anchor" in action:
            return action["anchor"]
        elif "motivation" in action:
            return Anchor(name=action["motivation"], type="motivation", weight=1.0)
        #set the anchor in npc attribute
        return None

def rank_memory_locations_by_salience(npc, anchor, tag_filter=None, top_n=3):
    """
    Returns top_n locations from memory most salient to the current anchor.
    """
    relevant_memories = npc.mind.memory.query_memory_by_tags(tag_filter or ["location"])
    ranked = []

    for mem in relevant_memories:
        loc = mem.source
        if not loc:
            continue
        salience = compute_salience(loc, npc, anchor)#compute_salience is here marked as not defined
        ranked.append((loc, salience, mem))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:top_n]

def generate_hunger_thought(npc):
    """
    Generate a subjective hunger thought based on internal hunger level.
    This does NOT trigger actions or anchors — it only represents experience.
    """

    # --- threshold gate ---
    if npc.hunger <= 4:
        return None

    # --- deduplication guard ---
    # Prevents re-spawning the same hunger narrative every think()
    if npc.mind.has_thought_with_tag("hunger"):
        return None

    # --- hunger tiering ---
    if npc.hunger > 7:
        choice = "burger"
        urgency = 8
    else:
        choice = "sandwich"
        urgency = 6

    # --- construct subjective thought ---
    thought = Thought(
        subject="food",
        content=f"I'm hungry. I want a {choice}.",
        urgency=urgency,
        tags=["hunger", "food", choice],
        payload={"desired_food": choice},
    )

    # --- register with mind ---
    npc.mind.add_thought(thought)

    debug_print(
        npc,
        f"[THOUGHT] Generated hunger thought: {thought.content}",
        category="think"
    )

    return thought

def procure_food(npc):
    npc.anchors.add(ProcureFood(
        name="procure_food",
        type="motivation",
        owner=npc,
        priority=1.5
    ))
    """Then downstream:
    ChooseFoodVenue
    BuyIngredients
    EatOut """
#The procure layer will be where an npc decides whether to go out to a cafe / restaurant, or buy food from shop to take home, or eat a snack directly from their inventory