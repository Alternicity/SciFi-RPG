#memory.memory_builders.book_memory_builder.py

def _record_book_memory(npc, book):
    """Tick-0 book-specific memory writer.
    Later: generalize into generic_thought_builders/memory_from_thought.py."""
    from memory.memory_entry import KnowledgeMemory

    reading_record = KnowledgeMemory(
        subject="book",
        verb="read",
        object_=book.title,
        source_title=book.title,
        knowledge_type=book.knowledge_type,
        subject_tags=list(book.subject_tags),
        psy_resonance_experienced=book.psy_resonance,
        tags=["book_knowledge", *book.subject_tags],
        owner=npc.name,
    )
    npc.mind.memory.semantic.setdefault("book_knowledge", []).append(reading_record)