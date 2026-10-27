#create.create_ObjectInWorld.create_book.py
from world.books import Book
from world.books_catalogue import LIBRARY_COLLECTION

def random_book():
    pass

def spawn_book(template):
    return Book(
        title=template.title,
        author=template.author,
        subject_tags=list(template.subject_tags),
        knowledge_type=template.knowledge_type,
        is_redacted=template.is_redacted,
        psy_resonance=template.psy_resonance,
        reading_difficulty=template.reading_difficulty,
        colour=template.colour,
    )
