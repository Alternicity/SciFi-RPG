import re
import sys

def add_uuid_to_classes(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File {filename} not found. Skipping.")
        return

    # Add imports if missing
    if 'import uuid' not in content:
        content = 'import uuid\n' + content
    if 'from dataclasses import field' not in content:
        if 'from dataclasses import dataclass' in content:
            content = re.sub(r'(from dataclasses import dataclass)', r'\1, field', content)
        else:
            content = 'from dataclasses import field\n' + content

    # Regex pattern to find dataclasses with classes (including multiline class body)
    pattern = re.compile(
        r'(@dataclass.*?\nclass\s+\w+\(?.*?\)?:\n(?:\s+.*\n)+)', 
        re.MULTILINE
    )

    def add_id_field(match):
        class_block = match.group(0)
        # Don't add if id already present
        if re.search(r'^\s*id\s*:', class_block, re.MULTILINE):
            return class_block

        # Find the line after the class definition line to insert id field
        lines = class_block.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith('class '):
                insert_at = i + 1
                break
        else:
            insert_at = 1

        indent = ' ' * 4  # assumes 4 spaces indentation
        id_line = f'{indent}id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)'
        lines.insert(insert_at, id_line)

        return '\n'.join(lines)

    new_content = pattern.sub(add_id_field, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Processed {filename}")

if __name__ == "__main__":
    for file in ['InWorldObjects.py', 'location.py', 'events.py']:
        add_uuid_to_classes(file)
