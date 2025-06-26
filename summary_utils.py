#summary_utils.py
from tabulate import tabulate
import textwrap

def summarize_motivations_and_percepts(character) -> str:
    """
    Returns a readable summary of a character's percepts using tabulate.
    Includes a summary table and a percept-type salience breakdown.
    """

    if not hasattr(character, 'motivation_manager'):
        raise TypeError(f"summarize_percepts expected a Character, got {type(character)}: {character}")
    

    output = "\n=== Motivations ===\n"

    summary_rows = []

    # Top two motivations
    top_motives = character.motivation_manager.sorted_by_urgency(descending=True)[:2]
    motive_1 = top_motives[0].type if len(top_motives) > 0 else '—'
    motive_2 = top_motives[1].type if len(top_motives) > 1 else '—'

    # Location
    location = format_location(character.location) if character.location else "in transit"

    summary_rows.append([
        character.name,
        motive_1,
        motive_2,
        location
    ])

    output += tabulate(summary_rows, headers=["Name", "Urgent Motive", "Second Motive", "Location"])

    # === Percept Contents ===
    output += "\n\n=== Percept Contents (Simplified) ===\n"
    try:
        percepts = character.get_percepts()
        if percepts:
            for entry in percepts:
                data = entry.get("data", {})
                salience = entry.get("salience", "—")
                percept_type = data.get("type", "Unknown")
                details = data.get("details", "—")
                output += f"- {percept_type} (salience: {salience}) — {details}\n"
                #print("[DEBUG] Percept data type:", type(entry.get("origin")))

        else:
            output += "— No percepts found —\n"
    except Exception as e:
        output += f"[ERROR retrieving percepts: {e}]\n"

    # === Percept Breakdown ===
    output += "\n=== Percept Type → Salience Summary ===\n"

    header_row1 = []
    header_row2 = []
    value_row = []

    percepts_dict = getattr(character, "_percepts", {})

    if percepts_dict:
        sorted_items = sorted(percepts_dict.items(), key=lambda item: item[1].get("salience", 0.0), reverse=True)

        #TMP debug block
        for key, entry in sorted_items:
            data = entry.get("data", {})
            salience = entry.get("salience", "—")
            
            if key == "self":
                percept_type = "Self"
            else:
                percept_type = data.get("type") or data.get("name")

            if not percept_type:
                percept_type = "Unknown"
                print(f"[DEBUG] Unknown Percept detected for key '{key}':")
                print(f"        salience = {salience}")
                print(f"        data = {data}")
                print(f"        keys in data = {list(data.keys())}")
                print(f"        full entry = {entry}")

            header_row1.append(percept_type)
            header_row2.append("Salience")
            value_row.append(str(salience))

        output += tabulate([header_row2, value_row], headers=header_row1, tablefmt="grid")
    else:
        output += "\n— No percepts available —\n"

    return output

def format_location(loc):
    if hasattr(loc, 'name') and hasattr(loc, 'region'):
        return f"{loc.name} in {loc.region.name if hasattr(loc.region, 'name') else loc.region}"
    return str(loc)
