#actions.social_actions.greet.py

from focus_utils import set_attention_focus
from create.create_game_state import get_game_state


def greet_customer_auto(waitress, target):
    game_state = get_game_state()

    set_attention_focus(waitress, target)
    set_attention_focus(target, waitress)

    social = waitress.mind.memory.semantic.get("social")
    social.record_interaction(
        target,
        hour=game_state.hour,
        day=game_state.day,
        valence=+1,
        kind="greet",
        new_type="customer"
    )

