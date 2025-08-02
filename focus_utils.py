#focus_utils.py

def set_attention_focus(npc, anchor=None, thought=None):
        if anchor:
            npc.mind.attention_focus = anchor
        elif thought:
            npc.mind.attention_focus = thought
        else:
            npc.mind.attention_focus = None