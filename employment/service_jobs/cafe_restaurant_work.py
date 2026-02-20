#employment.service_jobs.cafe_restaurant_work.py
from anchors.social_anchors.basic_social_anchors import create_greet_anchor
from create.create_game_state import get_game_state
from focus_utils import set_attention_focus
from social.social_utils import has_recent_interaction
from debug_utils import debug_print
from actions.social_actions.greet import greet_customer_auto

#Not polymorphism — it’s dispatch by employment profile

def work(waitress):#called from UtilityAI.execute_action
    location = waitress.location
    debug_print(
            waitress,
            f"[WORK LOOP] others={len(location.characters_there)} "
            f"recent={len(location.recent_arrivals)}",
            category="employment"
        )

    for other in location.characters_there:
        if other is waitress:
            continue
        if getattr(other, "is_employee", False):
            continue


        create_greet_anchor(waitress, other)
        greet_customer_auto(waitress, other)

    #do we need to have execute_action register something or some combination of things from here from here to call greet_customer_auto() ?



