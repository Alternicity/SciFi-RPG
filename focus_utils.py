#focus_utils.py
""" That function should become the only place in the entire codebase that assigns:
npc.mind.attention_focus """
#modeling pre-cognitive attention capture
from base.character import Character
from anchors.anchor_utils import Anchor
from character_thought import Thought

from debug_utils import debug_print

def describe_focus(obj):
    if obj is None:
        return "None"

    # Character
    if isinstance(obj, Character):
        return f"{obj.__class__.__name__}({obj.name})"

    # Anchor
    if isinstance(obj, Anchor):
        return f"Anchor {obj.name}"

    """ # Thought
    if isinstance(obj, Thought):
        if obj.anchor:
            return f"Thought: Anchor {obj.anchor.name}"
        return f"Thought: {obj.content}" """


    # Thought
    if isinstance(obj, Thought):
        label = obj.content

        # truncate long thoughts for readability
        if isinstance(label, str) and len(label) > 40:
            label = label[:37] + "..."

        anchor_flag = " (anchored)" if obj.anchored else ""
        return f"Thought('{label}'){anchor_flag}"


    # Fallback
    return str(obj)


#legacy function
""" def describe_focus(focus):
    if focus is None:
        return "None"

    # Thought-style objects
    subject = getattr(focus, "subject", None)
    content = getattr(focus, "content", None)
    if subject or content:
        return f"Thought({subject})"

    # Anchors
    if hasattr(focus, "type") and hasattr(focus, "name"):
        return f"Anchor({focus.name})"

    # Characters
    if hasattr(focus, "name"):
        return f"{focus.__class__.__name__}({focus.name})"

    # Fallback
    return focus.__class__.__name__ """



def set_attention_focus(npc, anchor=None, thought=None, character=None):
    """
    Unified attention setter.
    Exactly one of (anchor, thought, character) should be non-None.
    """
    old = npc.mind.attention_focus

    new_focus = anchor or thought or character#it could be something else

    if new_focus is not None:
        npc.mind.attention_focus = new_focus
        debug_print(
            npc,
            f"[FOCUS] Attention changed "
            f"from {describe_focus(old)} → {describe_focus(new_focus)}",
            category="focus"
        )
        return






def clear_attention_focus(npc):
    npc.mind.attention_focus = None
    debug_print(npc, "[FOCUS] Cleared", category="focus")