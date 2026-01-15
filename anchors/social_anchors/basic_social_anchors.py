#anchors.social_anchors.basic_social_anchors.py
from anchors.anchor_utils import Anchor

def create_greet_anchor(npc, target):
    npc.anchors.add(Anchor(
        name="greet_customer",#I think customer should be replaced with a more general target
        type="work",
        owner=npc,
        target_object=target,
        desired_tags=["person"],
        priority=1.2,
        tags=["social", "service"]
    ))
    #This function would be used also, for example, by a hostess at a dinner party.