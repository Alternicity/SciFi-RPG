#anchors.social_anchors.basic_social_anchors.py
from anchors.anchor_utils import Anchor
from debug_utils import debug_print

def create_greet_anchor(npc, target):#npc, not waitress
    waitress = npc

    waitress.mind.attention_focus = target
    debug_print(
        waitress,
        f"[FOCUS] FROM create_greet_anchor: attention → customer {target.name}",
        category="focus"
    )

    anchor = Anchor(
        name="greet_person",   # 👍 generalized
        type="work",
        owner=npc,
        target_object=target,
        desired_tags=["person"],
        priority=1.2,
        tags=["social", "service", "greeting"]
    )
    if anchor not in npc.anchors:
        npc.anchors.append(anchor)

    npc.current_anchor = anchor
    #This function would be used also, for example, by a hostess at a dinner party.