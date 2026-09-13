# GUI.viewmodels.book_display.py

from display.display import build_info_column
from GUI.helpers.formatting import is_highlighted_percept

#for now, build_info_column() will simply return "—" for a Book, because it has no Book-specific branch.
def get_book_display_data(percept, observer):

    data = percept["data"]
    origin = percept["origin"]

    title = data.get("title") or data.get("name", "Unknown Book")
    colour = data.get("colour")

    if colour:
        name = f"{colour.title()} Book"
    else:
        name = "Book"

    description = title

    info = build_info_column(
        origin,
        observer,
        data,
        getattr(observer, "current_anchor", None)
    )

    highlight = is_highlighted_percept(
        origin,
        observer
    )

    return name, description, info, highlight