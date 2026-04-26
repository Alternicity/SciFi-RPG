#ai.ai_utility_thought_tools
from character_thought import Thought, FailedThought
from anchors.anchor_utils import Anchor
from anchors.eat_anchor import ProcureFood#but ProcureFood is a class, is that ok?
from typing import Optional
from create.create_game_state import get_game_state
from character_components.npc_effects import RecentMealEffect
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

def generate_leave_location_thought(npc):
    location = npc.location
    if not location:
        return

    t = npc.mind.get_thought_with_tag("leave_location")
    # Boost urgency significantly if purpose is fulfilled
    if npc.location_purpose_fulfilled:
        if t:
            t.urgency = min(10, t.urgency + 3)
        else:
            npc.mind.add_thought(Thought(
                subject=location,
                content=f"I should leave {location.name}.",
                urgency=7,  # high — purpose done
                tags=["leave_location", "movement"]
            ))
        return
    # Original time-based logic as fallback
    if t:
        if npc.time_in_location > 3:
            t.urgency = min(10, t.urgency + 1)
        return

    if npc.current_anchor and npc.current_anchor.name in ["eat", "drink", "work"]:
        # allow override if leaving is urgent
        if npc.time_in_location < 3:
            return

    urgency = 0
    if npc.time_in_location > 2:
        urgency = 4
    else:
        urgency = 1

    thought = Thought(
        subject=location,
        content=f"I should leave {location.name}.",
        urgency=urgency,
        tags=["leave_location", "movement"]
    )

    npc.mind.add_thought(thought)

def reduce_thought_urgency(npc, tag, amount):
    t = npc.mind.get_thought_with_tag(tag)
    if t:
        t.urgency = max(0, t.urgency - amount)

def debug_urgency_state(npc, urgencies, context=""):
    top_mot, mot_urg = urgencies["motivation"]
    top_thought, thought_urg = urgencies["thought"]

    thought_label = npc.mind.get_thought_label(top_thought)

    if mot_urg >= thought_urg:
        winner = f"mot:{getattr(top_mot, 'type', None)}"
    else:
        winner = f"thought:{thought_label}"

    debug_print(
        npc,
        f"[URGENCY{':' + context if context else ''}] "
        f"mot={getattr(top_mot, 'type', None)}:{mot_urg} "
        f"thought={thought_label}:{thought_urg} "
        f"→ winner={winner}",
        category="debug"
    )
    
def get_current_urgencies(npc, exclude_thought=None):
    top_mot = npc.motivation_manager.get_top_motivation()
    top_thought = npc.mind.get_most_urgent_thought()

    mot_urg = top_mot.urgency if top_mot else 0

    # --- Handle exclusion ---
    if top_thought and top_thought == exclude_thought:
        # Find next-best thought instead
        other_thoughts = [
            t for t in npc.mind.thoughts
            if t is not exclude_thought
        ]

        if other_thoughts:
            next_thought = max(other_thoughts, key=lambda t: t.urgency)
            thought_urg = next_thought.urgency
            top_thought = next_thought
        else:
            thought_urg = 0
            top_thought = None
    else:
        thought_urg = top_thought.urgency if top_thought else 0

    return {
        "motivation": (top_mot, mot_urg),
        "thought": (top_thought, thought_urg),
        "excluded": exclude_thought,
        "max": max(mot_urg, thought_urg)
    }

def choose_fun_location(npc):

    best = None
    best_score = -999

    for loc in npc.region.locations:

        score = getattr(loc, "fun_value", 0)

        if "social" in getattr(loc, "tags", []):
            score += npc.fun_prefs.get("social", 0)

        for other in loc.characters_there:

            rel = npc.mind.memory.semantic["social"].get_relation(other)

            if rel.current_type == "friend":
                score += 3

            elif rel.current_type == "enemy":
                score -= 3

        if score > best_score:
            best = loc
            best_score = score

    return best


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
    if npc.has_effect_type(RecentMealEffect):
        return

    # Prevents re-spawning the same hunger narrative every think()
    #existing = npc.mind.get_thought_with_tag("hunger")
    #existing now not accessed

    """ if existing:
        if npc.time_in_location > 3:
            existing.urgency += 1
        return """

    # --- hunger tiering ---
    if npc.hunger > 6:
        choice = "burger"
        #urgency = 8
    else:
        choice = "sandwich"
        #urgency = 6

    if npc.has_effect_type(RecentMealEffect):
        debug_print(
            npc,
            f"[THOUGHT] from generate_hunger_thought() {npc.name} Hunger under RecentMealEffect, no more food",
            category="think"
        )
        return

    if npc.hunger <= 6:   # ← slightly higher threshold helps stability
        return

    npc.mind.reinforce_or_create_thought(
        "hunger",
        amount=1,
        subject=npc,
        content=f"I feel hungry. Maybe a {choice}.",
        tags=["hunger", "food", "eat"],
    )

    #but note we also have here:

    # --- construct thought ---
    #Chat insisting that this should be deleted
    """ thought = Thought(
        subject="food",
        content=f"I'm hungry. I want a {choice}.",
        urgency=urgency,
        tags=["hunger", "food", "eat", choice],
        payload={"desired_food": choice},
    )
    npc.mind.add_thought(thought) """

    """ debug_print(
            npc,
            f"[THOUGHT] from generate_hunger_thought() {npc.name} Hunger={npc.hunger:.2f} Generated: {thought.content}",
            category="think"
        ) """

    #return thought
    return None

def select_food_from_location(npc, location, desired_name=None):
    if not hasattr(location, "items_available"):
        return None

    if desired_name:
        for item in location.items_available:
            if getattr(item, "name", None) == desired_name:
                return item

    # fallback: first available
    debug_print(
            npc,#npc marked as not defined
            f"[THOUGHT] from select_food_from_location fallback choice chosen",
            category="think"
        )

    return location.items_available[0] if location.items_available else None


def procure_food(npc):
    pass
    """Then downstream:
    ChooseFoodVenue
    BuyIngredients
    EatOut """
#The procure layer will be where an npc decides whether to go out to a cafe / restaurant, or buy food from shop to take home, or eat a snack directly from their inventory