#fix_percept_fields.py
import re
import os

FILE_PATH = "location.py"  # Adjust if needed

REQUIRED_FIELDS = [
    "name",
    "type",
    "description",
    "origin",
    "tags",
    "salience",
    "urgency",
    "source",
    "security",
    "is_open",
    "has_security",
]

PERCEPT_METHOD_TEMPLATE = '''
    def get_percept_data(self, observer=None):
        return {{
            "name": self.name,
            "type": self.__class__.__name__,
            "description": f"{{self.name}}: {{self.description}}",
            "region": self.region.name if self.region else None,
            "location": self.name,
            "origin": self,
            "tags": self.tags,
            "salience": self.compute_salience(observer),
            "urgency": 1,
            "source": None,
            "menu_options": [],
            "security": getattr(self, "security_level", 0),
            "is_open": getattr(self, "is_open", True),
            "has_security": self.has_security() if hasattr(self, "has_security") else False,
        }}
'''

def find_concrete_classes(source):
    """
    Returns a list of (class_name, class_block) tuples for concrete classes.
    """
    class_pattern = r'(class\s+(\w+)\(.*?\):\s+(?:(?:.|\n)*?))(?=\nclass|\Z)'
    results = []

    for match in re.finditer(class_pattern, source, re.MULTILINE):
        class_block = match.group(1)
        class_name = match.group(2)

        if 'is_concrete' in class_block:
            results.append((class_name, class_block))

    return results

def class_has_get_percept_data(class_block):
    return 'def get_percept_data' in class_block

def missing_fields(percept_body):
    return [key for key in REQUIRED_FIELDS if f'"{key}"' not in percept_body]

def patch_get_percept_data(percept_body: str) -> str:
    """
    Adds missing required fields to an existing percept return dict.
    """
    percept_lines = percept_body.strip().splitlines()
    closing_brace_index = next(i for i, line in enumerate(percept_lines) if line.strip().endswith('}'))

    present_keys = set()
    for line in percept_lines:
        match = re.search(r'"(\w+)"\s*:', line)
        if match:
            present_keys.add(match.group(1))

    missing = [k for k in REQUIRED_FIELDS if k not in present_keys]
    if not missing:
        return percept_body

    for field in missing:
        insert_line = f'        "{field}": "FIXME",'
        percept_lines.insert(closing_brace_index, insert_line)
        closing_brace_index += 1

    return "\n".join(percept_lines)

def patch_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    modified = source
    modified_any = False

    for class_name, class_block in find_concrete_classes(source):
        if not class_has_get_percept_data(class_block):
            # Inject new get_percept_data method
            indent = "    "
            full_patch = class_block.rstrip() + "\n" + indent + PERCEPT_METHOD_TEMPLATE.replace('\n', f'\n{indent}') + "\n"
            modified = modified.replace(class_block, full_patch)
            print(f"✅ Injected full method into {class_name}")
            modified_any = True
        else:
            # Find and patch get_percept_data return block
            method_match = re.search(r'def get_percept_data\(.*?\):\s+return\s+{([^}]+)}', class_block, re.DOTALL)
            if method_match:
                return_body = method_match.group(0)
                updated_body = patch_get_percept_data(return_body)
                if updated_body != return_body:
                    modified = modified.replace(return_body, updated_body)
                    print(f"✅ Patched missing fields in {class_name}")
                    modified_any = True

    if modified_any:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified)
        print("🎉 Patch complete and saved.")
    else:
        print("✅ All percept methods already complete.")

if __name__ == "__main__":
    if not os.path.exists(FILE_PATH):
        print(f"❌ File not found: {FILE_PATH}")
    else:
        patch_file(FILE_PATH)
