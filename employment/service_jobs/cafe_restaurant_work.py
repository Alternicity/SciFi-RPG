#employment.service_jobs.cafe_restaurant_work.py
from anchors.social_anchors.basic_social_anchors import create_greet_anchor
from create.create_game_state import get_game_state
from focus_utils import set_attention_focus
from social.social_utils import has_recent_interaction
from debug_utils import debug_print
#Not polymorphism — it’s dispatch by employment profile

def work(waitress):#called from UtilityAI.execute_action
    location = waitress.location
    debug_print(
            waitress,
            f"[WORK LOOP] others={len(location.characters_there)} "
            f"recent={len(location.recent_arrivals)}",
            category="employment"
        )


    for other in location.characters_there:#where is other coming from?
        if other is waitress:
            continue

        if other in location.recent_arrivals:
            if has_recent_interaction(waitress, other):
                continue

            create_greet_anchor(waitress, other)



