#focus_utils.py
""" That function should become the only place in the entire codebase that assigns:
npc.mind.attention_focus """
#modeling pre-cognitive attention capture

from debug_utils import debug_print

def describe_focus(focus):
    #Formatting logic should not live inside control branches
    if focus is None:
        return "None"

    subject = getattr(focus, "subject", None)
    content = getattr(focus, "content", None)

    if subject or content:
        return f"{subject}: '{content}'"

    # Fallback for non-Thought focus (Character, Anchor, etc.)
    name = getattr(focus, "name", focus.__class__.__name__)
    return str(name)


def set_attention_focus(npc, anchor=None, thought=None, character=None):
    """
    Unified attention setter.
    Exactly one of (anchor, thought, character) should be non-None.
    """
    old = npc.mind.attention_focus

    if thought is not None:
        npc.mind.attention_focus = thought
        debug_print(
            npc,
            f"[FOCUS] Attention changed "
            f"from {describe_focus(old)} → {describe_focus(thought)}",
            category="focus"
        )
        return

    if character is not None:
        npc.mind.attention_focus = character
        debug_print(
            npc,
            f"[FOCUS] Attention changed "
            f"from {describe_focus(old)} → {describe_focus(character)}",
            category="focus"
        )
        return

    if anchor is not None:
        npc.mind.attention_focus = anchor
        debug_print(
            npc,
            f"[FOCUS] Attention changed "
            f"from {describe_focus(old)} → {describe_focus(anchor)}",
            category="focus"
        )
        return

    # Clear focus
    npc.mind.attention_focus = None
    debug_print(
        npc,
        f"[FOCUS] Attention cleared (was {describe_focus(old)})",
        category="focus"
    )




def clear_attention_focus(npc):
    npc.mind.attention_focus = None
    debug_print(npc, "[FOCUS] Cleared", category="focus")