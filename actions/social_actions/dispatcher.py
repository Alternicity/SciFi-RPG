#actions.social_actions.dispatcher.py

from actions.social_actions.greet import greet_customer_auto

def execute_social_action(npc, anchor):
    if anchor.name == "greet_customer":
        greet_customer_auto(npc, anchor.target_object)
        npc.current_anchor = None
        return

    # future:
    # flirt
    # intimidate
    # negotiate