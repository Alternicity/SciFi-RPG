#employment.service_jobs.cafe_restaurant_work.py
from anchors.social_anchors.basic_social_anchors import create_greet_anchor
from create.create_game_state import get_game_state
from focus_utils import set_attention_focus
from social.social_utils import has_recent_interaction
from debug_utils import debug_print
from actions.social_actions.greet import greet_customer_auto
from base.posture import Posture
from employment.WorkSession import WorkSession

class CafeRestaurantWorkSession(WorkSession):
    def __init__(self, employee, workplace):
        super().__init__(employee, workplace)

        self.greeted = set()
        self.served = set()
        self.seated = set()
        self.orders = {}

#Not polymorphism — it’s dispatch by employment profile

def work(waitress):#called from UtilityAI.execute_action
    location = waitress.location
    debug_print(
            waitress,
            f"[WORK LOOP] others={len(location.characters_there)} "
            f"recent={len(location.recent_arrivals)}",
            category="employment"
        )

    session = waitress.work_session
    if not session:
        return

    for other in location.recent_arrivals:

        if other is waitress:
            continue

        if getattr(other, "is_employee", False):
            continue

        if other in session.greeted:
            continue

        if getattr(other, "last_greeted_at", None) == session:
            continue

        greet_customer_auto(waitress, other, session)
        session.greeted.add(other)
        other.last_greeted_at = session

    #do we need to have execute_action register something or some combination of things from here from here to call greet_customer_auto() ?

    def should_greet(session, npc):#not yet used, for when expanding

        if npc in session.greeted:
            return False

        if npc.posture == Posture.SITTING:#Maybe not in later restaurant development
            return False

        return True
    #Use like:
    """ if should_greet(session, other):
        greet_customer_auto(waitress, other)
        session.greeted.add(other) """
