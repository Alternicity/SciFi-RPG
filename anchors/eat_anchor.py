#anchors.eat_anchor.py
from anchors.anchor import Anchor
from memory.memory_builders.memory_utils import best_food_location
from create.create_game_state import get_game_state
from worldQueries import location_sells_food
from debug_utils import debug_print
import random
#dont import set_attention_focus

from objects.furniture import CafeChair, CafeTable

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
    #we need to get a reference to the owner of the anchor here and set it to npc
    #then we can set location to npc.location

    #one anchor, many targets
    type = "eat"
    name = "eat"

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
        npc = self.owner
        location = npc.location

        from focus_utils import set_attention_focus
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

        free_chairs = [
            obj for obj in location.items.objects_present#location not defined here
            if isinstance(obj, CafeChair) and obj.is_free()
        ]

        if free_chairs:
            chair = random.choice(free_chairs)
            if chair.occupy(npc):#npc not defined here
                npc.current_chair = chair
                set_attention_focus(npc, character=None)  # optional reset

        # 2. Fallback: take first available item
        # I had to move this to after the free_chairs block
        return items_available[0]

    
    #del
    # Legacy compatibility
"""     def resolve_action(self):
        return self.propose_action() """
