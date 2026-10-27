#thoughts.generic_thought_builders.book_thought_templates.py

from dataclasses import dataclass
from typing import Callable, Optional
#Adding a new book topic = one register(...) call. No edits to the builder.

@dataclass(frozen=True)
class BookThoughtTemplate:
    tag: str
    priority: int                     # higher wins on collision
    content: Callable[[object, object], str]   # (npc, book) -> str
    urgency: Callable[[object, object], int] = lambda npc, book: 20
    extra_tags: tuple = ()


TEMPLATES: dict[str, BookThoughtTemplate] = {}


def register(template: BookThoughtTemplate) -> None:
    TEMPLATES[template.tag] = template

#book.subject_tags describe the book; template.extra_tags describe the NPC's reaction to it.
#psy, forbidden, mystery, archaeology — those are book properties. unease, fear, doubt — those are reactions. Keep them in their lanes.


# History 
register(BookThoughtTemplate(
    tag="history",
    priority=10,
    content=lambda npc, book: (
        f"{book.title} makes me wonder whether the accepted history "
        f"of the colony is complete."
        + (" Some pages are missing." if book.is_redacted else "")
    ),
    urgency=lambda npc, book: 25 if book.is_redacted else 15,
    extra_tags=("doubt",),
))

# Precursor
register(BookThoughtTemplate(
    tag="precursor",
    priority=20,   # beats "history" if both present
    content=lambda npc, book: (
        f"{book.title} makes me wonder what happened to the people "
        f"who came before us."
    ),
    urgency=lambda npc, book: 20 + int(10 * book.psy_resonance),
))

# --- Psy / -------------------------------------------------------
register(BookThoughtTemplate(
    tag="psy",
    priority=30,
    content=lambda npc, book: (
        f"{book.title} resonates in a way I can't quite name."
    ),
    urgency=lambda npc, book: 30 + int(10 * book.psy_resonance),
    extra_tags=("psy", "unease"),
))


#forbidden 
register(BookThoughtTemplate(
    tag="forbidden",
    priority=35,
    content=lambda npc, book: (
        f"{book.title} I had no idea about this!"
    ),
    urgency=lambda npc, book: 18 + int(10 * book.psy_resonance),
    extra_tags=("fear"),
))

#mystery
register(BookThoughtTemplate(
    tag="mystery",
    priority=15,
        content=lambda npc, book: (
            f"{book.title} is fascinating I wonder what the truth is."
        ),
        urgency=lambda npc, book: 18 + int(10 * book.psy_resonance),#perhaps instead of book.psy_resonance we could use npc.curiosity?
        #and, of course, update necessary code to handle this
        extra_tags=("supposed", "mystery"),
))

# --- Civic / practical -----------------------------------------------------
register(BookThoughtTemplate(
    tag="civic",
    priority=25,
    content=lambda npc, book: (
        f"{book.title} is a useful reminder of how the colony runs."
    ),
    urgency=lambda npc, book: 5,
))

""" Sketch, for later:

    "Luminous thought" via shared tag: in inject_book_thought, before adding the primary, check npc.mind.thoughts for any existing thought sharing a tag with the book's subject_tags. If found, either raise primary.urgency or emit an extra corollary with a special template like "resonant".

    Region cross-fertilisation: if a book has a tag matching a region name (e.g. "eastern_reaches"), and the NPC has a RegionKnowledge for it, merge: the thought can reference known facts. That's a RegionKnowledge-aware template that receives npc (which is why the template callables take npc).
 """


#The simplified system
 # --- Corollary depth registry -------------------------------------------------
# One template per depth i. Generic, not book-specific. Intel decides how many
# slots fire; depth i selects *which* template fires. Content(npc, book) can
# still peek at the book for flavour, but must not assume tag matches.
#
# Each entry: (content, urgency, extra_tags)
#   content(npc, book) -> str
#   urgency(npc, book) -> int
#   extra_tags: list[str]

def _corr0_content(npc, book):#basic placeholder system
    return f"This makes me think of something else."

def _corr0_urgency(npc, book):
    return 2

def _corr1_content(npc, book):
    return f"And also, there's a further connection."

def _corr1_urgency(npc, book):
    return 3

def _corr2_content(npc, book):
    return f"A third thread pulls loose."

def _corr2_urgency(npc, book):
    return 4

COROLLARY_TEMPLATES = [
    # depth 0
    {
        "content": _corr0_content,
        "urgency": _corr0_urgency,
        "extra_tags": ["corollary", "depth0"],
    },
    # depth 1
    {
        "content": _corr1_content,
        "urgency": _corr1_urgency,
        "extra_tags": ["corollary", "depth1"],
    },
    # depth 2
    {
        "content": _corr2_content,
        "urgency": _corr2_urgency,
        "extra_tags": ["corollary", "depth2"],
    },
]