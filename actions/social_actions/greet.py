#actions.social_actions.greet.py

from focus_utils import set_attention_focus
from create.create_game_state import get_game_state
from debug_utils import debug_print
from memory.social.social_relation import SocialRelation#added, but not accessed here
from character_thought import Thought

def greet_customer_auto(waitress, target):
    game_state = get_game_state()
    location = waitress.location

    set_attention_focus(waitress, target)
    set_attention_focus(target, waitress)

    social = waitress.mind.memory.semantic.get("social")#gets existing memories tagged social

    #What is record_interaction? A function in SocialRelation
    """ social.record_interaction(
        target,
        hour=game_state.hour,
        day=game_state.day,
        valence=+1,
        kind="greet",
        new_type="customer"
    ) """
    # I am  not sure this is interacting with npc.mind or using SocialRelation correctly

    debug_print(waitress, f"[WAITRESS GREET] Hello ", category = "employment")
    
    free_tables = [
        table for table in location.tables
        if table.has_free_seating(location)
    ]


    if free_tables:
        chosen = free_tables[0]
        debug_print(waitress, f"[HOST] Offering {chosen.name}", category="employment")
        target.mind.thoughts.append(
            Thought(
                content=f"I should sit at {chosen.name}",
                tags=["sit", "dine_in"],
                payload={"table": chosen}
            )
        )




    #if known to the waitress she could add targets name with {target.name} after the Hello?
    #debug_print(waitress, f"[WAITRESS GREET] {waitress.name} greets {target.name}", category="employment")
