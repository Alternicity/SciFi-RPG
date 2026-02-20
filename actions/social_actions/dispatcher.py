#actions.social_actions.dispatcher.py
#future proofing
from actions.social_actions.greet import greet_customer_auto

def execute_social_action(npc, anchor):
    if anchor.name == "greet_customer":#outdated. We dont work this way from anchors, this should check motivation/thought
        greet_customer_auto(npc, anchor.target_object)
        npc.current_anchor = None
    
        return
    #other if branches can go above
    # future:
    # flirt
    # intimidate
    # negotiate