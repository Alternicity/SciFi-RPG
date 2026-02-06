#anchors.eat_anchor.py
from anchors.anchor import Anchor
from memory.memory_builders.memory_utils import best_food_location
from create.create_game_state import get_game_state
from worldQueries import location_sells_food
from debug_utils import debug_print
game_state = get_game_state()

class ChooseFood(Anchor):
    #cafe/restaurant version
    """ hunger = npc.hunger
    venue = npc.location
        for each option in 
            venue.items_available[]
            compute_salience 
            return choice"""
    def compute_salience_for(self, percept, npc):
        return npc.hunger * 0.5
    
    

class ProcureFood(Anchor):#needs to be set up tick 1 for civ liberty

    def compute_salience_for(self, percept, npc):
        CHEAP_MEAL_COST = game_state.CHEAP_MEAL_COST
        hunger = npc.hunger
        funds = npc.wallet.balance

        score = hunger * 0.8

        if funds < CHEAP_MEAL_COST:
            score *= 0.6

        if npc.motivations.get("social", 0) > 0.5:
            score += 0.2

        return score


class EatAnchor(Anchor):
    #one anch, many targets
    type = "eat"

    def resolve_target_location(self):
        npc = self.owner
        return best_food_location(npc)#this currently works

    def can_execute_here(self):
        """Is eating possible at the current location?"""
        npc = self.owner
        return location_sells_food(npc.location)

        """ Current status:
        can_execute_here() is redundant
        resolve_action() is legacy glue
        Do not delete yet.
        Just stop depending on them. """

    def _select_best_item(self, items_available, desired_name):
        """
        Try to match desired food to what's available.
        Very thin adapter between desire and environment.
        """
        if not items_available:
            return None

        # 1. Exact match by name (or id)
        if desired_name:
            for item in items_available:
                if getattr(item, "name", None) == desired_name:
                    return item

            debug_print(
                self.owner,
                f"[EAT] Desired food '{desired_name}' not available here",
                category="think"
            )

        # 2. Fallback: take first available item
        # (Later this can be preference-weighted)
        return items_available[0]

    def propose_action(self):
        npc = self.owner
        cafe = npc.location

        if not hasattr(cafe, "items_available"):
            return None

        thought = npc.mind.get_thought_with_tag("hunger")
        desired = thought.payload.get("desired_food") if thought else None

        item = self._select_best_item(cafe.items_available, desired)
        if not item:
            return None

        return {#this type of logic block normally belongs in UtilityAi.choose_action() It got in here temporarily in the last dev push to get basic fodd buying working
            "name": "buy",
            "params": {
                "item": item
            }
        }

    # Legacy compatibility
    def resolve_action(self):
        return self.propose_action()
