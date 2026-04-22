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

    is_sitting = target.posture == Posture.SITTING

    if not is_sitting:
        if not free_tables:
            debug_print(waitress, "[HOST] No free tables", category="employment")
            return

        # ✅ NEW: skip greet if already seated AND already has sit/served thoughts
        already_handled = (
            target.posture == Posture.SITTING
            and target.mind.has_thought_with_tag("sit")
            and target.mind.has_thought_with_tag("served")
        )
        if already_handled:
            return

        debug_print(waitress, f"[HOST] Offering table", category="employment")

        chosen = None  # ← initialize before conditional block

        tables = [f for f in waitress.location.furniture if isinstance(f, CafeTable)]
        for table in tables:
            if table.has_free_seating(waitress.location):
                chosen = table
                break

        if chosen is None:
            debug_print(waitress, "[HOST] No free table found", category="employment")
            return  # ← exit cleanly, no crash

        debug_print(target, f"[DEBUG] Added SIT thought → {chosen.name}", category="employment")

        target.mind.add_thought(Thought(
            subject="sit",
            content=f"I should sit at {chosen.name}",
            origin="greet_customer_auto",
            urgency=7,
            tags=["sit", "dine_in"],
            payload={"table": chosen}
        ))

        # Temporary: inject "served" here to unblock pipeline (Issue 2)
        if not target.mind.has_thought_with_tag("served"):
            target.mind.add_thought(Thought(
                subject="served",
                content="I have been served.",
                origin="greet_customer_auto",
                urgency=3,
                tags=["served"],
            ))
            debug_print(target, f"[DEBUG] Added SERVED thought", category="employment")

    #if known to the waitress she could add targets name with {target.name} after the Hello?
    #debug_print(waitress, f"[WAITRESS GREET] {waitress.name} greets {target.name}", category="employment")
