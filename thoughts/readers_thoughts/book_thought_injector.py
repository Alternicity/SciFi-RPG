#thoughts.readers_thoughts.book_thought_injector.py

from thoughts.generic_thought_builders.book_thought_builder import build_book_thoughts
from memory.memory_builders.book_memory_builder import _record_book_memory
from character_thought import Thought
from character_memory import Memory

def inject_book_thought(npc, book):
    thoughts = build_book_thoughts(npc, book)

    # build_book_thoughts returns a flat list (primary + corollaries).
    # mind.thoughts gets every entry flat — the corollary tree in
    # primary.corollary is a back-reference, NOT a second insertion path.
    # Do not also walk .corollary here, or you'll double-insert.

    for t in thoughts:
        npc.mind.add_thought(t)

    _record_book_memory(npc, book)#check the memry is there

    print(
        f"[BOOK THOUGHT] {npc.name} read '{book.title}': "
        f"{len(thoughts)} thought(s) -> {[t.content for t in thoughts]}"
    )
    return thoughts


    #later build a generalised memory_from_thought()