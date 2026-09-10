#GUI.viewmodels.character_display.py
from display.display import build_info_column
from GUI.helpers.formatting import is_highlighted_percept

#Not really a generic GUI helper. It takes semantic percept data and turns it into display-ready character data.

def get_character_display_data(percept, observer):# Semantic percept → character display data.
    #is the semantic → display-row transformation.
    data = percept["data"]
    origin = percept["origin"]
    name = data.get("name", "Unknown")
    posture = data.get("posture")
    seated_at = data.get("seated_at")
    traits = data.get("observable_traits", [])

    if posture is not None:
        posture_text = posture.name.title()
    else:
        posture_text = "Unknown"

    if seated_at is not None:
        description = f"{posture_text} on {seated_at.name}"
    else:
        description = posture_text

    if traits:
        description += ", " + ", ".join(traits)

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