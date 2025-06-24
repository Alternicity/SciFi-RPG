import ast
import os

LOCATION_BASE_CLASSES = {"Location", "Vendor"}
DEBUG_LINE = 'print(f"[DEBUG] get_percept_data in {self.__class__.__name__}, origin: {self}")\n'

def inject_debug_line_to_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    class_defs = [node for node in tree.body if isinstance(node, ast.ClassDef)]

    modified = False
    new_lines = source.splitlines(keepends=True)

    for class_node in class_defs:
        base_names = {base.id for base in class_node.bases if isinstance(base, ast.Name)}
        if not LOCATION_BASE_CLASSES.intersection(base_names):
            continue  # skip if it's not a subclass of Location or Vendor

        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == "get_percept_data":
                start_line = node.body[0].lineno - 1  # inject before the first real line
                indent = ' ' * (len(new_lines[start_line]) - len(new_lines[start_line].lstrip()))
                debug_line = indent + DEBUG_LINE
                if DEBUG_LINE.strip() not in new_lines[start_line + 1]:
                    new_lines.insert(start_line + 1, debug_line)
                    modified = True

    if modified:
        print(f"🔧 Modified: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    else:
        print(f"✅ Skipped (no matching classes or already has debug): {file_path}")


# Update this to your actual file path if different
target_file = "location.py"

if os.path.exists(target_file):
    inject_debug_line_to_file(target_file)
else:
    print(f"❌ File not found: {target_file}")
