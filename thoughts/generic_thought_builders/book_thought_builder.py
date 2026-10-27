#thoughts.generic_thought_builders.book_thought_builder.py

from character_thought import Thought
from thoughts.generic_thought_builders.book_thought_templates import TEMPLATES, COROLLARY_TEMPLATES


FALLBACK_CONTENT = "{title} has given me something to think about."

COROLLARY_BASE_INTELLIGENCE = 10
COROLLARY_STEP = 2


# --- helpers

#new, basic, placeholder system
def merge_tags(*sources):
    """De-dupe tags preserving first-seen order."""
    seen = set()
    out = []
    for src in sources:
        if not src:
            continue
        for tag in src:
            if tag not in seen:
                seen.add(tag)
                out.append(tag)
    return out


def _primary_template_candidates(book):
    """Templates registered for any of the book's subject_tags, highest priority first.

    Used ONLY for primary-thought selection. Corollaries are intel-gated and
    come from COROLLARY_TEMPLATES, not from this pool.
    """
    return sorted(
        (TEMPLATES[t] for t in book.subject_tags if t in TEMPLATES),
        key=lambda tpl: tpl.priority,
        reverse=True,
    )


def _make_thought(npc, book, template):
    tags = merge_tags(
        ["book", "readable"],
        book.subject_tags,
        template.extra_tags,
    )
    return Thought(
        subject="book",
        content=template.content(npc, book),
        origin="book",
        source=book.author,
        predicate="read_book",
        urgency=template.urgency(npc, book),
        tags=tags,
        payload={
            "book_title": book.title,
            "book_author": book.author,
            "knowledge_type": book.knowledge_type,
            "psy_resonance": book.psy_resonance,
            "reading_difficulty": book.reading_difficulty,
        },
    )


###


def _pick_template(book):
    """Return the highest-priority template matching any of the book's tags."""
    matches = [TEMPLATES[t] for t in book.subject_tags if t in TEMPLATES]
    if not matches:
        return None
    return max(matches, key=lambda tpl: tpl.priority)

def build_book_thought(npc, book) -> Thought:
    """The primary thought for reading this book."""
    matches = _primary_template_candidates(book)
    if matches:
        return _make_thought(npc, book, matches[0])

    # Fallback
    return Thought(
        subject="book",
        content=FALLBACK_CONTENT.format(title=book.title),
        origin="book",
        source=book.author,
        predicate="read_book",
        urgency=10,
        tags=["book", "readable", *book.subject_tags],
        payload={"book_title": book.title, "book_author": book.author},
    )



def _corollary_count(intel: int) -> int:
    """Intel-gated corollary slots. intel < 10 -> 0.
    intel 10 -> 1, 11 -> 1, 12 -> 2, 13 -> 2, 14 -> 3, 15 -> 3 ...
    """
    if intel < 10:
        return 0
    return (intel - 10) // 2 + 1

def _build_corollary(npc, book, primary, i):
    """Depth-i corollary. Generic template, not tag-matched to book.

    Depth i selects which COROLLARY_TEMPLATES entry fires. Intel (via
    _corollary_count) decides how many depths are reached.
    """
    if i >= len(COROLLARY_TEMPLATES):
        return None

    tmpl = COROLLARY_TEMPLATES[i]
    tags = merge_tags(
        primary.tags,
        tmpl["extra_tags"],
    )
    return Thought(
        subject="book",
        content=tmpl["content"](npc, book),
        origin="book_corollary",
        source=book.author,
        predicate="read_book",
        urgency=tmpl["urgency"](npc, book),
        tags=tags,
        corollary_of=primary,#maybe thought.corollary_of is being set
        payload={
            "book_title": book.title,
            "book_author": book.author,
            "corollary_depth": i,
        },
    )

# --- public builders

def build_book_thought(npc, book) -> Thought:
    """The primary thought for reading this book. Tag-matched, highest priority."""
    matches = _primary_template_candidates(book)
    if matches:
        return _make_thought(npc, book, matches[0])

    # Fallback: no template matched any subject_tag
    tags = merge_tags(["book", "readable"], book.subject_tags)
    return Thought(
        subject="book",
        content=FALLBACK_CONTENT.format(title=book.title),
        origin="book",
        source=book.author,
        predicate="read_book",
        urgency=10,
        tags=tags,
        payload={"book_title": book.title, "book_author": book.author},
    )


def build_book_thoughts(npc, book) -> list[Thought]:#line 172
    """Primary thought plus any corollaries the NPC is smart enough for.
        
    Contract: returns a FLAT list — [primary, cor0, cor1, ...].
    Also links corollaries into primary.corollary for tree walks.
    Callers should iterate the returned list for "all thoughts from this read";
    use .corollary when you need parent-child structure (e.g. luminous resonance).
    """
    primary = build_book_thought(npc, book)
    out = [primary]
    n = _corollary_count(npc.intelligence)
    for i in range(n):
        c = _build_corollary(npc, book, primary, i)
        if c is not None:
            out.append(c)
            primary.corollary.append(c)
    return out











""" 
def build_book_thought(npc, book):

    if "history" in book.subject_tags:
        content = (
            f"{book.title} makes me wonder whether "
            "the accepted history of the colony is complete."
        )

    elif "precursor" in book.subject_tags:
        content = (
            f"{book.title} makes me wonder what happened "
            "to the people who came before us."
        )

    else:
        content = (
            f"{book.title} has given me something to think about."
        )

    return Thought(
        subject=npc.name,#ATTN
        content=content,
        urgency=20,
        tags=list(book.subject_tags),
        source="book"
    ) """
    