def pluralize_class_name(name: str):
    # Simplified pluralization logic
    if name.endswith('y') and name[-2] not in 'aeiou':
        return name[:-1] + 'ies'
    elif name.endswith('s'):
        return name + 'es'
    else:
        return name + 's'

from collections import defaultdict
def group_reactions(reactions):
    """
    reactions: List of tuples -> (character_name, reaction_text, class_name)
    Returns grouped output lines
    """
    grouped = defaultdict(list)

    for name, reaction_text, class_name in reactions:
        key = (reaction_text, class_name)
        if name not in grouped[key]:
            grouped[key].append(name)

    output_lines = []

    for (reaction_text, class_name), names in grouped.items():
        if len(names) == 1:
            output_lines.append(f"{names[0]} {reaction_text}")
        elif len(names) == 2:
            output_lines.append(f"{names[0]} and {names[1]} {reaction_text}")
        elif len(names) == 3:
            output_lines.append(f"{names[0]}, {names[1]} and {names[2]} {reaction_text}")
        else:
            # For larger groups, just refer to class name
            output_lines.append(f"Several {class_name}s {reaction_text}")

    return output_lines
