import os
import ast

class OriginCheckInGetPerceptData(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename

    def visit_FunctionDef(self, node):
        if node.name == "get_percept_data":
            # Look for return statement
            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    if isinstance(child.value, ast.Dict):
                        keys = [k.s for k in child.value.keys if isinstance(k, ast.Str)]
                        if "origin" not in keys:
                            print(f"[MISSING ORIGIN] {self.filename} -> get_percept_data() @ line {child.lineno}")
        self.generic_visit(node)

def scan_for_missing_origin_in_get_percept_data(root_dir="."):
    print("Scanning for missing 'origin' in get_percept_data functions...")

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".py"):
                file_path = os.path.join(dirpath, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        source = f.read()
                        tree = ast.parse(source, filename=file_path)
                        visitor = OriginCheckInGetPerceptData(file_path)
                        visitor.visit(tree)
                except SyntaxError as e:
                    print(f"[ERROR] Skipping {file_path}: {e}")

scan_for_missing_origin_in_get_percept_data("./")  # Replace path if needed
