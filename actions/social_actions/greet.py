#actions.social_actions.greet.py

from focus_utils import set_attention_focus
from create.create_game_state import get_game_state
from debug_utils import debug_print
from memory.social.social_relation import SocialRelation#added, but not accessed here
from character_thought import Thought

from base.posture import Posture

def greet_customer_auto(waitress, target, session):
    game_state = get_game_state()
    location = waitress.location

    set_attention_focus(waitress, target)
    set_attention_focus(target, waitress)

    social = waitress.mind.memory.semantic.get("social")
    relation = social.get_relation(target)

    relation.record_interaction(
        hour=game_state.hour,
        day=game_state.day,
        valence=+1,
        new_type="customer"
    )

    target.last_greeted_at = session

    #greet is ok to happen upon customer (here: target) arrives

    debug_print(waitress, f"[WAITRESS GREET] Hello ", category = "employment")
    
    free_tables = [
        table for table in location.tables
        if table.has_free_seating(location)
    ]

    if target.posture == Posture.SITTING:#we could also add a recent_arrivals filter
        return

    if free_tables: #and not target.mind.has_thought_with_tag("sit"): line 43
        chosen = free_tables[0]
        debug_print(waitress, f"[HOST] Offering {chosen.name}", category="employment")#this print was not showing in output, so I commented part of line 43
        if not target.mind.has_thought_with_tag("sit"):
            target.mind.thoughts.append(
                Thought(#this gets added
                    subject=target,
                    content=f"I should sit at {chosen.name}",
                    tags=["sit", "dine_in"],
                    payload={"table": chosen},
                    urgency=6
                )
            )
            debug_print(target, f"[DEBUG] Added SIT thought → {chosen.name}", category="employment")
            #this print is not showing in output


    #if known to the waitress she could add targets name with {target.name} after the Hello?
    #debug_print(waitress, f"[WAITRESS GREET] {waitress.name} greets {target.name}", category="employment")
